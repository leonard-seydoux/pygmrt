from pathlib import Path

import pytest

from pygmrt.tiles import DownloadResult, ManifestEntry, get_path


def test_get_path_success(tmp_path):
    # Prepare a fake existing tif file
    tif = tmp_path / "gmrt_0.000_0.000_1.000_1.000.tif"
    tif.write_text("ok")

    entry = ManifestEntry(
        path=str(tif),
        coverage={"west": 0.0, "south": 0.0, "east": 1.0, "north": 1.0},
        size_bytes=tif.stat().st_size,
        status="created",
    )
    result = DownloadResult(entries=[entry])

    p = get_path(result)
    assert p == tif


essential_msg = "No GeoTIFF"  # substring we expect in error message


def test_get_path_no_match(tmp_path):
    # No files created, or wrong extension
    other = tmp_path / "gmrt_0.000_0.000_1.000_1.000.xyz"
    other.write_text("ok")

    entry = ManifestEntry(
        path=str(other),
        coverage={"west": 0.0, "south": 0.0, "east": 1.0, "north": 1.0},
        size_bytes=other.stat().st_size,
        status="created",
    )
    result = DownloadResult(entries=[entry])

    with pytest.raises(RuntimeError) as e:
        get_path(result)
    assert "No GeoTIFF" in str(e.value)
