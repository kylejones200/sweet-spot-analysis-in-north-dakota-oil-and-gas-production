"""Exploratory spatial and time-series plots from combined production CSV."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from bakken_sweet_spot.config import data_path, figures_dir, section, tables_dir
from bakken_sweet_spot.data_io import load_combined_csv
from bakken_sweet_spot.production import export_production_table, merge_well_stats, summarize_wells


def plot_lat_long_kde(df: pd.DataFrame, *, lat_col: str, long_col: str, output_path: Path) -> Path:
    sns.set_theme()
    g = sns.jointplot(x=long_col, y=lat_col, data=df, kind="kde")
    g.figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(g.figure)
    return output_path


def plot_production_by_category(
    df: pd.DataFrame,
    *,
    date_col: str,
    category_col: str,
    value_col: str,
    output_path: Path,
    ylim: tuple[float, float] = (0, 1000),
) -> Path:
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot = df.pivot_table(index=date_col, columns=category_col, values=value_col)
    pivot.plot(ax=ax, legend=False, ylim=ylim)
    ax.set_title("Oil production by well category")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def run_production_exploration(config: dict[str, Any]) -> dict[str, Path]:
    """KDE map, category panel, and scaled production export."""
    prod_cfg = section(config, "production")
    name_col = prod_cfg.get("well_name_col", "WellName")
    oil_col = prod_cfg.get("oil_col", "Oil")
    lat_col = prod_cfg.get("lat_col", "Lat")
    long_col = prod_cfg.get("long_col", "Long")
    df = load_combined_csv(data_path(config, "combined_csv"))
    stats = summarize_wells(df, name_col=name_col, value_col=oil_col)
    enriched = merge_well_stats(df, stats, name_col=name_col)
    fig_root = figures_dir(config)
    table_root = tables_dir(config)
    paths: dict[str, Path] = {
        "lat_long_kde": plot_lat_long_kde(
            df, lat_col=lat_col, long_col=long_col, output_path=fig_root / "lat_long_kde.png"
        ),
        "production_table": export_production_table(
            enriched, table_root / "bakken_production_scaled.csv"
        ),
    }
    if "ReportDate" in df.columns and "API_WELLNO_category" in df.columns:
        paths["category_panel"] = plot_production_by_category(
            df,
            date_col="ReportDate",
            category_col="API_WELLNO_category",
            value_col=oil_col,
            output_path=fig_root / "oil_by_category.png",
        )

    return paths
