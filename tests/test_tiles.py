"""Tests for pygmrt.tiles module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
import rasterio

from pygmrt.tiles import (
    BoundingBox,
    DownloadResult,
    ManifestEntry,
    download_tiles,
    get_path,
)
from pygmrt.tiles import (
    _build_url,
    _check_directory,
    _save_filename,
    _split_antimeridian,
    _validate_bbox,
)


class TestValidateBbox:
    """Tests for _validate_bbox function."""

    def test_valid_bbox(self):
        """Test valid bounding box."""
        west, south, east, north = _validate_bbox([10.0, 20.0, 30.0, 40.0])
        assert west == 10.0
        assert south == 20.0
        assert east == 30.0
        assert north == 40.0

    def test_bbox_wrong_length(self):
        """Test bbox with wrong number of elements."""
        with pytest.raises(ValueError, match="bbox must have shape"):
            _validate_bbox([10.0, 20.0, 30.0])

    def test_longitude_out_of_range(self):
        """Test bbox with longitude out of range."""
        with pytest.raises(ValueError, match="longitude values must be"):
            _validate_bbox([200.0, 20.0, 30.0, 40.0])

        with pytest.raises(ValueError, match="longitude values must be"):
            _validate_bbox([10.0, 20.0, -200.0, 40.0])

    def test_latitude_out_of_range(self):
        """Test bbox with latitude out of range."""
        with pytest.raises(ValueError, match="latitude values must be"):
            _validate_bbox([10.0, 100.0, 30.0, 40.0])

        with pytest.raises(ValueError, match="latitude values must be"):
            _validate_bbox([10.0, 20.0, 30.0, -100.0])

    def test_south_greater_than_north(self):
        """Test bbox where south >= north."""
        with pytest.raises(ValueError, match="south must be < north"):
            _validate_bbox([10.0, 40.0, 30.0, 20.0])

    def test_bbox_with_negative_values(self):
        """Test valid bbox with negative coordinates."""
        west, south, east, north = _validate_bbox(
            [-120.0, -50.0, -100.0, -30.0]
        )
        assert west == -120.0
        assert south == -50.0
        assert east == -100.0
        assert north == -30.0


class TestSplitAntimeridian:
    """Tests for _split_antimeridian function."""

    def test_no_crossing(self):
        """Test longitude range without antimeridian crossing."""
        result = _split_antimeridian(10.0, 50.0)
        assert result == [(10.0, 50.0)]

    def test_with_crossing(self):
        """Test longitude range with antimeridian crossing."""
        result = _split_antimeridian(170.0, -170.0)
        assert result == [(170.0, 180.0), (-180.0, -170.0)]

    def test_exactly_at_antimeridian(self):
        """Test longitude range exactly at antimeridian."""
        result = _split_antimeridian(180.0, -180.0)
        assert result == [(180.0, 180.0), (-180.0, -180.0)]

    def test_full_circle(self):
        """Test longitude range covering almost full circle."""
        result = _split_antimeridian(170.0, -170.0)
        assert len(result) == 2
        assert result[0] == (170.0, 180.0)
        assert result[1] == (-180.0, -170.0)


class TestSaveFilename:
    """Tests for _save_filename function."""

    def test_basic_filename(self):
        """Test basic filename generation."""
        filename = _save_filename("gmrt", (10.5, 20.5, 30.5, 40.5))
        assert filename == "gmrt_medium_10.500_20.500_30.500_40.500.tif"

    def test_filename_with_resolution(self):
        """Test filename with different resolutions."""
        filename_low = _save_filename(
            "gmrt", (10.0, 20.0, 30.0, 40.0), resolution="low"
        )
        filename_high = _save_filename(
            "gmrt", (10.0, 20.0, 30.0, 40.0), resolution="high"
        )

        assert "low" in filename_low
        assert "high" in filename_high
        assert filename_low != filename_high

    def test_filename_with_custom_extension(self):
        """Test filename with custom extension."""
        filename = _save_filename(
            "gmrt", (10.0, 20.0, 30.0, 40.0), extension="geotiff"
        )
        assert filename.endswith(".geotiff")

    def test_filename_with_negative_coords(self):
        """Test filename with negative coordinates."""
        filename = _save_filename("gmrt", (-120.5, -50.5, -100.5, -30.5))
        assert "-120.500" in filename
        assert "-50.500" in filename


class TestCheckDirectory:
    """Tests for _check_directory function."""

    def test_create_directory(self):
        """Test directory creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test_subdir"
            result = _check_directory(test_dir)
            assert result.exists()
            assert result.is_dir()

    def test_existing_directory(self):
        """Test with existing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = _check_directory(tmpdir)
            assert result.exists()
            assert result.is_dir()

    def test_nested_directory_creation(self):
        """Test creation of nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_dir = Path(tmpdir) / "level1" / "level2" / "level3"
            result = _check_directory(nested_dir)
            assert result.exists()
            assert result.is_dir()

    def test_string_path(self):
        """Test with string path instead of Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "string_dir")
            result = _check_directory(test_dir)
            assert isinstance(result, Path)
            assert result.exists()


class TestBuildUrl:
    """Tests for _build_url function."""

    def test_url_generation_medium(self):
        """Test URL generation with medium resolution."""
        url = _build_url(10.0, 20.0, 30.0, 40.0, "medium")
        assert "www.gmrt.org/services/GridServer" in url
        assert "format=geotiff" in url
        assert "resolution=med" in url

    def test_url_generation_low(self):
        """Test URL generation with low resolution."""
        url = _build_url(10.0, 20.0, 30.0, 40.0, "low")
        assert "www.gmrt.org/services/GridServer" in url

    def test_url_generation_high(self):
        """Test URL generation with high resolution."""
        url = _build_url(10.0, 20.0, 30.0, 40.0, "high")
        assert "www.gmrt.org/services/GridServer" in url

    def test_url_contains_bbox(self):
        """Test that URL contains bbox parameters."""
        url = _build_url(10.5, 20.5, 30.5, 40.5, "medium")
        assert "10.5" in url
        assert "20.5" in url
        assert "30.5" in url
        assert "40.5" in url


class TestDownloadTiles:
    """Tests for download_tiles function."""

    def test_missing_bbox(self):
        """Test download_tiles with missing bbox."""
        with pytest.raises(ValueError, match="Provide bbox"):
            download_tiles()

    def test_invalid_resolution(self):
        """Test download_tiles with invalid resolution."""
        with pytest.raises(ValueError, match="Supported resolutions"):
            download_tiles(bbox=[10.0, 20.0, 30.0, 40.0], resolution="ultra")

    @patch("pygmrt.tiles._download_stream")
    @patch("pygmrt.tiles.rasterio.open")
    def test_successful_download(self, mock_raster_open, mock_download):
        """Test successful tile download."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock rasterio dataset
            mock_dataset = MagicMock()
            mock_dataset.name = "test.tif"
            mock_dataset.crs = "EPSG:4326"
            mock_dataset.shape = (100, 100)
            mock_raster_open.return_value = mock_dataset

            # Download tiles
            result = download_tiles(
                bbox=[10.0, 20.0, 30.0, 40.0],
                save_directory=tmpdir,
                resolution="low",
            )

            assert result is not None
            mock_download.assert_called_once()

    @patch("pygmrt.tiles._download_stream")
    @patch("pygmrt.tiles.rasterio.open")
    def test_overwrite_parameter(self, mock_raster_open, mock_download):
        """Test overwrite parameter functionality."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_dataset = MagicMock()
            mock_raster_open.return_value = mock_dataset

            # Create an existing file
            save_path = Path(tmpdir)
            filename = _save_filename(
                "gmrt", (10.0, 20.0, 30.0, 40.0), resolution="low"
            )
            existing_file = save_path / filename
            existing_file.touch()

            # Download without overwrite - should not download
            download_tiles(
                bbox=[10.0, 20.0, 30.0, 40.0],
                save_directory=tmpdir,
                resolution="low",
                overwrite=False,
            )
            mock_download.assert_not_called()

    def test_invalid_bbox_in_download(self):
        """Test download_tiles with invalid bbox values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(RuntimeError):
                download_tiles(
                    bbox=[200.0, 20.0, 30.0, 40.0],
                    save_directory=tmpdir,
                )


