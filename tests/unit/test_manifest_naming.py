from pygmrt.tiles import _save_filename


def test_save_filename_extension_and_tokens():
    name_tif = _save_filename("tile", (-10, -5, 10, 5))
    assert name_tif.endswith(".tif")
    assert "-10.000_-5.000_10.000_5.000" in name_tif
