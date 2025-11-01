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
    """Convert notebook to markdown with SVG output."""
    print("Converting notebook to markdown (SVG format)...")

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
            os.path.abspath(README_PATH),
            '--ExtractOutputPreprocessor.extract_output_types={"image/svg+xml"}',
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print("✓ Notebook converted")
    return True


def fix_image_paths():
    """Fix image paths and move images to docs/images folder."""
    print("Fixing image paths...")

    # Create images directory if it doesn't exist
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Move any README_*.svg files from root to docs/images/
    import glob

    for svg_file in glob.glob("README_*.svg"):
        target = os.path.join(IMAGES_DIR, os.path.basename(svg_file))
        os.rename(svg_file, target)
        print(f"  Moved {svg_file} -> {target}")

    with open(README_PATH, "r") as f:
        content = f.read()

    # Replace absolute paths with relative paths
    # Pattern: ![svg](/absolute/path/README_X_Y.svg) -> ![svg](docs/images/README_X_Y.svg)
    content = re.sub(
        r"!\[(.*?)\]\(/[^\)]*/(README_\d+_\d+\.svg)\)",
        r"![\1](docs/images/\2)",
        content,
    )

    # Replace any local README_X_Y.svg references with docs/images/
    content = re.sub(
        r"!\[(.*?)\]\((README_\d+_\d+\.svg)\)",
        r"![\1](docs/images/\2)",
        content,
    )

    with open(README_PATH, "w") as f:
        f.write(content)

    # Count SVG image references
    svg_refs = re.findall(r"!\[.*?\]\(docs/images/.*?\.svg\)", content)

    if svg_refs:
        print(f"✓ Fixed {len(svg_refs)} SVG image path(s)")
    else:
        print("⚠ No SVG images found")

    return len(svg_refs) > 0


def main():
    """Main build process."""
    # Make sure we're in the repository root
    if not os.path.exists(DOCS_DIR):
        print(
            f"❌ Error: {DOCS_DIR} directory not found. Run this script from the repository root."
        )
        return 1

    if convert_notebook():
        fix_image_paths()
        print("\n✅ README.md built successfully!")
        print(f"📦 SVG images saved in {IMAGES_DIR}/")
    else:
        print("\n❌ Build failed")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
