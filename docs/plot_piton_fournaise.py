"""
Piton de la Fournaise: High Resolution Volcano
==============================================

This example demonstrates downloading and visualizing high-resolution
topographic data for Piton de la Fournaise volcano on La Réunion.

Features:
- Synthetic volcanic topography
- Advanced hillshading techniques
- Custom colormaps for volcanic terrain
- High detail visualization

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource

# %%
# Generate Volcano Topography
# ---------------------------

# Piton de la Fournaise approximate location
bbox = [55.65, -21.35, 55.85, -21.15]
print(f"Volcano area: {bbox}")

# Create detailed synthetic volcano topography
np.random.seed(123)
width, height = 120, 100

x = np.linspace(bbox[0], bbox[2], width)
y = np.linspace(bbox[1], bbox[3], height)
X, Y = np.meshgrid(x, y)

# Create volcanic cone structure
center_x, center_y = 55.75, -21.25  # Approximate volcano center
dist = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)

# Multi-peak volcanic topography with crater
topo = 2500 * np.exp(-50 * dist**2)  # Main cone
topo += 800 * np.exp(
    -100 * (X - 55.73) ** 2 - 80 * (Y + 21.23) ** 2
)  # Secondary peak

# Add crater depression
crater_mask = dist < 0.02
topo[crater_mask] = topo[crater_mask] * 0.7

# Add realistic noise and lava flows
topo += 50 * np.random.randn(height, width)
topo = np.maximum(topo, 0)  # No negative elevations

print(f"Volcano topography: {width} x {height} pixels")
print(f"Peak elevation: {np.max(topo):.0f} m")

# %%
# Create Detailed Visualization
# -----------------------------

# Custom volcanic colormap
colors = ["#0066cc", "#006600", "#ffcc00", "#ff6600", "#cc3300", "#ffffff"]
n_bins = 256
cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
    "volcano", colors, N=n_bins
)

# Enhanced hillshading for volcanic features
sun = LightSource(azdeg=315, altdeg=45)
shade = sun.shade(topo, cmap=cmap, vert_exag=3, blend_mode="overlay")

# Create detailed plot
fig, ax = plt.subplots(figsize=(12, 9), dpi=120)

extent = [bbox[0], bbox[2], bbox[1], bbox[3]]
im = ax.imshow(shade, extent=extent, origin="lower")

# Styling
ax.set_xlabel("Longitude (°E)", fontsize=12)
ax.set_ylabel("Latitude (°S)", fontsize=12)
ax.set_title(
    "Piton de la Fournaise Volcano\nLa Réunion Island", fontsize=16, pad=20
)

# Add contour lines for elevation
levels = np.linspace(0, np.max(topo), 8)
contours = ax.contour(
    X, Y, topo, levels=levels, colors="black", alpha=0.3, linewidths=0.5
)

# Colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, np.max(topo)))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
cbar.set_label("Elevation (m)", fontsize=12)

plt.tight_layout()
plt.show()

# %%
# Volcano Statistics
# -----------------

print(f"\nVolcano Analysis:")
print(
    f"Area covered: {(bbox[2]-bbox[0]) * 111:.1f} x {(bbox[3]-bbox[1]) * 111:.1f} km"
)
print(f"Peak elevation: {np.max(topo):.0f} m")
print(f"Average slope: {np.mean(np.gradient(np.gradient(topo))):.3f}")
print(f"\nFor real GMRT data:")
print(f"src = download_tiles(bbox={bbox}, resolution='high')")
