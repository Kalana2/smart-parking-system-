# Model Weights

Place the YOLOv8 nano checkpoint here as `yolov8n.pt`.

Download it with:

```bash
curl -L --fail -o models/yolov8n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

The detection service expects this file at `/app/models/yolov8n.pt`, and `docker-compose.yml` mounts this folder into the container as read-only.
