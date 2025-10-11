# Research: Python package to fetch and download GMRT tiles

## Unknowns and Decisions

### Resolution level mapping (named levels → service specifics)
- Decision: Use named levels: low, medium, high.
- Rationale: Simpler API for users; hides provider-specific details.
- Alternatives considered: Numeric grid spacing; tile zoom integers.

### Supported formats
- Decision: GeoTIFF (default) and PNG.
- Rationale: Balance geospatial fidelity (GeoTIFF) with broad compatibility (PNG).
- Alternatives considered: JPEG (lossy; excluded for data integrity).

### Antimeridian handling
- Decision: Auto-split into two longitudinal ranges and merge results.
- Rationale: Transparent UX; avoids user pre-processing.
- Alternatives considered: Reject input; treat as wrap without split.

## Dependencies and Best Practices

- HTTP downloads: Use streaming (requests) to avoid large in-memory buffers; set timeouts and retries with backoff.
- File integrity: Write to temp file then atomic rename; verify size/headers when available.
- Deterministic naming: Include format and tile/bbox indices; avoid collisions; document scheme.
- Resumability: If overwrite=skip, detect existing files and reuse; on error, remove partial temp files.
- Testing: Mock HTTP for unit tests; mark network tests as opt-in; assert manifest correctness.
- Performance measurement: Record wall-clock time for a small bbox and capture as baseline in CI artifacts when feasible.
