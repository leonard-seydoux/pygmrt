"""Tiles download module.

Minimal API to download Global Multi-Resolution Topography (GMRT) tiles for a
given bounding box or a batch of bounding boxes.

Notes
-----
- Main entry point: :func:`download_tiles`.
- Provider: GMRT GridServer only (no API key required).
- Formats supported: ``geotiff``. PNG is not currently supported by GMRT GridServer.
- Antimeridian crossing is handled by splitting longitude ranges automatically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
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

# Service endpoints
GMRT_BASE_URL = "https://www.gmrt.org/services/GridServer"

# Type aliases for clarity
Format = Literal["geotiff"]
Resolution = Literal["low", "medium", "high"]


class BoundingBox(TypedDict):
    west: float
    south: float
    east: float
    north: float


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
    dest: str,
    format: Format = "geotiff",
    resolution: Resolution = "medium",
    overwrite: bool = False,
) -> DownloadResult:
    """Download tiles for a single bounding box.

    Parameters
    ----------
    bbox : sequence of float, optional
        Bounding box in WGS84 degrees as ``[west, south, east, north]``.
        Must be provided.
    dest : str
        Destination directory path where files will be written. Created if
        needed.
    format : {"geotiff"}, default "geotiff"
        Output format. GMRT GridServer supports GeoTIFF here.
    resolution : {"low", "medium", "high"}, default "medium"
        Named resolution level; mapped internally to provider-specific datasets.
    overwrite : bool, default False
        If ``False``, reuse existing files. If ``True``, force re-download.
    provider : removed
        Single provider (GMRT) by design.

    Returns
    -------
    DownloadResult
        Manifest of written or reused files and counters of created/reused
        entries.

    Raises
    ------
    ValueError
        If invalid argument combinations or bbox values are provided.
    PermissionError
        If the destination directory is not writable.
    RuntimeError
        If download attempts ultimately fail.
    """
    # Validate bbox presence
    if bbox is None:
        raise ValueError("Provide bbox as [west, south, east, north]")

    # Validate format
    if format not in ("geotiff",):
        raise ValueError("Unsupported format. Supported: 'geotiff'")

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
                west=lon_a, south=min_lat, east=lon_b, north=max_lat
            )
            # Build URL
            url = _build_url(
                lon_a, min_lat, lon_b, max_lat, format, resolution
            )
            # Determine filename
            fname = _safe_filename(
                "gmrt", format, (lon_a, min_lat, lon_b, max_lat)
            )
            dest_file = dest_path / fname
            # Reuse if skip and exists
            if dest_file.exists() and not overwrite:
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

    try:
        _process_one(bbox)
    except Exception as e:
        result.errors.append(f"bbox error: {e}")
        raise
    return result


# === Phase 2: Foundational helpers ===


def _validate_bbox(b: Sequence[float]) -> Tuple[float, float, float, float]:
    """Validate a bounding box.

    Parameters
    ----------
    b : sequence of float
        Bounding box as ``[west, south, east, north]`` in degrees.

    Returns
    -------
    tuple of float
        The validated bbox as ``(west, south, east, north)`` with floats.

    Raises
    ------
    ValueError
    If the bbox length is not 4, latitude/longitude values are out of range,
    or ``south >= north``.
    """
    if len(b) != 4:
        raise ValueError(
            "bbox must be a sequence of 4 numbers: [west, south, east, north]"
        )
    min_lon, min_lat, max_lon, max_lat = map(float, b)
    if not (-180.0 <= min_lon <= 180.0 and -180.0 <= max_lon <= 180.0):
        raise ValueError("longitude values must be in [-180, 180]")
    if not (-90.0 <= min_lat <= 90.0 and -90.0 <= max_lat <= 90.0):
        raise ValueError("latitude values must be in [-90, 90]")
    if min_lat >= max_lat:
        raise ValueError("south must be < north")
    # Antimeridian allowed (min_lon may be > max_lon) handled by split helper
    return min_lon, min_lat, max_lon, max_lat


def _split_antimeridian(
    min_lon: float, max_lon: float
) -> List[Tuple[float, float]]:
    """Split longitude range if crossing the antimeridian.

    Parameters
    ----------
    min_lon, max_lon : float
        Input longitudes in degrees, each within [-180, 180].

    Returns
    -------
    list of tuple of float
        One or two ranges ``[(west, east), ...]`` depending on whether the
        interval crosses the antimeridian.
    """
    if min_lon <= max_lon:
        return [(min_lon, max_lon)]
    return [(min_lon, 180.0), (-180.0, max_lon)]


def _safe_filename(
    prefix: str, fmt: Format, rng: Tuple[float, float, float, float]
) -> str:
    """Create a deterministic and safe filename for a bbox and format.

    Parameters
    ----------
    prefix : str
        Filename prefix, typically the provider name.
    fmt : {"geotiff"}
        Output format determining the file extension.
    rng : tuple of float
        Bounding box as ``(west, south, east, north)``.

    Returns
    -------
    str
        Filename with fixed decimal precision and appropriate extension.
    """
    min_lon, min_lat, max_lon, max_lat = rng
    ext = "tif"
    # Keep predictable precision to avoid overly long names
    return f"{prefix}_{min_lon:.3f}_{min_lat:.3f}_{max_lon:.3f}_{max_lat:.3f}.{ext}"


def _ensure_dest(dest: str) -> Path:
    """Ensure destination directory exists and is writable.

    Parameters
    ----------
    dest : str
        Destination directory path.

    Returns
    -------
    pathlib.Path
        The destination path object.

    Raises
    ------
    PermissionError
        If the destination exists but is not writable.
    """
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
    overwrite: bool = False,
) -> int:
    """Download a URL to a file, atomically and with streaming.

    Parameters
    ----------
    url : str
        Source URL to fetch.
    dest_file : pathlib.Path
        Target file path to write. A temporary ``.part`` is used and atomically
        moved into place on completion.
    timeout : float, default 30.0
        Per-request timeout in seconds.
    retries : int, default 3
        Number of retry attempts on failures.
    backoff : float, default 0.5
        Linear backoff multiplier between retries, in seconds.
    overwrite : bool, default False
        If ``False``, reuse existing file. If ``True``, force re-download.

    Returns
    -------
    int
        Size of the written file in bytes.

    Raises
    ------
    RuntimeError
        When the HTTP response indicates an error or returns a text/JSON/HTML payload
        instead of a binary raster file.
    """
    if dest_file.exists() and not overwrite:
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
    """Map named resolution to service-specific levels.

    Notes
    -----
    Currently returns the same value (``low``, ``medium``, or ``high``) and is a
    placeholder for future provider-specific mapping.
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
) -> str:
    """Construct a provider-specific data URL for a bounding box.

    Parameters
    ----------
    min_lon, min_lat, max_lon, max_lat : float
        Bounding box edges in degrees.
    fmt : {"geotiff"}
        Desired output format.
    res : {"low", "medium", "high"}
        Named resolution level used for provider mapping.
    provider : removed
        Single provider (GMRT) by design.

    Returns
    -------
    str
        Fully qualified URL to request the data.

    Raises
    ------
    ValueError
        If unsupported format/provider combinations are requested or an unknown
        provider is supplied.
    """
    # GMRT GridServer (no API key). Supports GeoTIFF via west/east/south/north.
    if fmt != "geotiff":
        raise ValueError("GMRT supports only 'geotiff' format")
    return f"{GMRT_BASE_URL}?format=geotiff&west={min_lon}&east={max_lon}&south={min_lat}&north={max_lat}"


# OpenTopography support removed: single-provider (GMRT) by design.
