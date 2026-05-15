"""Generated from Jupyter notebook: Bakken heatmap

Magics and shell lines are commented out. Run with a normal Python interpreter."""


# --- code cell ---

import numpy as np
import pandas as pd
import seaborn as sns


def main():
    sns.set(color_codes=True)

    # %matplotlib inline  # Jupyter-only


    # --- code cell ---

    df = pd.read_csv("/Users/jnesnky/Desktop/Bakken/combinedfile.csv")


    # --- code cell ---

    df.head()


    # --- code cell ---

    sns.jointplot(x="Long", y="Lat", data=df, kind="kde")
    # --- code cell ---

    df.pivot_table(index="ReportDate", columns="API_WELLNO_category", values="Oil").plot(
        legend=False, ylim=(0, 1000)
    )


    # --- code cell ---

    df["Name"] = df["WellName"].astype("category")


    # --- code cell ---

    df.set_index(["Name", "ReportDate"], inplace=True)


    # --- duplicate code cell omitted (identical to earlier cell) ---


    # --- code cell ---

    grouped = df.groupby("Name")["Oil"]
    names = grouped.agg([np.sum, np.mean, np.std, np.max])


    # --- code cell ---

    type(names)


    # --- code cell ---

    df.reset_index(inplace=True)
    df_outer = pd.merge(df, names, on="Name", how="outer")


    # --- code cell ---

    df1 = df_outer.copy()


    # --- code cell ---

    df_outer["local_scaled"] = df_outer["Oil"] / df_outer["amax"]


    # --- code cell ---

    df_outer.set_index("ReportDate", inplace=True)


    # --- code cell ---

    df1.set_index(["Name", "ReportDate"], inplace=True)


    # --- code cell ---

    df1["Oil"].plot()


    # --- code cell ---

    df1.head()


    # --- code cell ---

    df1.to_csv("Bakken Production.csv")


if __name__ == "__main__":
    main()
