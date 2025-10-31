#!/usr/bin/env python3
"""
Build README.md from README.ipynb with GitHub URLs for images.
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


def parse_vscode_notebook():
    """Parse VSCode XML notebook format and convert to markdown."""
    print("Parsing VSCode notebook...")
    
    try:
        # Read the notebook file
        with open("README.ipynb", "r") as f:
            content = f.read()
        
        # Parse cells from VSCode XML format
        markdown_content = []
        lines = content.split('\n')
        
        in_cell = False
        cell_content = []
        cell_language = None
        
        for line in lines:
            # Detect cell start
            if '<VSCode.Cell' in line:
                in_cell = True
                # Extract language
                if 'language="markdown"' in line:
                    cell_language = 'markdown'
                elif 'language="python"' in line:
                    cell_language = 'python'
                continue
            
            # Detect cell end
            if '</VSCode.Cell>' in line:
                if cell_content:
                    if cell_language == 'markdown':
                        # Add markdown directly
                        markdown_content.append('\n'.join(cell_content))
                    elif cell_language == 'python':
                        # Add code block
                        markdown_content.append('```python')
                        markdown_content.append('\n'.join(cell_content))
                        markdown_content.append('```')
                    markdown_content.append('')  # Empty line between cells
                
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
            f.write('\n'.join(markdown_content))
        
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
            "readme.ipynb",
            "--output",
            "README.md",
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


def check_images():
    """Check if SVG images were generated."""
    print("Checking generated images...")

    with open("README.md", "r") as f:
        content = f.read()

    # Count SVG image references
    import re
    svg_refs = re.findall(r'!\[.*?\]\(README_files/.*?\.svg\)', content)
    
    if svg_refs:
        print(f"✓ Found {len(svg_refs)} SVG image(s) in README_files/")
    else:
        print("⚠ No SVG images found")
    
    return len(svg_refs) > 0


def main():
    """Main build process."""
    if convert_notebook():
        check_images()
        print("\n✅ README.md built successfully!")
        print("📦 SVG images saved in README_files/ directory")
    else:
        print("\n❌ Build failed")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