class TestGetPath:
    """Tests for get_path function."""

    def test_get_path_with_created_entry(self):
        """Test get_path with a created entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = Path(tmpdir) / "test.tif"
            test_file.touch()

            # Create result with entry
            entry = ManifestEntry(
                path=str(test_file),
                coverage={"west": 0, "south": 0, "east": 1, "north": 1},
                size_bytes=100,
                status="created",
            )
            result = DownloadResult(entries=[entry])

            path = get_path(result)
            assert path == test_file

    def test_get_path_with_reused_entry(self):
        """Test get_path with a reused entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.tiff"
            test_file.touch()

            entry = ManifestEntry(
                path=str(test_file),
                coverage={"west": 0, "south": 0, "east": 1, "north": 1},
                size_bytes=100,
                status="reused",
            )
            result = DownloadResult(entries=[entry])

            path = get_path(result)
            assert path == test_file

    def test_get_path_no_valid_entry(self):
        """Test get_path with no valid entries."""
        result = DownloadResult(entries=[])

        with pytest.raises(RuntimeError, match="No GeoTIFF found"):
            get_path(result)

    def test_get_path_file_not_exists(self):
        """Test get_path when file doesn't exist."""
        entry = ManifestEntry(
            path="/nonexistent/file.tif",
            coverage={"west": 0, "south": 0, "east": 1, "north": 1},
            size_bytes=100,
            status="created",
        )
        result = DownloadResult(entries=[entry])

        with pytest.raises(RuntimeError, match="No GeoTIFF found"):
            get_path(result)


