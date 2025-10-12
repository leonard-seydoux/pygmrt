SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR)

html:
	(cd .. && uv pip install -q ".[docs]")
	(cd .. && uv run sphinx-build -b html docs "docs/$(BUILDDIR)/html" $(SPHINXOPTS) $(O))
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."
