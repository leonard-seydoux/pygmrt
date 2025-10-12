from pathlib import Path

from pygmrt import tiles


def test_save_directory_accepts_path(monkeypatch, tmp_path):
    calls = []

    def fake_download(url, dest_file, **kwargs):
        dest_file.write_text("ok")
        calls.append(url)
        return dest_file.stat().st_size

    monkeypatch.setattr(tiles, "_download_stream", fake_download)

    save_dir: Path = tmp_path / "out"
    res = tiles.download_tiles(
        bbox=[-10, -5, -9.5, -4.5],
        save_directory=save_dir,  # pass a Path, not str
        resolution="low",
        overwrite=True,
    )

    assert len(res.entries) >= 1
    for e in res.entries:
        assert Path(e.path).exists()
    assert len(calls) == len(res.entries)
