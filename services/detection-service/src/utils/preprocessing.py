import cv2


def resize_frame(frame, width, height):
	return cv2.resize(frame, (width, height))


def to_rgb(frame):
	return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
