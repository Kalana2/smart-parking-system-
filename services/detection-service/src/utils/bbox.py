def clamp_bbox(bbox, width, height):
	x1, y1, x2, y2 = bbox
	x1 = max(0.0, min(float(x1), float(width)))
	y1 = max(0.0, min(float(y1), float(height)))
	x2 = max(0.0, min(float(x2), float(width)))
	y2 = max(0.0, min(float(y2), float(height)))
	if x2 < x1:
		x1, x2 = x2, x1
	if y2 < y1:
		y1, y2 = y2, y1
	return [x1, y1, x2, y2]


def is_valid_bbox(bbox):
	if not bbox or len(bbox) != 4:
		return False
	x1, y1, x2, y2 = bbox
	return x2 >= x1 and y2 >= y1
