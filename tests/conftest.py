"""Pytest configuration and shared fixtures."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def valid_bbox():
    """Provide a valid bounding box for testing."""
    return [10.0, 20.0, 30.0, 40.0]


@pytest.fixture
def la_reunion_bbox():
    """Provide La Réunion Island bounding box."""
    return [55.05, -21.5, 55.95, -20.7]


@pytest.fixture
def antimeridian_bbox():
    """Provide a bounding box crossing the antimeridian."""
    return [170.0, -10.0, -170.0, 10.0]


@pytest.fixture
def invalid_bboxes():
    """Provide a list of invalid bounding boxes for testing."""
    return [
        [10.0, 20.0, 30.0],  # Wrong length
        [200.0, 20.0, 30.0, 40.0],  # Longitude out of range
        [10.0, 100.0, 30.0, 40.0],  # Latitude out of range
        [10.0, 40.0, 30.0, 20.0],  # South > North
    ]
