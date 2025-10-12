# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "pygmrt"
copyright = "2025, pygmrt contributors"
author = "pygmrt contributors"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "nbsphinx",
    "sphinx_gallery.gen_gallery",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

# -- Theme options -----------------------------------------------------------

html_theme_options = {
    "github_url": "https://github.com/leonard-seydoux/pygmrt",
    "use_edit_page_button": True,
    "show_toc_level": 2,
    "navbar_align": "left",
    "navbar_center": ["navbar-nav"],
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version"],
}

html_context = {
    "github_user": "leonard-seydoux",
    "github_repo": "pygmrt",
    "github_version": "main",
    "doc_path": "docs",
}

# -- MyST options -----------------------------------------------------------

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "linkify",
    "strikethrough",
    "substitution",
    "tasklist",
]

# -- Autodoc options --------------------------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# -- Autosummary options ----------------------------------------------------

autosummary_generate = True

# -- NBSphinx options -------------------------------------------------------

nbsphinx_execute = "never"  # Don't execute notebooks during build
nbsphinx_allow_errors = True

# -- Sphinx Gallery options ------------------------------------------------

sphinx_gallery_conf = {
    "examples_dirs": ".",  # Current directory contains example scripts
    "gallery_dirs": "gallery",  # Output directory for gallery
    "filename_pattern": "/plot_",  # Match files starting with 'plot_'
    "ignore_pattern": r"__init__\.py|conf\.py",
    "plot_gallery": True,  # Execute examples to generate thumbnails
    "download_all_examples": False,
    "show_memory": False,
    "expected_failing_examples": [],
    "matplotlib_animations": False,
    "reference_url": {
        "pygmrt": None,  # The module is local
    },
}

# -- Napoleon options -------------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
