import requests
import pytest

from pygmrt.tiles import _build_url


@pytest.mark.network
def test_gmrt_gridserver_small_bbox_tiff_signature():
    # A tiny bbox near La Réunion to keep payload small
    url = _build_url(55.0, -21.5, 55.1, -21.4, "geotiff", "medium")
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        # Should be a binary attachment; content-type may be octet-stream
        assert (
            r.headers.get("Content-Disposition", "").lower().find(".tif") != -1
        )
        head = next(r.iter_content(chunk_size=32))
        # TIFF magic: little-endian 49 49 2A 00 or big-endian 4D 4D 00 2A
        assert head[:4] in (b"II*\x00", b"MM\x00*")
