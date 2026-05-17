import os
import threading
import time
import uuid
from datetime import datetime, timezone

import cv2
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

from config import load_config
from detector import Detector
from publisher import Publisher
from tracker import Tracker


class PipelineState:
	def __init__(self):
		self.last_frame_jpeg = None
		self.last_frame_ts = 0.0
		self.last_error = None
		self.lock = threading.Lock()
		self.ready_event = threading.Event()
		self.stop_event = threading.Event()

	def update_frame(self, jpeg_bytes):
		with self.lock:
			self.last_frame_jpeg = jpeg_bytes
			self.last_frame_ts = time.time()

	def get_frame(self):
		with self.lock:
			return self.last_frame_jpeg


def _utc_now():
	return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _encode_jpeg(frame):
	ok, buffer = cv2.imencode(".jpg", frame)
	if not ok:
		return None
	return buffer.tobytes()


def _capture_loop(state, config):
	if not os.path.exists(config.model_path):
		state.last_error = f"Model file not found: {config.model_path}"
		return

	detector = Detector(config.model_path)
	tracker = Tracker()
	publisher = Publisher(config)

	frame_id = 0
	camera_attempt = 0
	capture = None

	while not state.stop_event.is_set():
		if capture is None or not capture.isOpened():
			if camera_attempt > config.camera_retry_max:
				state.last_error = "Camera open failed after retries"
				return
			capture = cv2.VideoCapture(config.camera_source)
			if not capture.isOpened():
				camera_attempt += 1
				delay = config.camera_retry_base_sec * (2 ** (camera_attempt - 1))
				time.sleep(delay)
				continue
			camera_attempt = 0

		ok, frame = capture.read()
		if not ok:
			capture.release()
			capture = None
			camera_attempt += 1
			delay = config.camera_retry_base_sec * (2 ** (camera_attempt - 1))
			time.sleep(delay)
			continue

		jpeg_bytes = _encode_jpeg(frame)
		if jpeg_bytes:
			state.update_frame(jpeg_bytes)

		if frame_id % config.frame_skip != 0:
			frame_id += 1
			continue

		detections = detector.detect(frame, config.confidence_threshold)
		tracks = tracker.update(detections, frame)

		vehicles = []
		for track in tracks:
			vehicles.append(
				{
					"track_id": track["track_id"],
					"class": track["class"],
					"bbox": [round(x, 2) for x in track["bbox"]],
					"confidence": round(track["confidence"] or 0.0, 4),
				}
			)

		payload = {
			"event_id": str(uuid.uuid4()),
			"timestamp": _utc_now(),
			"frame_id": frame_id,
			"camera_id": config.camera_id,
			"vehicles": vehicles,
		}

		try:
			publisher.publish(payload)
			state.ready_event.set()
		except Exception as exc:
			state.last_error = str(exc)
			return

		frame_id += 1


app = FastAPI(title="Detection Service", version="1.0")
state = PipelineState()
config = load_config()


@app.on_event("startup")
def on_startup():
	worker = threading.Thread(target=_capture_loop, args=(state, config), daemon=True)
	worker.start()


@app.on_event("shutdown")
def on_shutdown():
	state.stop_event.set()


@app.get("/healthz")
def healthz():
	payload = {"status": "ok"}
	if state.last_error:
		payload["error"] = state.last_error
	return payload


@app.get("/readyz")
def readyz(response: Response):
	if state.ready_event.is_set():
		return {"status": "ready"}
	response.status_code = 503
	return {"status": "starting"}


@app.get("/stream")
def stream():
	boundary = "frame"

	def generator():
		interval = 1.0 / max(config.preview_fps, 1)
		while not state.stop_event.is_set():
			frame = state.get_frame()
			if frame:
				yield (
					f"--{boundary}\r\n"
					"Content-Type: image/jpeg\r\n\r\n"
				).encode("utf-8") + frame + b"\r\n"
			time.sleep(interval)

	return StreamingResponse(
		generator(),
		media_type=f"multipart/x-mixed-replace; boundary={boundary}",
	)


if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="0.0.0.0", port=config.port)
