"""Command-line entry points."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from bakken_sweet_spot import __version__
from bakken_sweet_spot.config import data_path, load_config, tables_dir
from bakken_sweet_spot.data_io import load_workbook
from bakken_sweet_spot.heatmap import run_production_exploration
from bakken_sweet_spot.panel import run_panel_pipeline
from bakken_sweet_spot.paths import DEFAULT_CONFIG_PATH
from bakken_sweet_spot.sweet_spot import run_sweet_spot_pipeline
from bakken_sweet_spot.workbook import build_merged_workbook

logger = logging.getLogger(__name__)


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s %(message)s")


def _print_paths(paths: dict[str, Path]) -> None:
    for name, path in paths.items():
        logger.info("%s → %s", name, path)


def cmd_panel(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config))
    paths = run_panel_pipeline(config)
    _print_paths(paths)
    return 0


def cmd_production(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config))
    paths = run_production_exploration(config)
    _print_paths(paths)
    return 0


def cmd_sweet_spot(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config))
    paths = run_sweet_spot_pipeline(config)
    _print_paths(paths)
    return 0


def cmd_workbook(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config))
    workbook_path = data_path(config, "workbook_xlsx")
    merged = build_merged_workbook(load_workbook(workbook_path))
    out = tables_dir(config) / "bakken_workbook_merged.csv"
    merged.to_csv(out, index=False)
    logger.info("Merged workbook → %s (%d rows, %d columns)", out, len(merged), len(merged.columns))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="North Dakota Bakken sweet-spot and production analysis",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "-c",
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to config.yaml",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser(
        "panel",
        help="Panel OLS with Driscoll–Kraay SEs and sample-well plots",
    ).set_defaults(func=cmd_panel)
    sub.add_parser(
        "production",
        help="Exploratory KDE and scaled production table",
    ).set_defaults(func=cmd_production)
    sub.add_parser(
        "sweet-spot",
        help="Cumulative production heatmap GIF (needs --extra map)",
    ).set_defaults(func=cmd_sweet_spot)
    sub.add_parser(
        "workbook",
        help="Merge Bakken Excel workbook sheets",
    ).set_defaults(func=cmd_workbook)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _configure_logging(args.verbose)
    try:
        return args.func(args)
    except (FileNotFoundError, KeyError, ImportError, ValueError) as exc:
        logger.error("%s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
