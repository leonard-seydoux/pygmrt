from pygmrt import tiles


def test_batch_handles_multiple(monkeypatch, tmp_path):
    calls = []

    def fake_download(url, dest_file, **kwargs):
        dest_file.write_text("ok")
        calls.append(url)
        return dest_file.stat().st_size

    monkeypatch.setattr(tiles, "_download_stream", fake_download)
    res = tiles.download_tiles(
        bboxes=[[-10, -5, 10, 5], [170, -5, -170, 5]],
        dest=str(tmp_path),
        format="geotiff",
        resolution="low",
        provider="gmrt",
    )
    assert len(res.entries) >= 2
    assert res.count_created == len(res.entries)
    assert len(calls) == len(res.entries)
