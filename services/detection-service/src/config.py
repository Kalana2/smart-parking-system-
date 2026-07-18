import os
from dataclasses import dataclass


def _get_env(name, default=None):
	value = os.getenv(name, default)
	if value is None or value == "":
		raise ValueError(f"Missing required environment variable: {name}")
	return value


def _get_int(name, default=None, minimum=None):
	raw = os.getenv(name, default)
	if raw is None or raw == "":
		raise ValueError(f"Missing required environment variable: {name}")
	try:
		value = int(raw)
	except ValueError as exc:
		raise ValueError(f"Invalid integer for {name}: {raw}") from exc
	if minimum is not None and value < minimum:
		raise ValueError(f"{name} must be >= {minimum}")
	return value


def _get_float(name, default=None, minimum=None, maximum=None):
	raw = os.getenv(name, default)
	if raw is None or raw == "":
		raise ValueError(f"Missing required environment variable: {name}")
	try:
		value = float(raw)
	except ValueError as exc:
		raise ValueError(f"Invalid float for {name}: {raw}") from exc
	if minimum is not None and value < minimum:
		raise ValueError(f"{name} must be >= {minimum}")
	if maximum is not None and value > maximum:
		raise ValueError(f"{name} must be <= {maximum}")
	return value


@dataclass(frozen=True)
class Config:
	port: int
	model_path: str
	camera_source: str
	camera_id: str
	confidence_threshold: float
	frame_skip: int
	rabbitmq_host: str
	rabbitmq_port: int
	rabbitmq_user: str
	rabbitmq_password: str
	rabbitmq_exchange: str
	rabbitmq_routing_key: str
	rabbitmq_retry_max: int
	rabbitmq_retry_base_sec: float
	camera_retry_max: int
	camera_retry_base_sec: float
	camera_loop: bool
	event_schema_path: str
	preview_fps: int


def load_config():
	return Config(
		port=_get_int("PORT", "8001", minimum=1),
		model_path=_get_env("MODEL_PATH", "/app/models/yolov8n.pt"),
		camera_source=_get_env("CAMERA_SOURCE", "/app/videos/sample.mp4"),
		camera_id=os.getenv("CAMERA_ID", "cam_01"),
		confidence_threshold=_get_float("CONFIDENCE_THRESHOLD", "0.5", minimum=0.0, maximum=1.0),
		frame_skip=_get_int("FRAME_SKIP", "3", minimum=1),
		rabbitmq_host=_get_env("RABBITMQ_HOST", "rabbitmq"),
		rabbitmq_port=_get_int("RABBITMQ_PORT", "5672", minimum=1),
		rabbitmq_user=_get_env("RABBITMQ_USER", "parking_admin"),
		rabbitmq_password=_get_env("RABBITMQ_PASSWORD", "parking_password"),
		rabbitmq_exchange=os.getenv("RABBITMQ_EXCHANGE", "events"),
		rabbitmq_routing_key=os.getenv("RABBITMQ_ROUTING_KEY", "vehicle.detected.v1"),
		rabbitmq_retry_max=_get_int("RABBITMQ_RETRY_MAX", "5", minimum=0),
		rabbitmq_retry_base_sec=_get_float("RABBITMQ_RETRY_BASE_SEC", "1.0", minimum=0.1),
		camera_retry_max=_get_int("CAMERA_RETRY_MAX", "5", minimum=0),
		camera_retry_base_sec=_get_float("CAMERA_RETRY_BASE_SEC", "1.0", minimum=0.1),
		camera_loop=os.getenv("CAMERA_LOOP", "true").lower() == "true",
		event_schema_path=os.getenv(
			"EVENT_SCHEMA_PATH", "/app/shared/events/vehicle.detected.v1.json"
		),
		preview_fps=_get_int("PREVIEW_FPS", "8", minimum=1),
	)
