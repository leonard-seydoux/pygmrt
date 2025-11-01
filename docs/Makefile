.PHONY: all logo readme clean help

# Default target
all: logo readme

# Build the logo
logo:
	@echo "\nBuilding logo..."
	@cd .. && uv run python docs/build_logo.py

# Build README and images from notebook
readme:
	@echo "\nBuilding README and images from notebook..."
	@cd .. && uv run python docs/build_readme.py

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f images/logo.png
	@rm -f images/README_*.svg
	@rm -f ../README.md
	@echo "Cleaned"

# Show help
help:
	@echo "Available targets:"
	@echo "  make all     - Build logo and README (default)"
	@echo "  make logo    - Build logo only"
	@echo "  make readme  - Build README and images only"
	@echo "  make clean   - Remove generated files"
	@echo "  make help    - Show this help message"
