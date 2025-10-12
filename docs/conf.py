# Configuration file for the Sphinx documentation builder.
#
# Build with:
#   sphinx-build -b html docs docs/_build/html

import os
import sys
from datetime import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(".."))

project = "pygmrt"
author = "pygmrt maintainers"
current_year = datetime.now().year
copyright = f"{current_year}, {author}"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_autodoc_typehints",
]

autosummary_generate = True
napoleon_google_docstring = False
napoleon_numpy_docstring = True

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "linkify",
]

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "show_toc_level": 2,
    "navigation_depth": 2,
}
html_static_path = ["_static"]
templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]
