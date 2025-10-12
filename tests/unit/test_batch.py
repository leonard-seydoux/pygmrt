from pygmrt import tiles


def test_multiple_calls_handle_multiple(monkeypatch, tmp_path):
    calls = []

    def fake_download(url, dest_file, **kwargs):
        dest_file.write_text("ok")
        calls.append(url)
        return dest_file.stat().st_size

    monkeypatch.setattr(tiles, "_download_stream", fake_download)

    res1 = tiles.download_tiles(
        bbox=[-10, -5, 10, 5],
        save_directory=str(tmp_path),
        resolution="low",
    )
    res2 = tiles.download_tiles(
        bbox=[170, -5, -170, 5],
        save_directory=str(tmp_path),
        resolution="low",
    )

    total_entries = len(res1.entries) + len(res2.entries)
    assert total_entries >= 2
    assert res1.count_created + res2.count_created == total_entries
    assert len(calls) == total_entries
