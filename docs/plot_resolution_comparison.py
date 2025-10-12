"""
Resolution Comparison: GMRT Data Quality
========================================

This example compares different resolution settings for GMRT data
download, showing quality trade-offs between speed and detail.

Features:
- Multi-resolution synthetic comparison
- File size analysis
- Download time estimates
- Quality assessment

"""

import matplotlib.pyplot as plt
import numpy as np
import time

# %%
# Setup Comparison Area
# ---------------------

# Mid-Atlantic Ridge section
bbox = [-25.0, 35.0, -20.0, 40.0]
print(f"Test area: {bbox} (Mid-Atlantic Ridge)")

# Resolution settings
resolutions = ['high', 'medium', 'low']
res_values = [1, 4, 16]  # GMRT GridServer values
pixel_counts = [2000, 500, 125]  # Approximate pixels per side

print("\nResolution Comparison:")
for res, val, px in zip(resolutions, res_values, pixel_counts):
    print(f"{res:>6}: {val:>2} arc-seconds, ~{px:>4} x {px:>4} pixels")

# %%
# Generate Multi-Resolution Topography
# ------------------------------------

np.random.seed(42)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for i, (res, px_count) in enumerate(zip(resolutions, pixel_counts)):
    # Simulate different resolutions
    x = np.linspace(bbox[0], bbox[2], px_count)
    y = np.linspace(bbox[1], bbox[3], px_count)
    X, Y = np.meshgrid(x, y)
    
    # Create ridge topography at different resolutions
    ridge_topo = -3000 + 1000 * np.exp(-((X + 22.5)**2 + (Y - 37.5)**2) * 5)
    
    # Add detail based on resolution
    if res == 'high':
        detail = 200 * (np.sin(10 * X) * np.cos(8 * Y))
        noise_scale = 50
    elif res == 'medium': 
        detail = 100 * (np.sin(4 * X) * np.cos(3 * Y))
        noise_scale = 100
    else:  # low
        detail = 50 * (np.sin(2 * X) * np.cos(1.5 * Y))
        noise_scale = 150
        
    ridge_topo += detail
    ridge_topo += noise_scale * np.random.randn(px_count, px_count)
    
    # Plot
    ax = axes[i]
    extent = [bbox[0], bbox[2], bbox[1], bbox[3]]
    im = ax.imshow(ridge_topo, extent=extent, cmap='terrain', 
                   origin='lower', aspect='equal')
    
    ax.set_title(f'{res.title()} Resolution\n{px_count} x {px_count} pixels', 
                 fontsize=14)
    ax.set_xlabel('Longitude (°W)')
    if i == 0:
        ax.set_ylabel('Latitude (°N)')
        
    # Add colorbar
    plt.colorbar(im, ax=ax, label='Depth (m)' if i == 1 else '')

plt.suptitle('GMRT Resolution Comparison: Mid-Atlantic Ridge', fontsize=16, y=1.02)
plt.tight_layout()
plt.show()

# %%
# Performance Analysis
# -------------------

# Simulated download characteristics
file_sizes = [45.2, 2.8, 0.18]  # MB
download_times = [120, 8, 1.2]   # seconds
detail_scores = [95, 75, 40]     # quality score

print(f"\nPerformance Comparison:")
print(f"{'Resolution':<10} {'File Size':<12} {'Time':<10} {'Quality':<8}")
print(f"{'-'*10} {'-'*12} {'-'*10} {'-'*8}")

for res, size, time_est, quality in zip(resolutions, file_sizes, download_times, detail_scores):
    print(f"{res:<10} {size:>8.1f} MB   {time_est:>6.1f} s   {quality:>5}/100")

# Create comparison chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# File size comparison
bars1 = ax1.bar(resolutions, file_sizes, color=['#d62728', '#ff7f0e', '#2ca02c'])
ax1.set_ylabel('File Size (MB)')
ax1.set_title('Download File Size')
ax1.set_ylim(0, max(file_sizes) * 1.1)

for bar, size in zip(bars1, file_sizes):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{size:.1f} MB', ha='center', va='bottom')

# Quality vs Speed trade-off  
ax2.scatter(download_times, detail_scores, s=200, c=['red', 'orange', 'green'], alpha=0.7)
for i, res in enumerate(resolutions):
    ax2.annotate(res.title(), (download_times[i], detail_scores[i]), 
                xytext=(5, 5), textcoords='offset points')

ax2.set_xlabel('Download Time (seconds)')
ax2.set_ylabel('Detail Quality Score')
ax2.set_title('Quality vs Speed Trade-off')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %%
# Usage Recommendations
# --------------------

print(f"\nUsage Recommendations:")
print(f"• High resolution: Detailed studies, small areas (<50 km²)")
print(f"• Medium resolution: Regional analysis, medium areas (50-500 km²)")  
print(f"• Low resolution: Large-scale surveys, overview maps (>500 km²)")
print(f"\nExample usage:")
print(f"src = download_tiles(bbox=[-25, 35, -20, 40], resolution='medium')")