# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD  ?= uv run sphinx-build
SOURCEDIR    = .
BUILDDIR     = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Install documentation dependencies
install:
	uv add --group docs sphinx pydata-sphinx-theme myst-parser nbsphinx sphinx-gallery

# Clean build directory
clean:
	rm -rf $(BUILDDIR)

# Build HTML documentation
html:
	uv add --group docs sphinx pydata-sphinx-theme myst-parser nbsphinx sphinx-gallery
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build and serve documentation locally
serve: html
	@echo "Starting local server at http://localhost:8000"
	@cd $(BUILDDIR)/html && uv run python -m http.server 8000

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)