# Installation

## From PyPI (Recommended)

Install the latest stable release from PyPI:

```bash
pip install pygmrt
```

## From Source

For development or the latest features:

```bash
git clone https://github.com/leonard-seydoux/pygmrt.git
cd pygmrt
pip install -e .
```

## Dependencies

pygmrt requires:

- Python 3.11+
- requests
- rasterio

Optional dependencies for examples and visualization:

- matplotlib
- cartopy
- numpy
- scipy

## Verify Installation

Test your installation:

```python
from pygmrt.tiles import download_tiles
print("pygmrt is installed correctly!")
```