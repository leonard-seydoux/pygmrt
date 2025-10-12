# pygmrt

Minimal Python package to download GMRT tiles for a given bounding box.

- Providers: `gmrt` (default, no API key) and `opentopo` (requires OpenTopography API key)
- Formats: GeoTIFF (default). PNG is available in the API but not via GMRT provider.
- Resolution: low, medium (default), high
- Antimeridian: automatically handled by splitting and merging ranges

See `specs/001-create-a-python/quickstart.md` for usage examples.

## Usage

Python example (single bbox):

```python
from pygmrt.tiles import download_tiles

result = download_tiles(
	bbox=[-73.5, 40.0, -71.5, 42.0],
	dest="./data",
)
print(result)
```

To process multiple bounding boxes, call `download_tiles` in a loop.

Notes:
- Existing files are reused when `overwrite=False` (default).
- Network tests are skipped by default; enable with `-m network` in pytest.

## La Réunion example (GMRT, GeoTIFF)

```python
from pygmrt.tiles import download_tiles

result = download_tiles(
	bbox=[55.0, -21.5, 56.0, -20.5],
	dest="./data",
	format="geotiff",
	provider="gmrt",
)
print(result.entries[0].path)
```

Tip: if you encounter a corrupt or partial file (e.g. after an interrupted run), set `overwrite=True` to force a fresh download.
