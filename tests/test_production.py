import pandas as pd

from bakken_sweet_spot.production import merge_well_stats, summarize_wells


def test_summarize_and_scale():
    df = pd.DataFrame(
        {
            "WellName": ["A", "A", "B"],
            "Oil": [10.0, 30.0, 5.0],
        }
    )
    stats = summarize_wells(df, name_col="WellName", value_col="Oil")
    enriched = merge_well_stats(df, stats, name_col="WellName")
    a_scaled = enriched.loc[enriched["WellName"] == "A", "local_scaled"].tolist()
    assert a_scaled == [10 / 30, 1.0]
    assert enriched.loc[enriched["WellName"] == "B", "local_scaled"].iloc[0] == 1.0
