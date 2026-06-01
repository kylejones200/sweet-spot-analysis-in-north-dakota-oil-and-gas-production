"""Panel regression with Driscoll–Kraay and clustered standard errors."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from PIL import Image

from bakken_sweet_spot.config import animations_dir, figures_dir, section
from bakken_sweet_spot.data_io import load_production_from_config, prepare_panel_frame


def fit_panel_models(
    panel: pd.DataFrame,
    dependent: str,
    regressor: str,
    *,
    dk_bandwidth: int = 3,
) -> tuple[PanelOLS, PanelOLS, PanelOLS]:
    """Fit entity-fixed-effects models with default, DK, and clustered SEs."""
    x_matrix = sm.add_constant(panel[regressor])
    y = panel[dependent]
    model_default = PanelOLS(y, x_matrix, entity_effects=True).fit()
    model_dk = PanelOLS(y, x_matrix, entity_effects=True).fit(
        cov_type="kernel", kernel="bartlett", bandwidth=dk_bandwidth
    )
    model_cluster = PanelOLS(y, x_matrix, entity_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    return model_default, model_dk, model_cluster


def plot_standard_error_comparison(
    models: tuple[PanelOLS, PanelOLS, PanelOLS],
    *,
    labels: list[str] | None = None,
    output_path: Path,
) -> Path:
    """Bar chart comparing SE estimates across covariance specifications."""
    param_labels = labels or ["Intercept", "Days"]
    default_se, dk_se, cluster_se = (m.std_errors.to_numpy() for m in models)
    x = range(len(param_labels))
    width = 0.25
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(
        [i - width for i in x],
        default_se,
        width=width,
        label="Default SEs",
        color="black",
        alpha=0.7,
    )
    ax.bar(x, dk_se, width=width, label="Driscoll–Kraay SEs", color="gray", alpha=0.7)
    ax.bar(
        [i + width for i in x],
        cluster_se,
        width=width,
        label="Clustered SEs",
        color="steelblue",
        alpha=0.7,
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(param_labels)
    ax.set_ylabel("Standard error")
    ax.set_title("Panel OLS standard errors by covariance estimator")
    ax.legend()
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_sample_well_series(
    panel: pd.DataFrame,
    dependent: str,
    *,
    entity_col: str,
    n_wells: int,
    output_path: Path,
) -> Path:
    """Line plot of monthly oil for the first ``n_wells`` entities."""
    plt.rcParams.update(
        {"font.family": "serif", "axes.spines.top": False, "axes.spines.right": False}
    )
    wells = panel.index.get_level_values(entity_col).unique()[:n_wells]
    fig, ax = plt.subplots(figsize=(12, 6))
    for well in wells:
        well_data = panel.xs(well, level=entity_col)
        ax.plot(well_data.index, well_data[dependent], label=f"Well {well}", linewidth=1)

    ax.set_title("Monthly oil production over time")
    ax.legend(frameon=False)
    ax.grid(False)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_sample_well_boxplot(
    panel: pd.DataFrame,
    dependent: str,
    *,
    entity_col: str,
    n_wells: int,
    output_path: Path,
) -> Path:
    wells = panel.index.get_level_values(entity_col).unique()[:n_wells]
    series = [panel.xs(well, level=entity_col)[dependent].dropna() for well in wells]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(series, tick_labels=[str(w) for w in wells])
    ax.set_title("Monthly oil production distribution")
    ax.grid(False)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def build_production_animation(
    panel: pd.DataFrame,
    dependent: str,
    *,
    entity_col: str,
    time_col: str,
    n_wells: int,
    frames_dir: Path,
    gif_path: Path,
    duration_ms: int = 100,
) -> Path:
    """Progressive line chart GIF for sample wells."""
    plt.rcParams.update(
        {"font.family": "serif", "axes.spines.top": False, "axes.spines.right": False}
    )
    wells = panel.index.get_level_values(entity_col).unique()[:n_wells]
    dates = sorted(panel.index.get_level_values(time_col).unique())
    frames_dir.mkdir(parents=True, exist_ok=True)
    images: list[Image.Image] = []
    for i, date in enumerate(dates):
        fig, ax = plt.subplots(figsize=(12, 6))
        for well in wells:
            well_data = panel.xs(well, level=entity_col)
            well_data = well_data.loc[well_data.index <= date]
            ax.plot(well_data.index, well_data[dependent], label=f"Well {well}", linewidth=1)
        ax.set_title("Monthly oil production over time")
        ax.grid(False)
        frame_path = frames_dir / f"frame_{i:03d}.png"
        fig.savefig(frame_path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        images.append(Image.open(frame_path))

    gif_path.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=duration_ms, loop=0)
    return gif_path


def run_panel_pipeline(config: dict[str, Any]) -> dict[str, Path]:
    """Load data, fit models, and write figures under ``output/``."""
    panel_cfg = section(config, "panel")
    entity_col = panel_cfg.get("entity_col", "API_WELLNO")
    time_col = panel_cfg.get("time_col", "ReportDate")
    dependent = panel_cfg.get("dependent", "Oil")
    regressor = panel_cfg.get("regressor", "Days")
    dk_bandwidth = int(panel_cfg.get("dk_bandwidth", 3))
    n_wells = int(panel_cfg.get("sample_wells", 5))
    raw = load_production_from_config(config)
    panel = prepare_panel_frame(
        raw,
        entity_col=entity_col,
        time_col=time_col,
        dependent=dependent,
        regressor=regressor,
    )
    models = fit_panel_models(panel, dependent, regressor, dk_bandwidth=dk_bandwidth)
    fig_root = figures_dir(config)
    anim_root = animations_dir(config)
    paths = {
        "standard_errors": plot_standard_error_comparison(
            models, output_path=fig_root / "panel_standard_errors.png"
        ),
        "timeseries": plot_sample_well_series(
            panel,
            dependent,
            entity_col=entity_col,
            n_wells=n_wells,
            output_path=fig_root / "oil_production_timeseries.png",
        ),
        "boxplot": plot_sample_well_boxplot(
            panel,
            dependent,
            entity_col=entity_col,
            n_wells=n_wells,
            output_path=fig_root / "oil_production_boxplot.png",
        ),
        "animation": build_production_animation(
            panel,
            dependent,
            entity_col=entity_col,
            time_col=time_col,
            n_wells=n_wells,
            frames_dir=anim_root / "panel_frames",
            gif_path=anim_root / "oil_production_animation.gif",
        ),
    }
    return paths
