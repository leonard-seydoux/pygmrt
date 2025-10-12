# Installation

Option A — install directly from GitHub (no local clone required):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install "git+https://github.com/leonard-seydoux/pygmrt.git"
```

Option B — develop locally (editable install):

```bash
git clone https://github.com/leonard-seydoux/pygmrt.git
cd pygmrt
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Optional (for notebooks and plotting):

```bash
pip install cartopy rasterio matplotlib ipykernel
python -m ipykernel install --user --name pygmrt --display-name "Python (pygmrt)"
```
