# Data Model: Python package to fetch and download GMRT tiles

## Entities

### BoundingBox
- minLon: float (-180 to 180)
- minLat: float (-90 to 90)
- maxLon: float (-180 to 180)
- maxLat: float (-90 to 90)
- Validations: minLon < maxLon unless antimeridian handling; minLat < maxLat; ranges within WGS84.

### DownloadRequest
- bboxes: list[BoundingBox] or single BoundingBox
- format: enum { geotiff, png }
- resolution: enum { low, medium, high }
- destination: string (absolute or relative path)
- overwrite: enum { skip, overwrite }

### ManifestEntry
- path: string
- format: enum { geotiff, png }
- coverage: BoundingBox
- size_bytes: int
- status: enum { created, reused }

### DownloadResult
- entries: list[ManifestEntry]
- stats: { count_created: int, count_reused: int }
