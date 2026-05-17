from ultralytics import YOLO


class Detector:
	def __init__(self, model_path):
		self.model = YOLO(model_path)

	def detect(self, frame, confidence_threshold):
		results = self.model.predict(source=frame, conf=confidence_threshold, verbose=False)
		if not results:
			return []
		result = results[0]
		if result.boxes is None:
			return []
		class_names = result.names or {}
		detections = []
		for box in result.boxes:
			bbox = box.xyxy[0].tolist()
			confidence = float(box.conf[0])
			class_id = int(box.cls[0])
			class_name = class_names.get(class_id, str(class_id))
			detections.append(
				{
					"bbox": bbox,
					"confidence": confidence,
					"class": class_name,
				}
			)
		return detections
