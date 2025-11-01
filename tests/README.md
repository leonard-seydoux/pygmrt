# Tests

This directory contains the test suite for the pygmrt package.

## Running Tests

Install test dependencies:
```bash
uv pip install pytest pytest-cov pytest-mock
```

Run all tests:
```bash
uv run pytest
```

Run with coverage:
```bash
uv run pytest --cov=pygmrt --cov-report=html
```

Run specific test file:
```bash
uv run pytest tests/test_tiles.py
```

Run specific test class or function:
```bash
uv run pytest tests/test_tiles.py::TestValidateBbox
uv run pytest tests/test_tiles.py::TestValidateBbox::test_valid_bbox
```

## Test Structure

- `conftest.py` - Shared fixtures and test configuration
- `test_tiles.py` - Tests for the tiles module

## Test Categories

Tests are organized into the following categories:

### Unit Tests
- `TestValidateBbox` - Tests for bounding box validation
- `TestSplitAntimeridian` - Tests for antimeridian handling
- `TestSaveFilename` - Tests for filename generation
- `TestCheckDirectory` - Tests for directory creation
- `TestBuildUrl` - Tests for URL construction

### Integration Tests
- `TestDownloadTiles` - Tests for the main download function
- `TestGetPath` - Tests for path extraction from results
- `TestIntegrationScenarios` - End-to-end workflow tests

## Coverage

The test suite aims for high coverage of:
- Input validation
- Edge cases (antimeridian, negative coordinates, etc.)
- Error handling
- File system operations
- URL generation
- Main API functions
