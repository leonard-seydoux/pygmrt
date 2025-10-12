# pygmrt

[![Documentation Status](https://readthedocs.org/projects/pygmrt/badge/?version=latest)](https://pygmrt.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/pygmrt.svg)](https://badge.fury.io/py/pygmrt)

A minimal Python package for downloading Global Multi-Resolution Topography (GMRT) tiles.

## Quick Start

```python
from pygmrt.tiles import download_tiles

# Download bathymetry data for La Réunion
bbox = [55.0, -21.5, 56.0, -20.5]  # [west, south, east, north]
src = download_tiles(bbox=bbox, resolution="medium")

# Read the data
data = src.read(1)
src.close()
```

## Features

- 🌍 **Simple API**: One function to download GMRT tiles
- 🗺️ **Multiple resolutions**: Choose from low, medium, or high resolution
- 🔄 **Smart caching**: Automatically reuses downloaded files
- 🌐 **Antimeridian support**: Handles bounding boxes that cross ±180°
- 📦 **No API key required**: Direct access to GMRT GridServer

## Installation

```bash
pip install pygmrt
```

Or for development:

```bash
git clone https://github.com/leonard-seydoux/pygmrt.git
cd pygmrt
pip install -e .
```

## Documentation

```{toctree}
:maxdepth: 2
:caption: Contents

installation
usage
gallery/index
api
```

## Gallery

Explore our {doc}`gallery/index` to see pygmrt in action with real-world examples.

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`