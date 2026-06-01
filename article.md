---
author: "Kyle Jones"
date_published: "February 12, 2025"
date_exported_from_medium: "November 10, 2025"
canonical_link: "https://medium.com/@kyle-t-jones/sweet-spot-analysis-in-north-dakota-oil-and-gas-production-5358580431e9"
---

# Sweet Spot Analysis in North Dakota Oil and Gas Production Sweet spot analysis is an approach in oil and gas exploration that
identifies areas with sustained high production potential. By...

### Sweet Spot Analysis in North Dakota Oil and Gas Production
Sweet spot analysis is an approach in oil and gas exploration that identifies areas with sustained high production potential. By understanding where wells perform best over time, operators can optimize future drilling locations, improve recovery rates, and enhance economic returns. Production varies significantly based on geology, completion techniques, and operational decisions across basins.

I wanted to find the most productive areas of North Dakota using cumulative production data since 2016.


<figcaption>Source: Author</figcaption>


I compiled well-level production data from the North Dakota Monthly Production Report. This dataset includes oil output, well locations, and monthly production figures since 2016. I used cumulative prod as the measure of well performance. That isn't perfect but it is useful for highlighting areas that sustain output over time.

I overlayed a heatmap of cumulative oil production over time on a regular map to see which regions consistently produced at high levels. Each well is represented as a point, with color intensity reflecting its cumulative output from Jan 2016 to Nov 2024.

```python
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx  # For basemaps
import imageio.v2 as imageio  # Use imageio.v2 to avoid warnings
from PIL import Image
import os

# Load the production dataset
df = pd.read_csv("merged_mpr_data.csv")

# Extract date-related fields
df["Year"] = df["Source_File"].str.extract(r"(\d{4})").astype(int)
df["Month"] = df["Source_File"].str.extract(r"_(\d{2})").astype(int)
df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(day=1))

# Convert numeric fields
numeric_columns = ["Oil", "Wtr", "Days", "Runs", "Gas", "GasSold"]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")

# Keep relevant columns
df = df[["WellName", "Date", "Oil", "Lat", "Long"]]

# Remove rows without valid latitude/longitude data
df = df.dropna(subset=["Lat", "Long"])

# Compute cumulative oil production per well over time
df["Cumulative_Oil"] = df.groupby("WellName")["Oil"].cumsum()

# Get unique months for the animation
months = df["Date"].sort_values().unique()

# Create output folder
output_folder = "heatmap_frames"
os.makedirs(output_folder, exist_ok=True)

# Store file paths for animation
image_files = []

# Generate heatmaps over time
for month in months:
    df_month = df[df["Date"] == month]

    # Create a GeoDataFrame for mapping
    gdf = gpd.GeoDataFrame(df_month, geometry=gpd.points_from_xy(df_month["Long"], df_month["Lat"]))
    gdf = gdf.set_crs(epsg=4326).to_crs(epsg=3857)  # Convert to Web Mercator projection

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(f"Cumulative Oil Production - {month.strftime('%Y-%m')}", fontsize=14)
    
    gdf.plot(column="Cumulative_Oil", cmap="YlOrRd", markersize=10, alpha=0.75, legend=True, ax=ax)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)  # Add a basemap
    
    # Remove numbers from the outside of the map
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.axis("off") 
    # Save frame as an image
    frame_path = os.path.join(output_folder, f"production_{month.strftime('%Y_%m')}.png")
    plt.savefig(frame_path, dpi=150, bbox_inches="tight")
    plt.close()
    
    image_files.append(frame_path)

# Create an animated GIF

# Ensure all images exist before creating the GIF
image_files = [img for img in image_files if os.path.exists(img)]

# Load images
img_list = [Image.open(img) for img in image_files]

# Get the reference size (first image)
first_shape = img_list[0].size  # (width, height)

# Resize all images to the first image's size if needed
img_list = [img.resize(first_shape, Image.LANCZOS) if img.size != first_shape else img for img in img_list]

# Convert images to frames for GIF
gif_path = "cumulative_production_with_price_animation.gif"
img_list[0].save(
    gif_path, save_all=True, append_images=img_list[1:], duration=200, loop=0
)

print(f"Animation saved as {gif_path}")
```

This animation provides a dynamic, time-sensitive view of production performance. Traditional static maps only offer a snapshot, whereas our approach shows how different areas of North Dakota mature.
