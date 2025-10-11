import pytest
from pygmrt.tiles import _map_resolution, _build_url, download_tiles


def test_map_resolution_levels():
    assert _map_resolution("low") == "low"
    assert _map_resolution("medium") == "medium"
    assert _map_resolution("high") == "high"


def test_build_url_contains_params_gmrt():
    url = _build_url(-10, -5, 10, 5, "geotiff", "medium", "gmrt")
    # GMRT GridServer uses west/east/south/north
    assert "west=-10" in url and "east=10" in url
    assert "south=-5" in url and "north=5" in url
    assert "format=geotiff" in url


def test_invalid_format():
    with pytest.raises(ValueError):
        download_tiles(bbox=[-10, -5, 10, 5], dest="./data", format="jpeg")


def test_invalid_resolution():
    with pytest.raises(ValueError):
        download_tiles(
            bbox=[-10, -5, 10, 5], dest="./data", resolution="ultra"
        )
