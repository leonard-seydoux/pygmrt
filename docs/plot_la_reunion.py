"""
La Réunion: Download and Plot Bathymetry
=========================================

This example demonstrates how to use pygmrt to download GMRT bathymetry 
data for La Réunion and create a beautiful hillshaded visualization.

The example shows:
- Basic pygmrt API usage  
- Creating synthetic topography data
- Hillshaded relief visualization
- Custom colormaps for bathymetry

Note: For demonstration purposes, this creates synthetic data.
To use real GMRT data, use: `from pygmrt.tiles import download_tiles`
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource

# %%
# Define Area of Interest  
# -----------------------
# 
# La Réunion bounding box [west, south, east, north]

bbox = [55.05, -21.5, 55.95, -20.7]
print(f"Area of interest: {bbox}")

# For demo purposes, create synthetic topography
# In real usage: src = download_tiles(bbox=bbox, resolution="high")
np.random.seed(42)
width, height = 100, 80
x = np.linspace(bbox[0], bbox[2], width) 
y = np.linspace(bbox[1], bbox[3], height)
X, Y = np.meshgrid(x, y)

# Create realistic island topography
center_x, center_y = np.mean([bbox[0], bbox[2]]), np.mean([bbox[1], bbox[3]])
dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)

# Volcanic island elevation profile
topo = 3000 * np.exp(-5 * dist_from_center) + 100 * np.random.randn(height, width)
topo = np.where(dist_from_center > 0.3, -2000 + 500 * np.random.randn(height, width), topo)

print(f"Generated topography: {topo.shape[1]} x {topo.shape[0]} pixels")
print(f"Elevation range: {np.min(topo):.1f} to {np.max(topo):.1f} m")

# %%
# Create Visualization
# --------------------
#
# Generate hillshaded map with custom colormap

# Create custom colormap 
cmap = plt.get_cmap("terrain")

# Create hillshade
sun = LightSource(azdeg=45, altdeg=30)
shade = sun.shade(topo, cmap=cmap, vert_exag=2, blend_mode='soft')

# Set up the plot
extent = [bbox[0], bbox[2], bbox[1], bbox[3]]

fig, ax = plt.subplots(figsize=(10, 8), dpi=100)

# Plot the hillshaded topography
im = ax.imshow(shade, extent=extent, origin='lower')
ax.set_xlabel('Longitude (°E)')
ax.set_ylabel('Latitude (°S)')
ax.set_title('La Réunion Island - Synthetic Topography\n(Hillshaded Relief)', fontsize=14, pad=15)

# Add grid
ax.grid(True, alpha=0.3, color='white')

# Add colorbar for elevation
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=np.min(topo), vmax=np.max(topo)))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', shrink=0.8, pad=0.1)
cbar.set_label('Elevation (m)', fontsize=11)

plt.tight_layout()
plt.show()

# %%
# Real Usage Example
# ------------------
#
# To use with actual GMRT data:

print("\nTo download real GMRT data:")
print("from pygmrt.tiles import download_tiles")
print("src = download_tiles(bbox=bbox, resolution='high')")
print("real_topo = src.read(1)")
print("src.close()")