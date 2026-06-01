# Sweet Spot Analysis in North Dakota Oil and Gas Production

Companion code for [`article.md`](article.md). Identifies high-performing Bakken areas using cumulative production, well-level summaries, and panel regressions with Driscoll–Kraay standard errors.

Published: 2025-02-12 · [Medium article](https://medium.com/@kyle-t-jones/sweet-spot-analysis-in-north-dakota-oil-and-gas-production-5358580431e9)

## Business context

Sweet spot analysis is an approach in oil and gas exploration that identifies areas with sustained high production potential. By understanding where wells perform best over time, operators can optimize future drilling locations, improve recovery rates, and enhance economic returns. Production varies significantly based on geology, completion techniques, and operational decisions across basins.

I wanted to find the most productive areas of North Dakota using cumulative production data since 2016.

I compiled well-level production data from the North Dakota Monthly Production Report. This dataset includes oil output, well locations, and monthly production figures since 2016. I used cumulative prod as the measure of well performance. That isn't perfect but it is useful for highlighting areas that sustain output over time.

## Project layout

```
├── article.md
├── config.yaml          # data paths, panel settings, output dirs
├── data/                # input CSV/XLSX (not committed — see data/README.md)
├── output/              # generated figures, tables, GIFs (gitignored)
├── src/bakken_sweet_spot/
├── notebooks/           # legacy Jupyter exports
├── tests/
└── main.py              # optional: python main.py panel
```

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```bash
uv sync
# Place north_dakota_production.csv in data/ (see data/README.md)

uv run bakken panel          # panel OLS + figures + animation
uv run bakken sweet-spot     # cumulative heatmap GIF (needs map extra)
uv sync --extra map
uv run bakken sweet-spot

uv run bakken production     # KDE + scaled production table (needs combinedfile.csv)
uv run bakken workbook       # merge Excel workbook (needs .xlsx + openpyxl)
uv sync --extra dev
uv run bakken workbook
```

### Commands

| Command | Description |
|---------|-------------|
| `bakken panel` | Entity fixed-effects panel of oil on days; SE comparison, sample-well plots, GIF |
| `bakken sweet-spot` | Monthly cumulative-oil heatmaps with basemap → GIF |
| `bakken production` | Lat/long KDE and per-well scaled production export |
| `bakken workbook` | Merge Bakken 2018 Excel sheets to one CSV |

### Outputs

| Command | Writes to |
|---------|-----------|
| `panel` | `output/figures/panel_*.png`, `output/animations/oil_production_animation.gif` |
| `sweet-spot` | `output/figures/heatmap_frames/`, `output/animations/cumulative_production_animation.gif` |
| `production` | `output/figures/lat_long_kde.png`, `output/tables/bakken_production_scaled.csv` |
| `workbook` | `output/tables/bakken_workbook_merged.csv` |

## Configuration

Edit [`config.yaml`](config.yaml) for file paths, column names, panel regression options, and output directories.

## Development

```bash
uv sync --extra dev
uv run pytest
uv run ruff check src tests
```

## Notebooks

Legacy notebooks live under `notebooks/`. Prefer the `bakken_sweet_spot` package and CLI above.

## Disclaimer

Educational/demo code only. Not financial, safety, or engineering advice. Use at your own risk. Verify results independently before any production or operational use.

## License

MIT — see [LICENSE](LICENSE).