class TestIntegrationScenarios:
    """Integration tests for common usage scenarios."""

    @patch("pygmrt.tiles._download_stream")
    @patch("pygmrt.tiles.rasterio.open")
    def test_la_reunion_download(self, mock_raster_open, mock_download):
        """Test downloading La Réunion Island area."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_dataset = MagicMock()
            mock_dataset.name = "la_reunion.tif"
            mock_dataset.crs = "EPSG:4326"
            mock_raster_open.return_value = mock_dataset

            # La Réunion bbox
            result = download_tiles(
                bbox=[55.05, -21.5, 55.95, -20.7],
                save_directory=tmpdir,
                resolution="low",
            )

            assert result is not None
            mock_download.assert_called_once()

    @patch("pygmrt.tiles._download_stream")
    @patch("pygmrt.tiles.rasterio.open")
    def test_antimeridian_crossing(self, mock_raster_open, mock_download):
        """Test downloading area crossing the antimeridian."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_dataset = MagicMock()
            mock_raster_open.return_value = mock_dataset

            # Bbox crossing antimeridian
            result = download_tiles(
                bbox=[170.0, -10.0, -170.0, 10.0],
                save_directory=tmpdir,
                resolution="low",
            )

            assert result is not None

    @patch("pygmrt.tiles._download_stream")
    @patch("pygmrt.tiles.rasterio.open")
    def test_different_resolutions(self, mock_raster_open, mock_download):
        """Test downloading same area with different resolutions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_dataset = MagicMock()
            mock_raster_open.return_value = mock_dataset

            bbox = [10.0, 20.0, 30.0, 40.0]

            for resolution in ["low", "medium", "high"]:
                result = download_tiles(
                    bbox=bbox,
                    save_directory=tmpdir,
                    resolution=resolution,
                )
                assert result is not None
