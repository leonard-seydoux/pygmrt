#!/usr/bin/env python3
"""
Build README.md from readme.ipynb with GitHub URLs for images.
Run this from the repository root directory.
"""
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

# GitHub repository info
GITHUB_USER = "leonard-seydoux"
GITHUB_REPO = "pygmrt"
GITHUB_BRANCH = "main"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}"

# Paths
DOCS_DIR = "docs"
NOTEBOOK_PATH = os.path.join(DOCS_DIR, "readme.ipynb")
README_PATH = "README.md"
IMAGES_DIR = os.path.join(DOCS_DIR, "images")


def parse_vscode_notebook():
    """Parse VSCode XML notebook format and convert to markdown."""
    print("Parsing VSCode notebook...")

    try:
        # Read the notebook file
        with open("README.ipynb", "r") as f:
            content = f.read()

        # Parse cells from VSCode XML format
        markdown_content = []
        lines = content.split("\n")

        in_cell = False
        cell_content = []
        cell_language = None

        for line in lines:
            # Detect cell start
            if "<VSCode.Cell" in line:
                in_cell = True
                # Extract language
                if 'language="markdown"' in line:
                    cell_language = "markdown"
                elif 'language="python"' in line:
                    cell_language = "python"
                continue

            # Detect cell end
            if "</VSCode.Cell>" in line:
                if cell_content:
                    if cell_language == "markdown":
                        # Add markdown directly
                        markdown_content.append("\n".join(cell_content))
                    elif cell_language == "python":
                        # Add code block
                        markdown_content.append("```python")
                        markdown_content.append("\n".join(cell_content))
                        markdown_content.append("```")
                    markdown_content.append("")  # Empty line between cells

                # Reset for next cell
                in_cell = False
                cell_content = []
                cell_language = None
                continue

            # Collect cell content
            if in_cell:
                cell_content.append(line)

        # Write to README.md
        with open("README.md", "w") as f:
            f.write("\n".join(markdown_content))

        print("✓ Notebook converted")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def convert_notebook():
    """Convert notebook to markdown."""
    print("Converting notebook to markdown...")

    # Convert without executing (uses existing cell outputs with SVG format)
    result = subprocess.run(
        [
            "uv",
            "run",
            "jupyter",
            "nbconvert",
            "--to",
            "markdown",
            NOTEBOOK_PATH,
            "--output",
            "README",
            "--output-dir",
            ".",
            '--ExtractOutputPreprocessor.extract_output_types={"image/svg+xml"}',
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print("✓ Notebook converted")

    # Now manually embed the images
    embed_images_in_readme()

    return True


def embed_images_in_readme():
    """Embed image files as base64 data URIs in the README."""
    import base64
    import glob

    with open(README_PATH, "r") as f:
        content = f.read()

    # Find all SVG files in README_files/ directory
    svg_files = glob.glob("README_files/*.svg")

    if not svg_files:
        print("  No SVG files found to embed")
        return

    for svg_file in svg_files:
        # Read SVG file
        with open(svg_file, "rb") as f:
            svg_data = f.read()

        # Convert to base64
        b64_data = base64.b64encode(svg_data).decode("utf-8")
        data_uri = f"data:image/svg+xml;base64,{b64_data}"

        # Replace file reference with data URI
        # Pattern: ![svg](README_files/README_X_Y.svg)
        relative_path = svg_file.replace(
            "\\", "/"
        )  # Normalize path separators
        content = content.replace(f"]({relative_path})", f"]({data_uri})")
        print(f"  Embedded {svg_file}")

    with open(README_PATH, "w") as f:
        f.write(content)

    print("✓ Images embedded as data URIs")


def check_embedded_images():
    """Check if images are embedded in the README."""
    print("Checking embedded images...")

    with open(README_PATH, "r") as f:
        content = f.read()

    # Count embedded SVG images (data URIs)
    embedded_svg = content.count("data:image/svg+xml;base64,")

    # Clean up any leftover files/directories
    import glob
    import shutil

    # Remove any README_*.svg files that might have been created
    for svg_file in glob.glob("README_*.svg"):
        os.remove(svg_file)
        print(f"  Removed leftover {svg_file}")

    # Remove README_files directory if it exists
    if os.path.exists("README_files"):
        shutil.rmtree("README_files")
        print("  Removed README_files/ directory")

    if embedded_svg > 0:
        print(f"✓ Found {embedded_svg} embedded SVG image(s)")
        return True
    else:
        print("⚠ No embedded images found")
        return False


def main():
    """Main build process."""
    # Make sure we're in the repository root
    if not os.path.exists(DOCS_DIR):
        print(
            f"❌ Error: {DOCS_DIR} directory not found. Run this script from the repository root."
        )
        return 1

    if convert_notebook():
        check_embedded_images()
        print("\n✅ README.md built successfully!")
        print("📦 Images are embedded as base64 data URIs (self-contained)")
    else:
        print("\n❌ Build failed")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
