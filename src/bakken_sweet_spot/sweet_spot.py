"""Cumulative production sweet-spot heatmaps (article pipeline)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from bakken_sweet_spot.config import animations_dir, data_path, figures_dir, section
from bakken_sweet_spot.data_io import load_production_csv, parse_source_file_dates


def prepare_sweet_spot_frame(
    df: pd.DataFrame,
    *,
    source_col: str = "Source_File",
    well_col: str = "WellName",
    oil_col: str = "Oil",
    lat_col: str = "Lat",
    long_col: str = "Long",
) -> pd.DataFrame:
    """Parse dates, coerce numerics, and compute cumulative oil by well."""
    if source_col in df.columns:
        frame = parse_source_file_dates(df, source_col)
    elif "ReportDate" in df.columns:
        frame = df.copy()
        frame["Date"] = pd.to_datetime(frame["ReportDate"])
    else:
        msg = "Expected Source_File or ReportDate for time indexing"
        raise ValueError(msg)

    for col in [oil_col, "Wtr", "Days", "Runs", "Gas", "GasSold"]:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")

    frame = frame[[well_col, "Date", oil_col, lat_col, long_col]].dropna(subset=[lat_col, long_col])
    frame["Cumulative_Oil"] = frame.groupby(well_col, observed=False)[oil_col].cumsum()
    return frame


def _require_geospatial() -> tuple[Any, Any]:
    try:
        import contextily as ctx
        import geopandas as gpd
    except ImportError as exc:
        msg = "Sweet-spot maps require optional deps: uv sync --extra map"
        raise ImportError(msg) from exc
    return gpd, ctx


def build_cumulative_heatmap_gif(
    frame: pd.DataFrame,
    *,
    well_col: str,
    lat_col: str,
    long_col: str,
    value_col: str = "Cumulative_Oil",
    frames_dir: Path,
    gif_path: Path,
    duration_ms: int = 200,
    dpi: int = 150,
) -> Path:
    """Monthly cumulative-oil maps with basemap, saved as GIF."""
    from PIL import Image

    gpd, ctx = _require_geospatial()

    frames_dir.mkdir(parents=True, exist_ok=True)
    months = frame["Date"].sort_values().unique()
    image_files: list[Path] = []

    for month in months:
        month_df = frame[frame["Date"] == month]
        gdf = gpd.GeoDataFrame(
            month_df,
            geometry=gpd.points_from_xy(month_df[long_col], month_df[lat_col]),
        )
        gdf = gdf.set_crs(epsg=4326).to_crs(epsg=3857)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(f"Cumulative oil production — {pd.Timestamp(month).strftime('%Y-%m')}")
        gdf.plot(
            column=value_col,
            cmap="YlOrRd",
            markersize=10,
            alpha=0.75,
            legend=True,
            ax=ax,
        )
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis("off")

        frame_path = frames_dir / f"production_{pd.Timestamp(month).strftime('%Y_%m')}.png"
        fig.savefig(frame_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        image_files.append(frame_path)

    images = [Image.open(path) for path in image_files if path.exists()]
    if not images:
        msg = "No heatmap frames were written"
        raise RuntimeError(msg)

    size = images[0].size
    resized = [img.resize(size, Image.LANCZOS) if img.size != size else img for img in images]
    gif_path.parent.mkdir(parents=True, exist_ok=True)
    resized[0].save(
        gif_path, save_all=True, append_images=resized[1:], duration=duration_ms, loop=0
    )
    return gif_path


def run_sweet_spot_pipeline(config: dict[str, Any]) -> dict[str, Path]:
    """Build cumulative production animation from configured production CSV."""
    sweet_cfg = section(config, "sweet_spot")
    prod_cfg = section(config, "production")

    path = data_path(config, "production_csv")
    raw = load_production_csv(path)
    frame = prepare_sweet_spot_frame(
        raw,
        source_col=sweet_cfg.get("source_file_col", "Source_File"),
        well_col=prod_cfg.get("well_name_col", "WellName"),
        oil_col=prod_cfg.get("oil_col", "Oil"),
        lat_col=prod_cfg.get("lat_col", "Lat"),
        long_col=prod_cfg.get("long_col", "Long"),
    )

    anim_root = animations_dir(config)
    return {
        "cumulative_gif": build_cumulative_heatmap_gif(
            frame,
            well_col=prod_cfg.get("well_name_col", "WellName"),
            lat_col=prod_cfg.get("lat_col", "Lat"),
            long_col=prod_cfg.get("long_col", "Long"),
            frames_dir=figures_dir(config) / "heatmap_frames",
            gif_path=anim_root / "cumulative_production_animation.gif",
            duration_ms=int(sweet_cfg.get("animation_duration_ms", 200)),
            dpi=int(sweet_cfg.get("figure_dpi", 150)),
        ),
    }
