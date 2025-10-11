"""Tiles download module.

Minimal API to download GMRT tiles for a given bounding box or batch of bboxes.
Public entry point: download_tiles(...)

This module intentionally keeps the surface area small to align with the project
constitution and plan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    TypedDict,
)
import os
from pathlib import Path
from time import sleep
import requests

GMRT_BASE_URL = "https://www.gmrt.org/services/GridServer"
OPENTOPO_BASE_URL = "https://portal.opentopography.org/API/globaldem"


Format = Literal["geotiff", "png"]
Provider = Literal["gmrt", "opentopo"]
Resolution = Literal["low", "medium", "high"]
Overwrite = Literal["skip", "overwrite"]


class BoundingBox(TypedDict):
    minLon: float
    minLat: float
    maxLon: float
    maxLat: float


@dataclass
class ManifestEntry:
    path: str
    format: Format
    coverage: BoundingBox
    size_bytes: int
    status: Literal["created", "reused"]


@dataclass
class DownloadResult:
    entries: List[ManifestEntry]
    count_created: int = 0
    count_reused: int = 0
    errors: List[str] = field(default_factory=list)


def download_tiles(
    *,
    bbox: Optional[Sequence[float]] = None,
    bboxes: Optional[Iterable[Sequence[float]]] = None,
    dest: str,
    format: Format = "geotiff",
    resolution: Resolution = "medium",
    overwrite: Overwrite = "skip",
    provider: Provider = "gmrt",
) -> DownloadResult:
    """Download GMRT tiles for one bbox or a batch of bboxes.

    Args:
        bbox: [minLon, minLat, maxLon, maxLat] in WGS84 degrees.
        bboxes: Iterable of bbox sequences (mutually exclusive with bbox).
        dest: Destination directory to write files.
        format: Output format: "geotiff" (default) or "png".
        resolution: Named resolution level: "low", "medium" (default), "high".
        overwrite: "skip" (default) to reuse existing files, or "overwrite".

    Returns:
        DownloadResult with manifest entries and counts.
    """
    # Validate mutually exclusive bbox/bboxes
    if (bbox is None and bboxes is None) or (
        bbox is not None and bboxes is not None
    ):
        raise ValueError("Provide either bbox or bboxes, but not both")

    # Validate format
    if format not in ("geotiff", "png"):
        raise ValueError("Unsupported format. Supported: 'geotiff', 'png'")

    # Validate resolution
    if resolution not in ("low", "medium", "high"):
        raise ValueError(
            "Unsupported resolution. Supported: 'low', 'medium', 'high'"
        )

    dest_path = _ensure_dest(dest)

    result = DownloadResult(entries=[])

    def _process_one(b: Sequence[float]) -> None:
        min_lon, min_lat, max_lon, max_lat = _validate_bbox(b)
        # Split antimeridian into 1 or 2 ranges
        lon_ranges = _split_antimeridian(min_lon, max_lon)
        # For simplicity, one URL per longitude range covering the full latitude span
        for i, (lon_a, lon_b) in enumerate(lon_ranges):
            coverage = BoundingBox(
                minLon=lon_a, minLat=min_lat, maxLon=lon_b, maxLat=max_lat
            )
            # Build URL
            url = _build_url(
                lon_a, min_lat, lon_b, max_lat, format, resolution, provider
            )
            # Determine filename
            fname = _safe_filename(
                provider, format, (lon_a, min_lat, lon_b, max_lat)
            )
            dest_file = dest_path / fname
            # Reuse if skip and exists
            if dest_file.exists() and overwrite == "skip":
                size = dest_file.stat().st_size
                result.entries.append(
                    ManifestEntry(
                        path=str(dest_file),
                        format=format,
                        coverage=coverage,
                        size_bytes=size,
                        status="reused",
                    )
                )
                result.count_reused += 1
                continue
            # Download
            size = _download_stream(url, dest_file, overwrite=overwrite)
            result.entries.append(
                ManifestEntry(
                    path=str(dest_file),
                    format=format,
                    coverage=coverage,
                    size_bytes=size,
                    status="created",
                )
            )
            result.count_created += 1

    if bbox is not None:
        try:
            _process_one(bbox)
        except Exception as e:
            result.errors.append(f"bbox error: {e}")
            raise
        return result

    assert bboxes is not None
    for b in bboxes:
        try:
            _process_one(b)
        except Exception as e:
            result.errors.append(f"bbox {list(b)} error: {e}")
            # continue with next bbox
            continue
    return result


# === Phase 2: Foundational helpers ===


def _validate_bbox(b: Sequence[float]) -> Tuple[float, float, float, float]:
    if len(b) != 4:
        raise ValueError(
            "bbox must be a sequence of 4 numbers: [minLon, minLat, maxLon, maxLat]"
        )
    min_lon, min_lat, max_lon, max_lat = map(float, b)
    if not (-180.0 <= min_lon <= 180.0 and -180.0 <= max_lon <= 180.0):
        raise ValueError("longitude values must be in [-180, 180]")
    if not (-90.0 <= min_lat <= 90.0 and -90.0 <= max_lat <= 90.0):
        raise ValueError("latitude values must be in [-90, 90]")
    if min_lat >= max_lat:
        raise ValueError("minLat must be < maxLat")
    # Antimeridian allowed (min_lon may be > max_lon) handled by split helper
    return min_lon, min_lat, max_lon, max_lat


def _split_antimeridian(
    min_lon: float, max_lon: float
) -> List[Tuple[float, float]]:
    """Return 1 or 2 longitude ranges accounting for antimeridian crossing.

    If min_lon <= max_lon: returns [(min_lon, max_lon)]
    If min_lon > max_lon: returns [(min_lon, 180.0), (-180.0, max_lon)]
    """
    if min_lon <= max_lon:
        return [(min_lon, max_lon)]
    return [(min_lon, 180.0), (-180.0, max_lon)]


def _safe_filename(
    prefix: str, fmt: Format, rng: Tuple[float, float, float, float]
) -> str:
    min_lon, min_lat, max_lon, max_lat = rng
    ext = "tif" if fmt == "geotiff" else "png"
    # Keep predictable precision to avoid overly long names
    return f"{prefix}_{min_lon:.3f}_{min_lat:.3f}_{max_lon:.3f}_{max_lat:.3f}.{ext}"


def _ensure_dest(dest: str) -> Path:
    p = Path(dest)
    p.mkdir(parents=True, exist_ok=True)
    if not os.access(p, os.W_OK):
        raise PermissionError(f"Destination not writable: {dest}")
    return p


def _download_stream(
    url: str,
    dest_file: Path,
    *,
    timeout: float = 30.0,
    retries: int = 3,
    backoff: float = 0.5,
    overwrite: Overwrite = "skip",
) -> int:
    """Download a URL to dest_file atomically, streaming to avoid large buffers.

    Returns size in bytes. Reuses existing file when overwrite='skip'.
    """
    if dest_file.exists() and overwrite == "skip":
        return dest_file.stat().st_size

    tmp = dest_file.with_suffix(dest_file.suffix + ".part")
    attempt = 0
    while True:
        try:
            with requests.get(url, stream=True, timeout=timeout) as r:
                try:
                    r.raise_for_status()
                except Exception as http_err:
                    # include response status and a small portion of the body to help debugging
                    content_preview = None
                    try:
                        content_preview = r.text[:1024]
                    except Exception:
                        content_preview = "<unavailable>"
                    raise RuntimeError(
                        f"HTTP error while downloading {url}: {r.status_code} {r.reason}\nResponse preview: {content_preview}"
                    ) from http_err
                # Check content-type to ensure we're not saving an HTML error page
                ctype = (r.headers.get("Content-Type") or "").lower()
                if any(
                    t in ctype
                    for t in ["text/html", "text/plain", "application/json"]
                ):
                    preview = None
                    try:
                        preview = r.text[:1024]
                    except Exception:
                        preview = "<unavailable>"
                    raise RuntimeError(
                        f"Unexpected content-type {ctype} for {url}. Response preview: {preview}"
                    )
                tmp.parent.mkdir(parents=True, exist_ok=True)
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 64):
                        if chunk:
                            f.write(chunk)
            # Atomic replace
            tmp.replace(dest_file)
            return dest_file.stat().st_size
        except Exception:
            attempt += 1
            try:
                if tmp.exists():
                    tmp.unlink()
            except Exception:
                # Best-effort cleanup
                pass
            if attempt > retries:
                raise
            sleep(backoff * attempt)


def _map_resolution(res: Resolution) -> str:
    """Map named resolution to service-specific level.

    For now, names map directly to service levels to keep API simple.
    """
    mapping = {
        "low": "low",
        "medium": "medium",
        "high": "high",
    }
    return mapping[res]


def _build_url(
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
    fmt: Format,
    res: Resolution,
    provider: Provider,
) -> str:
    if provider == "gmrt":
        # GMRT GridServer (no API key). Supports GeoTIFF via west/east/south/north.
        if fmt != "geotiff":
            raise ValueError(
                "GMRT provider currently supports only 'geotiff' format"
            )
        return f"{GMRT_BASE_URL}?format=geotiff&west={min_lon}&east={max_lon}&south={min_lat}&north={max_lat}"
    if provider == "opentopo":
        # OpenTopography Global DEM API requires a dataset name and bounds.
        # Map our named resolution to a dataset. Defaults chosen for broad coverage.
        dataset = _opentopo_dataset_for(res)
        if fmt != "geotiff":
            raise ValueError(
                "OpenTopography provider only supports 'geotiff' format"
            )
        # Note: OpenTopography expects south, north, west, east
        url = (
            f"{OPENTOPO_BASE_URL}?demtype={dataset}&south={min_lat}&north={max_lat}&west={min_lon}&east={max_lon}"
            f"&outputFormat=GTiff"
        )
        api_key = os.getenv("OPENTOPO_API_KEY")
        if api_key:
            url += f"&API_Key={api_key}"
        return url
    raise ValueError(f"Unknown provider: {provider}")


def _opentopo_dataset_for(res: Resolution) -> str:
    """Map resolution names to OpenTopography dataset identifiers.

    - low -> SRTM15_PLUS (15 arc-second global topo-bathy)
    - medium -> SRTMGL3 (3 arc-second ~90 m global SRTM)
    - high -> SRTMGL1 (1 arc-second ~30 m; may be restricted in some regions)
    """
    mapping = {
        "low": "SRTM15_PLUS",
        "medium": "SRTMGL3",
        "high": "SRTMGL1",
    }
    return mapping[res]
