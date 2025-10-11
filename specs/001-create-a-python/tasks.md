---
description: "Task list for implementing pygmrt tile downloader"
---

# Tasks: Python package to fetch and download GMRT tiles

**Input**: Design documents from `/specs/001-create-a-python/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Per the constitution, tests are MANDATORY for new behavior and bug fixes. Include unit and
integration tests at minimum; add end-to-end tests when user journeys exist. Coverage MUST meet the
specified target (>=80%) and must not regress on changed files.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- Single project: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create source folders: `src/pygmrt/` and tests: `tests/unit/`, `tests/integration/`
- [X] T002 [P] Create package init: `src/pygmrt/__init__.py` exporting `__version__ = "0.1.0"`
- [X] T003 Add `pyproject.toml` with minimal package metadata, dependencies (`requests`), and tools (ruff, black, mypy, pytest)
- [X] T004 [P] Add `ruff` and `black` configuration (pyproject sections) and ensure formatting rules
- [X] T005 [P] Configure `mypy` (strict on public API) in `pyproject.toml`
- [X] T006 [P] Add `README.md` top-level with brief description and link to Quickstart
- [X] T007 Create module file: `src/pygmrt/tiles.py` (empty skeleton with docstring)
- [X] T008 Add `tests/__init__.py` and `tests/unit/__init__.py` to ensure package discovery

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core helpers and validation required by all stories

- [X] T009 Implement bbox validation helper in `src/pygmrt/tiles.py` (lon/lat ranges; min<max; allow antimeridian flag)
- [X] T010 [P] Implement antimeridian split helper in `src/pygmrt/tiles.py` returning 1–2 longitudinal ranges
- [X] T011 [P] Define deterministic filename scheme function in `src/pygmrt/tiles.py` (include format, bbox/tile indices)
- [X] T012 [P] Add manifest entry/result dataclasses in `src/pygmrt/tiles.py` per data-model.md
- [X] T013 Implement HTTP download stream helper in `src/pygmrt/tiles.py` with timeouts/retries and temp-file + atomic rename
- [X] T014 [P] Define GMRT base endpoint/URL template constant(s) in `src/pygmrt/tiles.py`
- [X] T015 Wire project lint/type/format checks via `pyproject.toml` (ensure `ruff`, `black`, `mypy`, `pytest` run locally)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Download tiles for a bounding box (Priority: P1) 🎯 MVP

**Goal**: User provides one bbox and destination; tiles are saved to disk using default format/resolution; return manifest

**Independent Test**: Provide a small bbox; verify files exist and manifest lists paths with coverage

### Tests for User Story 1

- [X] T016 [P] [US1] Unit test: bbox validation cases in `tests/unit/test_validation.py`
- [X] T017 [P] [US1] Unit test: filename/manifest correctness in `tests/unit/test_manifest_naming.py`
- [X] T018 [US1] Integration test (opt-in): small bbox download in `tests/integration/test_download_small_bbox.py` (mark `@pytest.mark.network`)

### Implementation for User Story 1

- [X] T019 [US1] Implement `download_tiles(bbox, dest, format="geotiff", resolution="medium", overwrite="skip", bboxes=None)` core happy path in `src/pygmrt/tiles.py`
- [X] T020 [P] [US1] Input validation + error messages (invalid bbox, unwritable dest) in `src/pygmrt/tiles.py`
- [X] T021 [P] [US1] Implement tile selection for bbox and call streaming downloader in `src/pygmrt/tiles.py`
- [X] T022 [US1] Build manifest entries and return `DownloadResult` in `src/pygmrt/tiles.py`
- [X] T023 [US1] Reuse existing files when `overwrite="skip"`; ensure no partial files remain on errors

**Checkpoint**: User Story 1 independently functional and testable (MVP)

---

## Phase 4: User Story 2 - Choose output format and resolution (Priority: P2)

**Goal**: Allow `format` (geotiff/png) and `resolution` (low/medium/high) selection; error on unsupported values

**Independent Test**: For a known bbox, verify outputs match selected format; verify resolution mapping invoked

### Tests for User Story 2

- [X] T024 [P] [US2] Unit test: format selection and unsupported error in `tests/unit/test_format_resolution.py`
- [X] T025 [P] [US2] Unit test: resolution mapping names→service levels in `tests/unit/test_format_resolution.py`

### Implementation for User Story 2

- [X] T026 [US2] Implement format handling (GeoTIFF default; PNG alternative) in `src/pygmrt/tiles.py`
- [X] T027 [P] [US2] Implement resolution mapping for low/medium/high in `src/pygmrt/tiles.py` and document mapping
- [X] T028 [US2] Validate unsupported options produce clear, actionable errors

**Checkpoint**: User Story 2 independently functional and testable

---

## Phase 5: User Story 3 - Batch requests (Priority: P3)

**Goal**: Accept multiple bboxes; process sequentially; produce combined manifest with per-bbox grouping

**Independent Test**: Provide two small bboxes; verify both sets saved and manifest groups entries by bbox

### Tests for User Story 3

- [X] T029 [P] [US3] Unit test: batch input handling and manifest grouping in `tests/unit/test_batch.py`
- [X] T030 [P] [US3] Unit test: invalid bbox among several → continue with per-bbox errors collected in `tests/unit/test_batch.py`

### Implementation for User Story 3

- [X] T031 [US3] Extend `download_tiles` to accept `bboxes` list argument (mutually exclusive with single `bbox`)
- [X] T032 [P] [US3] Iterate sequentially; collect manifests; include per-bbox results and errors without aborting all
- [X] T033 [US3] Document batch behavior and error aggregation in function docstring

**Checkpoint**: All user stories now independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T034 [P] Update `README.md` with usage examples and options; link to quickstart
- [ ] T035 [P] Performance validation against budgets across all stories; record baseline for small bbox
- [X] T036 [P] Add `pytest.ini` (or pyproject config) with `-m "not network"` default skip for network tests
- [ ] T037 Code cleanup and inline documentation for public API and error messages
- [X] T038 [P] Prepare minimal packaging metadata for distribution in `pyproject.toml` (name, version, description, classifiers)

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): No dependencies
- Foundational (Phase 2): Depends on Setup completion — BLOCKS all user stories
- User Stories (Phase 3+): Depend on Foundational; can proceed in priority order
- Polish (Final): Depends on desired stories being complete

### User Story Dependencies

- User Story 1 (P1): Can start after Foundational
- User Story 2 (P2): Can start after Foundational; independent of US1 except for shared helpers
- User Story 3 (P3): Can start after Foundational; independent of US1/US2; uses same core API

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implement core logic after tests
- Ensure story passes independent test before moving on

### Parallel Opportunities

- Setup tasks marked [P]
- Foundational tasks marked [P]
- Within a story, tasks in different files marked [P]

---

## Parallel Example: User Story 1

```bash
# Parallelizable tasks (different files)
Task: "Unit test: bbox validation cases in tests/unit/test_validation.py"
Task: "Unit test: filename/manifest correctness in tests/unit/test_manifest_naming.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup
2. Complete Foundational (CRITICAL - blocks all stories)
3. Complete User Story 1
4. STOP and VALIDATE: Run unit and (optionally) integration test; verify manifest

### Incremental Delivery

1. Add User Story 2 → Test independently → Document resolution/format mapping
2. Add User Story 3 → Test independently → Confirm batch manifest grouping

### Parallel Team Strategy

- Developer A: US1 tests and core implementation
- Developer B: Foundational helpers, resolution mapping, packaging metadata
- Developer C: Batch handling and documentation
