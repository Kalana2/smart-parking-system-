import sys
from pathlib import Path


TESTS_DIR = Path(__file__).resolve().parent
SRC_DIR = TESTS_DIR.parent / "src"
sys.path.append(str(SRC_DIR))

from utils.bbox import clamp_bbox, is_valid_bbox


def test_clamp_bbox_swaps_and_clamps():
    bbox = clamp_bbox([120, 90, 20, -10], width=100, height=80)
    assert bbox == [20.0, 0.0, 100.0, 80.0]


def test_is_valid_bbox():
    assert is_valid_bbox([0, 0, 10, 10])
    assert not is_valid_bbox([10, 10, 0, 0])
    assert not is_valid_bbox([1, 2, 3])
