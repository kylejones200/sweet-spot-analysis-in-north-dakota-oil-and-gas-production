"""Well-level production summaries and scaling."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def summarize_wells(
    df: pd.DataFrame,
    *,
    name_col: str = "WellName",
    value_col: str = "Oil",
) -> pd.DataFrame:
    """Aggregate monthly oil by well."""
    stats = (
        df.groupby(name_col, observed=False)[value_col]
        .agg(
            oil_sum="sum",
            oil_mean="mean",
            oil_std="std",
            oil_max="max",
        )
        .reset_index()
    )
    stats = stats.rename(columns={name_col: "Name"})
    return stats


def merge_well_stats(
    df: pd.DataFrame,
    stats: pd.DataFrame,
    *,
    name_col: str = "WellName",
) -> pd.DataFrame:
    """Attach per-well aggregates; adds ``local_scaled`` = Oil / well max."""
    working = df.copy()
    if name_col != "Name":
        working["Name"] = working[name_col].astype("category")
    merged = working.merge(stats, on="Name", how="left")
    merged["local_scaled"] = merged["Oil"] / merged["oil_max"]
    return merged


def export_production_table(df: pd.DataFrame, path: Path | str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    return path
