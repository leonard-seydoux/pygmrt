from pygmrt.tiles import _validate_bbox, _split_antimeridian
import pytest


def test_validate_bbox_ok():
    assert _validate_bbox([-10, -5, 10, 5]) == (-10.0, -5.0, 10.0, 5.0)


def test_validate_bbox_lat_range_error():
    with pytest.raises(ValueError):
        _validate_bbox([-10, 5, 10, -5])


def test_validate_bbox_lon_range_bounds():
    with pytest.raises(ValueError):
        _validate_bbox([-181, -5, 10, 5])


def test_antimeridian_split_no_cross():
    assert _split_antimeridian(-10, 10) == [(-10, 10)]


def test_antimeridian_split_cross():
    assert _split_antimeridian(170, -170) == [(170, 180.0), (-180.0, -170)]
