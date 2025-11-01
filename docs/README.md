# Documentation

This directory contains the documentation source files for the pygmrt package.

## Files

- `readme.ipynb` - Main documentation notebook with examples
- `build_readme.py` - Script to convert notebook to README.md
- `build_logo.py` - Script to generate the logo
- `Makefile` - Build automation

## Building Documentation

### Prerequisites

Ensure you have the project installed with uv:

```bash
cd ..
uv sync
```

### Build Commands

Build everything (logo + README):
```bash
make all
```

Build just the logo:
```bash
make logo
```

Build just the README:
```bash
make readme
```

Clean generated files:
```bash
make clean
```

### Manual Build

If you prefer to run the scripts directly:

```bash
# Generate logo
uv run python build_logo.py

# Convert notebook to README
uv run python build_readme.py
```

## How It Works

### Logo Generation (`build_logo.py`)

- Creates a simple topographic logo using matplotlib
- Outputs to `docs/images/logo.png`
- Uses hillshading for 3D effect

### README Generation (`build_readme.py`)

1. Converts `readme.ipynb` to markdown using jupyter nbconvert
2. Extracts SVG images from notebook output
3. Moves images to `docs/images/`
4. Updates image references to use GitHub raw URLs
5. Writes final README.md to repository root

The script automatically:
- Detects GitHub repository info from git config
- Handles antimeridian-crossing examples
- Preserves SVG format for high-quality plots
- Uses absolute GitHub URLs for PyPI compatibility

## Editing Documentation

1. Edit `readme.ipynb` in Jupyter or VS Code
2. Run cells to generate outputs
3. Save the notebook
4. Run `make readme` to regenerate README.md

### Important Notes

- Keep all code cells self-contained with imports
- Use `%config InlineBackend.figure_format = 'svg'` for SVG output
- Images will automatically be uploaded to docs/images/
- GitHub URLs ensure images work on PyPI

## Image Format

Images are saved as SVG for:
- High quality at any zoom level
- Small file size
- Better rendering on retina displays
- Professional appearance

## Troubleshooting

**Images not appearing:**
- Check that cells have been executed in the notebook
- Verify SVG output format is configured
- Run `make clean && make all` to rebuild everything

**Git errors:**
- Ensure you're in the repository root when running make
- Check that git remote is configured correctly

**Build errors:**
- Verify all dependencies are installed: `uv sync`
- Check that jupyter is available: `uv run jupyter --version`

## Dependencies

All dependencies are managed by uv and defined in `pyproject.toml`:
- jupyter (for nbconvert)
- matplotlib (for plots and logo)
- cartopy (for geographic projections)
- rasterio (for geospatial data)
- pycpt-city (for color palettes)
