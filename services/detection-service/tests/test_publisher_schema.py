import sys
from pathlib import Path

import pytest


TESTS_DIR = Path(__file__).resolve().parent
SRC_DIR = TESTS_DIR.parent / "src"
REPO_ROOT = TESTS_DIR.parents[2]
SCHEMA_PATH = REPO_ROOT / "shared" / "events" / "vehicle.detected.v1.json"

sys.path.append(str(SRC_DIR))

from publisher import Publisher


class DummyConfig:
    def __init__(self):
        self.event_schema_path = str(SCHEMA_PATH)
        self.rabbitmq_user = "user"
        self.rabbitmq_password = "pass"
        self.rabbitmq_host = "host"
        self.rabbitmq_port = 5672
        self.rabbitmq_exchange = "events"
        self.rabbitmq_routing_key = "vehicle.detected.v1"
        self.rabbitmq_retry_max = 0
        self.rabbitmq_retry_base_sec = 0.1


def test_publisher_schema_validation():
    publisher = Publisher(DummyConfig())
    payload = {
        "event_id": "b3e1a8af-4ae5-43da-9a0e-fb08e758b818",
        "timestamp": "2026-05-01T10:30:00Z",
        "frame_id": 10,
        "camera_id": "cam_01",
        "vehicles": [
            {
                "track_id": 1,
                "class": "car",
                "bbox": [10, 20, 40, 80],
                "confidence": 0.9,
            }
        ],
    }
    publisher._validate(payload)


def test_publisher_schema_rejects_missing_fields():
    publisher = Publisher(DummyConfig())
    payload = {
        "event_id": "b3e1a8af-4ae5-43da-9a0e-fb08e758b818",
        "timestamp": "2026-05-01T10:30:00Z",
        "frame_id": 10,
        "vehicles": [],
    }
    with pytest.raises(ValueError):
        publisher._validate(payload)
