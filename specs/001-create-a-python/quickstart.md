# Quickstart: pygmrt tile downloader

## Install

1. Ensure Python 3.11 is installed.
2. Install package (after implementation): `pip install pygmrt` (placeholder).

## Basic usage

```python
from pygmrt.tiles import download_tiles

# Download a 2° x 2° bbox with defaults to ./data
result = download_tiles(bbox=[-73.5, 40.0, -71.5, 42.0], save_directory="./data")
print(result)
```

## Options

- resolution: "low", "medium" (default), "high"
- save_directory: folder path to write files into
- overwrite: False (default) or True

## Notes

- If bbox crosses the antimeridian, the function auto-splits the download ranges.
- Existing files are reused when overwrite=False.
- Network tests may be opt-in in CI to avoid flakiness.
