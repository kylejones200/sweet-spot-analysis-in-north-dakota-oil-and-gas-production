# Data

Place input files here (not committed). Update paths in [`config.yaml`](../config.yaml) if you use different names.

| File | Used by | Source |
|------|---------|--------|
| `north_dakota_production.csv` | `bakken panel`, `bakken sweet-spot` | [North Dakota Industrial Commission](https://www.dmr.nd.gov/oilgas/) monthly production reports |
| `combinedfile.csv` | `bakken production` | Legacy combined export from exploratory notebooks |
| `Bakken2018_Excel_Well_Workbook.xlsx` | `bakken workbook` | Bakken 2018 Excel Well Workbook (IHS / state well header export) |

**Minimum columns for panel / sweet-spot pipelines**

- `API_WELLNO`, `ReportDate`, `Oil`, `Days` (panel regression)
- `WellName`, `Lat`, `Long`, `Oil`, and either `Source_File` or `ReportDate` (sweet-spot maps)

Example layout after download:

```
data/
├── north_dakota_production.csv
├── combinedfile.csv          # optional
└── Bakken2018_Excel_Well_Workbook.xlsx  # optional
```
