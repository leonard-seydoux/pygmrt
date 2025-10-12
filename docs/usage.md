# Usage

## Basic Usage

The main function is `download_tiles()` which downloads GMRT bathymetry data and returns a rasterio dataset:

```python
from pygmrt.tiles import download_tiles

# Define bounding box [west, south, east, north] in WGS84 degrees
bbox = [55.0, -21.5, 56.0, -20.5]  # La Réunion area

# Download medium resolution data
src = download_tiles(bbox=bbox, resolution="medium")

# Read the elevation data
elevation = src.read(1)

# Don't forget to close the dataset
src.close()
```

## Resolution Levels

Choose from three resolution levels:

- **`"low"`**: Lower resolution, faster download, smaller files
- **`"medium"`**: Balanced resolution and file size (default)
- **`"high"`**: Highest resolution, slower download, larger files

```python
# High resolution for detailed analysis
src = download_tiles(bbox=bbox, resolution="high")
```

## File Management

### Custom Save Directory

```python
src = download_tiles(
    bbox=bbox, 
    save_directory="./my_data",
    resolution="medium"
)
```

### Overwrite Existing Files

```python
# Force re-download even if file exists
src = download_tiles(bbox=bbox, overwrite=True)
```

## Antimeridian Crossing

pygmrt automatically handles bounding boxes that cross the ±180° meridian:

```python
# Crosses the international date line
bbox = [170.0, -5.0, -170.0, 5.0]
src = download_tiles(bbox=bbox)
```

## Working with the Data

### Basic Visualization

```python
import matplotlib.pyplot as plt
import numpy as np

src = download_tiles(bbox=bbox)
data = src.read(1)

# Simple plot
plt.figure(figsize=(10, 8))
plt.imshow(data, cmap='terrain')
plt.colorbar(label='Elevation (m)')
plt.title('GMRT Bathymetry')
plt.show()

src.close()
```

### With Cartopy

```python
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

src = download_tiles(bbox=bbox)
data = src.read(1)
bounds = src.bounds

fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# Plot data with correct extent
extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
im = ax.imshow(data, extent=extent, transform=ccrs.PlateCarree(), cmap='terrain')

ax.coastlines()
ax.gridlines(draw_labels=True)
plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.1)

src.close()
plt.show()
```

## Error Handling

```python
try:
    src = download_tiles(bbox=bbox)
    data = src.read(1)
    # Process data...
except ValueError as e:
    print(f"Invalid parameters: {e}")
except RuntimeError as e:
    print(f"Download failed: {e}")
finally:
    if 'src' in locals():
        src.close()
```

## Best Practices

1. **Always close datasets**: Use `src.close()` or context managers
2. **Start with low resolution**: Test your workflow before downloading large files
3. **Use appropriate resolution**: Match resolution to your analysis needs
4. **Check data quality**: GMRT resolution varies by location
5. **Handle missing data**: Use `np.isnan()` to check for NoData values

For more examples, see our {doc}`gallery/index`.