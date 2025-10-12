# pygmrt

Minimal Python package to download GMRT GeoTIFF tiles from GMRT GridServer by bounding box.

## Installation

Use one of the options below.

Option A — install directly from GitHub (no local clone required):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install "git+https://github.com/leonard-seydoux/pygmrt.git"
```

Option B — develop locally (editable install):

```bash
git clone https://github.com/leonard-seydoux/pygmrt.git
cd pygmrt
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Optional: for the plotting notebooks, install extras (Cartopy, Rasterio, Matplotlib):

```bash
pip install cartopy rasterio matplotlib ipykernel
python -m ipykernel install --user --name pygmrt --display-name "Python (pygmrt)"
```

## Quickstart

```python
from pathlib import Path
from pygmrt.tiles import download_tiles, get_path

# La Réunion bbox [west, south, east, north]
bbox = [55.0, -21.5, 56.0, -20.5]
result = download_tiles(bbox=bbox, save_directory="./data", resolution="low")

tif_path = get_path(result)
print(f"Saved to: {tif_path}")
```

## Examples (Notebooks)

All examples live in the `notebooks/` directory and can be run in Jupyter.

- `playground.ipynb` — simple La Réunion demo with a hillshade plot.
- `resolutions.ipynb` — compare downloads at low/medium/high resolutions.
- `antimeridian.ipynb` — bbox that crosses the antimeridian (auto-split).

See `notebooks/README.md` for a short index and how to run them.

## API

```python
download_tiles(*, bbox, save_directory, resolution="medium", overwrite=False) -> DownloadResult
get_path(result: DownloadResult) -> pathlib.Path
```

- Provider: GMRT GridServer (no API key)
- Format: GeoTIFF (implicit)
- BoundingBox keys: `west`, `south`, `east`, `north`

## Development

Run tests and lint locally:

```bash
pytest -q
ruff check -q
```
