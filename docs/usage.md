# Usage

Basic example: download a GeoTIFF for La Réunion and print the saved file path.

```python
from pygmrt.tiles import download_tiles, get_path

bbox = [55.0, -21.5, 56.0, -20.5]  # [west, south, east, north]
result = download_tiles(bbox=bbox, save_directory="./data", resolution="low")

print(get_path(result))
```

Notes
- Existing files are reused when `overwrite=False` (default).
- The function handles antimeridian crossing automatically.
