# Detection Service

The detection service ingests a camera stream, runs YOLOv8 for vehicle detection, tracks vehicles with DeepSORT, and publishes `vehicle.detected.v1` events to RabbitMQ.

## Endpoints

- `GET /healthz` returns service health and last error (if any).
- `GET /readyz` returns readiness once the model loads and events start publishing.
- `GET /stream` returns an MJPEG stream of the latest frames.

## Configuration

These environment variables are supported:

- `PORT` (default: 8001)
- `MODEL_PATH` (default: /app/models/yolov8n.pt)
- `CAMERA_SOURCE` (default: rtsp://your-camera-url)
- `CAMERA_ID` (default: cam_01)
- `CONFIDENCE_THRESHOLD` (default: 0.5)
- `FRAME_SKIP` (default: 3)
- `RABBITMQ_HOST` (default: rabbitmq)
- `RABBITMQ_PORT` (default: 5672)
- `RABBITMQ_USER` (default: parking_admin)
- `RABBITMQ_PASSWORD` (default: parking_password)
- `RABBITMQ_EXCHANGE` (default: events)
- `RABBITMQ_ROUTING_KEY` (default: vehicle.detected.v1)
- `RABBITMQ_RETRY_MAX` (default: 5)
- `RABBITMQ_RETRY_BASE_SEC` (default: 1.0)
- `CAMERA_RETRY_MAX` (default: 5)
- `CAMERA_RETRY_BASE_SEC` (default: 1.0)
- `EVENT_SCHEMA_PATH` (default: /app/shared/events/vehicle.detected.v1.json)
- `PREVIEW_FPS` (default: 8)

## Local Run

Use Docker Compose from the repo root:

```bash
docker compose up --build detection-service
```

Set `CAMERA_SOURCE` to an RTSP URL or a local video file path.

## Tests

Run the unit tests from the repo root:

```bash
. .venv/bin/activate
python -m pip install pytest jsonschema pika
python -m pytest services/detection-service/tests -q
```
