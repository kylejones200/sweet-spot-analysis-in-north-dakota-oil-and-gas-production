# Output

Generated artifacts are written here and are not committed to git.

| Subfolder | Contents |
|-----------|----------|
| `figures/` | PNG plots (standard errors, time series, KDE, heatmap frames) |
| `tables/` | CSV exports (merged workbook, scaled production) |
| `animations/` | GIFs (panel wells, cumulative sweet-spot map) |

Regenerate:

```bash
uv sync
uv run bakken panel
uv run bakken production      # needs data/combinedfile.csv
uv run bakken sweet-spot      # needs uv sync --extra map
uv run bakken workbook        # needs data/*.xlsx and uv sync --extra dev
```
