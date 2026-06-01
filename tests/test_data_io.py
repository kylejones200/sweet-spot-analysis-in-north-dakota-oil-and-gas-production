import pandas as pd

from bakken_sweet_spot.data_io import prepare_panel_frame
from bakken_sweet_spot.sweet_spot import prepare_sweet_spot_frame


def test_prepare_panel_frame():
    df = pd.DataFrame(
        {
            "API_WELLNO": ["1", "1", "2"],
            "ReportDate": ["2020-01-01", "2020-02-01", "2020-01-01"],
            "Oil": [100, 200, 50],
            "Days": [30, 28, 31],
        }
    )
    panel = prepare_panel_frame(
        df,
        entity_col="API_WELLNO",
        time_col="ReportDate",
        dependent="Oil",
        regressor="Days",
    )
    assert panel.index.names == ["API_WELLNO", "ReportDate"]
    assert len(panel) == 3


def test_prepare_sweet_spot_from_report_date():
    df = pd.DataFrame(
        {
            "WellName": ["W1", "W1"],
            "ReportDate": ["2016-01-01", "2016-02-01"],
            "Oil": [10.0, 20.0],
            "Lat": [47.0, 47.0],
            "Long": [-103.0, -103.0],
        }
    )
    frame = prepare_sweet_spot_frame(df)
    assert "Cumulative_Oil" in frame.columns
    assert frame["Cumulative_Oil"].iloc[-1] == 30.0
