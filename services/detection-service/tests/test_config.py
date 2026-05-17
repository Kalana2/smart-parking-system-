import os
import sys
from pathlib import Path

import pytest


TESTS_DIR = Path(__file__).resolve().parent
SRC_DIR = TESTS_DIR.parent / "src"
sys.path.append(str(SRC_DIR))

from config import load_config


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    keys = [
        "PORT",
        "MODEL_PATH",
        "CAMERA_SOURCE",
        "CAMERA_ID",
        "CONFIDENCE_THRESHOLD",
        "FRAME_SKIP",
        "RABBITMQ_HOST",
        "RABBITMQ_PORT",
        "RABBITMQ_USER",
        "RABBITMQ_PASSWORD",
        "RABBITMQ_EXCHANGE",
        "RABBITMQ_ROUTING_KEY",
        "RABBITMQ_RETRY_MAX",
        "RABBITMQ_RETRY_BASE_SEC",
        "CAMERA_RETRY_MAX",
        "CAMERA_RETRY_BASE_SEC",
        "EVENT_SCHEMA_PATH",
        "PREVIEW_FPS",
    ]
    for key in keys:
        monkeypatch.delenv(key, raising=False)
    yield


def test_load_config_defaults(monkeypatch, tmp_path):
    schema_path = tmp_path / "vehicle.detected.v1.json"
    schema_path.write_text("{}", encoding="utf-8")

    monkeypatch.setenv("EVENT_SCHEMA_PATH", str(schema_path))
    config = load_config()

    assert config.port == 8001
    assert config.model_path
    assert config.camera_source
    assert config.confidence_threshold == 0.5
    assert config.frame_skip == 3
    assert config.rabbitmq_host == "rabbitmq"
    assert config.rabbitmq_exchange == "events"
    assert config.rabbitmq_routing_key == "vehicle.detected.v1"
    assert config.preview_fps == 8


def test_invalid_confidence_threshold(monkeypatch):
    monkeypatch.setenv("CONFIDENCE_THRESHOLD", "1.5")
    with pytest.raises(ValueError):
        load_config()
