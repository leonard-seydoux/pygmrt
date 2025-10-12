# Notebooks: Examples and How-To

This folder contains runnable examples demonstrating the `pygmrt` API and plotting results.

## How to run

```bash
# From the project root
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install cartopy rasterio matplotlib ipykernel
python -m ipykernel install --user --name pygmrt --display-name "Python (pygmrt)"

# Start Jupyter
jupyter notebook notebooks/
```

## Index

1. `playground.ipynb`
   - Download a small GeoTIFF for La Réunion and plot a hillshade.
   - Demonstrates: `download_tiles`, `get_path`, Cartopy map.

2. `resolutions.ipynb` (to be added)
   - Download the same bbox at `low`, `medium`, and `high` resolutions to compare size/visuals.

3. `antimeridian.ipynb` (to be added)
   - Download a bbox crossing the antimeridian to demonstrate automatic splitting.

4. `large_area.ipynb` (to be added)
   - Download a larger bbox; discuss trade-offs and optional overwriting.
