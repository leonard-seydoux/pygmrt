<div align="center">

<img src="https://raw.githubusercontent.com/leonard-seydoux/pygmrt/main/docs/images/logo.png" alt="PyGMRT Logo" width=100/>

### PyGMRT

Downloading bathymetry and topography tiles from the<br>
[Global Multi-Resolution Topography (GMRT)](https://www.gmrt.org/) synthesis.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
![PyPI_Downloads](https://img.shields.io/pypi/dd/pygmrt)
![LICENSE](https://img.shields.io/pypi/l/pygmrt)
![Last Release](https://img.shields.io/github/v/release/leonard-seydoux/pygmrt)
![Last Commit](https://img.shields.io/github/last-commit/leonard-seydoux/pygmrt)


</div>

## Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Example: La Réunion Island Relief](#example-la-réunion-island-relief)
- [Example: Colombia Relief](#example-colombia-relief)
- [API Reference](#api-reference)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

PyGMRT provides a simple Python interface to access bathymetry and topography data from the [Global Multi-Resolution Topography](https://www.gmrt.org/) (GMRT) synthesis. The package handles all the complexity of downloading and processing geographic tiles, letting you focus on your analysis.

The core functionality centers around a single function that downloads tiles for any region on Earth. You can choose between three resolution levels: high resolution at 1 arc-second (about 30 meters at the equator), medium resolution at 4 arc-seconds, or low resolution at 16 arc-seconds. All data comes in GeoTIFF format, which works directly with [rasterio](https://rasterio.readthedocs.io/) and other geospatial tools.

The package automatically handles regions that cross the antimeridian (the 180° longitude line). This is often painful when working with global data, but PyGMRT takes care of it transparently. Since the package connects directly to the GMRT GridServer, you don't need API keys or authentication.

## Installation

We recommend using [UV](https://uv.readthedocs.io/), a modern Python package installer that handles dependencies efficiently. Traditional pip works just as well.

If you're using UV, add PyGMRT to your project:

```bash
uv add pygmrt
```

Or install from the latest development version:

```bash
git clone https://github.com/leonard-seydoux/pygmrt.git
cd pygmrt
uv sync
```

For pip users, install directly from PyPI:

```bash
pip install pygmrt
```

Or install from source:

```bash
git clone https://github.com/leonard-seydoux/pygmrt.git
cd pygmrt
pip install -e .
```

## Quick start

The simplest way to download topography data is with a single function call. Here we'll download data for La Réunion Island, a volcanic island in the Indian Ocean. The bounding box is specified as `[west, south, east, north]` in degrees.


```python
# Configure matplotlib to output SVG format for better quality
%config InlineBackend.figure_format = 'svg'
```


```python
from pygmrt.tiles import download_tiles

# Get tiles for La Réunion Island [west, south, east, north]
tiles = download_tiles(bbox=[55.05, -21.5, 55.95, -20.7], resolution="low")

# Print tiles
print(f"Downloaded tiles at: ./{tiles.name}")
print(f"CRS: {tiles.crs}")
print(f"Tiles array shape: {tiles.shape}")
```

    Downloaded tiles at: ./geotiff/gmrt_low_55.050_-21.500_55.950_-20.700.tif
    CRS: EPSG:4326
    Tiles array shape: (783, 821)


## Example: La Réunion Island Relief

La Réunion Island is home to one of the world's most active volcanoes. Its dramatic topography makes an excellent demonstration of PyGMRT's capabilities combined with matplotlib's hillshading.

In this example, we download medium-resolution data and apply illumination effects to create a 3D relief map. We use [pycpt-city](https://github.com/leonard-seydoux/pycpt-city) for the color palette and [Cartopy](https://scitools.org.uk/cartopy/) to handle the geographic projection.


```python
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pycpt
from matplotlib.colors import LightSource
from pygmrt.tiles import download_tiles

# La Réunion bbox [west, south, east, north]
bbox = [55.05, -21.5, 55.95, -20.7]

# Download
tiles = download_tiles(bbox=bbox, resolution="medium")

# Remove NaNs and smooth a bit for better visualization
topo = tiles.read(1)
topo[np.isnan(topo)] = 0
vmax = abs(topo).max()
bbox = tiles.bounds
extent = (bbox.left, bbox.right, bbox.bottom, bbox.top)
palette = pycpt.read("wiki-france")
palette.interpolate(256)

# Create figure
fig = plt.figure(figsize=(7, 7))
ax = plt.axes(projection=ccrs.PlateCarree())

# Hillshade
sun = LightSource(azdeg=0, altdeg=20)
shade = sun.shade(
    topo,
    cmap=palette.cmap,
    norm=palette.norm,
    vert_exag=0.05,
    blend_mode="soft",
)
ax.imshow(shade, extent=extent, origin="upper", transform=ccrs.PlateCarree())

# Extra map features
palette.colorbar(ax=ax, label="Elevation (m)", shrink=0.5)
ax.set_extent(extent)
gridlines = ax.gridlines(draw_labels=True, color="white", alpha=0.3)
gridlines.top_labels = False
gridlines.right_labels = False
ax.set_title("La Réunion Island with illumination")

plt.show()
```


    
![svg](https://raw.githubusercontent.com/leonard-seydoux/pygmrt/main/docs/images/README_8_0.svg)
    


## Example: Colombia Relief

Colombia offers a fascinating study in topographic diversity. From the Andes mountains to the Pacific and Caribbean coasts, and the Amazon basin in the southeast. This example shows how PyGMRT handles larger geographic areas.

We use low resolution here since we're covering a substantial area. The custom color palette works well for showing both underwater features and mountain ranges. Notice how the hillshading brings out the texture of the seafloor and the terrestrial topography.


```python
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pycpt
from cartopy import feature as cfeature
from matplotlib.colors import LightSource
from pygmrt.tiles import download_tiles

# Colombia bbox [west, south, east, north]
bbox = [-80.0, -5.0, -66.0, 13.0]

# Download
tiles = download_tiles(bbox=bbox, resolution="low")

# Remove NaNs and smooth a bit for better visualization
topo = tiles.read(1)
topo[np.isnan(topo)] = 0
vmax = abs(topo).max()
bbox = tiles.bounds
extent = (bbox.left, bbox.right, bbox.bottom, bbox.top)
palette = pycpt.read("colombia")

# Create figure
fig = plt.figure(figsize=(7, 7))
ax = plt.axes(projection=ccrs.PlateCarree())

# Hillshade
sun = LightSource(azdeg=0, altdeg=60)
shade = sun.shade(
    topo,
    cmap=palette.cmap,
    norm=palette.norm,
    vert_exag=0.5,
    blend_mode="soft",
)
ax.imshow(shade, extent=extent, origin="upper", transform=ccrs.PlateCarree())

# Extra map features
palette.colorbar(ax=ax, label="Elevation (m)", shrink=0.5)
ax.set_extent(extent)
ax.coastlines(color="k", linewidth=0.8)
ax.add_feature(cfeature.BORDERS, edgecolor="k", linewidth=0.8)
gridlines = ax.gridlines(draw_labels=True, color="white", alpha=0.3)
gridlines.top_labels = False
gridlines.right_labels = False
ax.set_title("Colombia relief")

plt.show()
```


    
![svg](https://raw.githubusercontent.com/leonard-seydoux/pygmrt/main/docs/images/README_10_0.svg)
    


## API Reference

The `download_tiles` function is the main entry point. Here's the complete documentation:


```python
help(download_tiles)
```

    Help on function download_tiles in module pygmrt.tiles:
    
    download_tiles(*, bbox: 'Sequence[float]' = None, save_directory: 'str | Path' = './geotiff', resolution: 'Resolution' = 'medium', overwrite: 'bool' = False) -> 'rasterio.DatasetReader'
        Download tiles and return the rasterio dataset.
        
        Parameters
        ----------
        bbox : sequence of float
            Bounding box in WGS84 degrees as ``[west, south, east, north]``.
        save_directory : str or pathlib.Path
            Destination directory path where files will be written. Created if
            needed.
        resolution : {"low", "medium", "high"}, default "medium"
            Named resolution level; mapped internally to provider-specific datasets.
        overwrite : bool, default False
            If ``False``, reuse existing files. If ``True``, force re-download.
        
        Returns
        -------
        rasterio.DatasetReader
            Opened rasterio dataset for the downloaded GeoTIFF. The caller is
            responsible for closing the dataset.
        
        Raises
        ------
        ValueError
            If invalid argument combinations or bbox values are provided.
        PermissionError
            If the destination directory is not writable.
        RuntimeError
            If download attempts ultimately fail.
    


## Development

To contribute or experiment with the code, start by cloning the repository:

```bash
git clone https://github.com/leonard-seydoux/pygmrt.git
cd pygmrt

# Install with UV (includes all development dependencies)
uv sync --all-extras

# Or use pip
pip install -e ".[dev,docs]"
```

Run the test suite to verify everything works:

```bash
# With UV
uv run pytest

# Or directly
pytest
```

This documentation is generated from `docs/readme.ipynb`. To rebuild it:

```bash
cd docs
make              # Build logo and README
make logo         # Generate logo only
make readme       # Convert notebook to README
```

The build process handles image generation and ensures URLs point to GitHub for proper display on PyPI.

## Contributing

PyGMRT is open source and welcomes contributions! Found a bug or have an idea? Open an issue or submit a pull request on [GitHub](https://github.com/leonard-seydoux/pygmrt).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This package builds on the work of several organizations and projects:

- The [Global Multi-Resolution Topography Synthesis](https://www.gmrt.org/) by [Lamont-Doherty Earth Observatory](https://www.ldeo.columbia.edu/) for providing free access to global bathymetry data.
- The [cpt-city](http://seaviewsensing.com/pub/cpt-city/) project for beautiful color palettes, accessible via [pycpt-city](https://github.com/leonard-seydoux/pycpt-city).
