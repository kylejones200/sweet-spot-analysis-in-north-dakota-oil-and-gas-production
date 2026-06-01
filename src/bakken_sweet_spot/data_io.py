"""Load production CSVs and the Bakken well workbook."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from bakken_sweet_spot.config import data_path


def load_production_csv(path: Path) -> pd.DataFrame:
    """Load North Dakota monthly production data."""
    if not path.exists():
        msg = f"Production file not found: {path}"
        raise FileNotFoundError(msg)
    df = pd.read_csv(path)
    if "ReportDate" in df.columns:
        df["ReportDate"] = pd.to_datetime(df["ReportDate"])
    return df


def load_production_from_config(config: dict[str, Any]) -> pd.DataFrame:
    return load_production_csv(data_path(config, "production_csv"))


def load_combined_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        msg = f"Combined production file not found: {path}"
        raise FileNotFoundError(msg)
    return pd.read_csv(path)


def load_workbook(path: Path) -> pd.ExcelFile:
    if not path.exists():
        msg = f"Workbook not found: {path}"
        raise FileNotFoundError(msg)
    return pd.ExcelFile(path)


def prepare_panel_frame(
    df: pd.DataFrame,
    *,
    entity_col: str,
    time_col: str,
    dependent: str,
    regressor: str,
) -> pd.DataFrame:
    """Set MultiIndex and coerce regressor / dependent for panel models."""
    panel = df.copy()
    panel[time_col] = pd.to_datetime(panel[time_col])
    panel[regressor] = pd.to_numeric(panel[regressor], errors="coerce")
    panel[dependent] = pd.to_numeric(panel[dependent], errors="coerce")
    panel = panel.dropna(subset=[regressor, dependent])
    return panel.set_index([entity_col, time_col])


def parse_source_file_dates(df: pd.DataFrame, source_col: str) -> pd.DataFrame:
    """Extract year/month from filenames like ``mpr_2016_03.csv``."""
    out = df.copy()
    out["Year"] = out[source_col].str.extract(r"(\d{4})").astype(int)
    out["Month"] = out[source_col].str.extract(r"_(\d{2})").astype(int)
    out["Date"] = pd.to_datetime(out[["Year", "Month"]].assign(day=1))
    return out
