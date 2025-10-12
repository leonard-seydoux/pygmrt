from pygmrt.tiles import _safe_filename


def test_safe_filename_formats():
    name_tif = _safe_filename("tile", "geotiff", (-10, -5, 10, 5))
    assert name_tif.endswith(".tif")
    assert "-10.000_-5.000_10.000_5.000" in name_tif
