from deep_sort_realtime.deepsort_tracker import DeepSort


class Tracker:
	def __init__(self):
		self.tracker = DeepSort(max_age=30, n_init=2)

	def update(self, detections, frame):
		formatted = [
			(det["bbox"], det["confidence"], det["class"]) for det in detections
		]
		tracks = self.tracker.update_tracks(formatted, frame=frame)
		results = []
		for track in tracks:
			if not track.is_confirmed():
				continue
			track_id = track.track_id
			ltrb = track.to_ltrb()
			results.append(
				{
					"track_id": int(track_id),
					"bbox": [float(x) for x in ltrb],
					"class": track.det_class or "unknown",
					"confidence": float(track.det_conf) if track.det_conf is not None else None,
				}
			)
		return results
