# Implementation Plan: Python package to fetch and download GMRT tiles

**Branch**: `001-create-a-python` | **Date**: 2025-10-11 | **Spec**: /Users/seydoux/Desktop/pygmrt/specs/001-create-a-python/spec.md
**Input**: Feature specification from `/specs/001-create-a-python/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a minimal Python package with a single primary entry point that downloads GMRT tiles for a given
bounding box (and optional batch), supporting output formats GeoTIFF (default) and PNG, and named
resolution levels (low/medium/high). Keep file and function count low while delivering a complete flow
including validation, deterministic file naming, manifest return, and resumable runs (reuse existing
files when overwrite=False).

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11  
**Primary Dependencies**: requests (HTTP), typing-extensions (if needed); leverage server-provided tile
formats to avoid client-side raster processing.  
**Storage**: Filesystem only (write to destination folder).  
**Testing**: pytest + coverage; network-dependent integration test behind opt-in marker.  
**Target Platform**: macOS/Linux/Windows (any Python 3.11 runtime).  
**Project Type**: single package (library-only).  
**Performance Goals**: For a 2° x 2° bbox with defaults, median completion ≤ 10 seconds on standard
broadband; avoid >20% regression post-baseline.  
**Constraints**: Low memory footprint; avoid large in-memory buffers; stream downloads to disk.  
**Scale/Scope**: Single-module package, one public entry point; batch bboxes supported without parallel
execution initially (keep simple).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The plan includes these gates and passes with no waivers:

- Code Quality: Use ruff/black for lint/format; enable type hints and run mypy (strict on public API).
  Complexity kept minimal: one module, one public function, a couple small helpers.
- Testing Standards: Target >=80% coverage; unit tests for validation, naming, manifest; integration
  test for a small bbox (opt-in marker to avoid flaky CI). No merges on red tests.
- UX Consistency: Public API function `download_tiles(bbox, dest, format='geotiff', resolution='medium',
  overwrite=False, bboxes=None)` with clear parameter names and actionable errors.
- Performance Requirements: Budget as above; measure via wall-clock timing for a fixed bbox; ensure
  streaming downloads and reuse existing files to minimize unnecessary work.

## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

ios/ or android/
```
src/
└── pygmrt/
  └── tiles.py            # public API and minimal helpers

tests/
├── integration/
│   └── test_download_small_bbox.py  # opt-in network test
└── unit/
  ├── test_validation.py
  └── test_manifest_naming.py
```

**Structure Decision**: Single project with one package `pygmrt` and one module `tiles.py` to keep the
API surface minimal. Tests split into unit and integration; no CLI or additional layers at MVP.

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |

## Constitution Check (Post-Design)

- Code Quality: PASS — single module, typed API, lint/format configured in repo tooling.
- Testing Standards: PASS — unit + integration tests defined; coverage target set to >=80%.
- UX Consistency: PASS — stable parameter names; clear error policy; deterministic naming documented.
- Performance Requirements: PASS — budgets defined; streaming downloads; measurement approach captured
  in research.md.
