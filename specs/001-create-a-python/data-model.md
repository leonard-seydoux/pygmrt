# Data Model: Python package to fetch and download GMRT tiles

## Entities

### BoundingBox
- west: float (-180 to 180)
- south: float (-90 to 90)
- east: float (-180 to 180)
- north: float (-90 to 90)
- Validations: minLon < maxLon unless antimeridian handling; minLat < maxLat; ranges within WGS84.

### DownloadRequest
- bbox: BoundingBox
- resolution: enum { low, medium, high }
- save_directory: string (absolute or relative path)
- overwrite: boolean

### ManifestEntry
- path: string
- coverage: BoundingBox
- size_bytes: int
- status: enum { created, reused }

### DownloadResult
- entries: list[ManifestEntry]
- count_created: int
- count_reused: int
- errors: list[string]
