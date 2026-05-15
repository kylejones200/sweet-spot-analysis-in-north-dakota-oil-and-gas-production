"""Generated from Jupyter notebook: 2025-04-04 time series panel regression with driscoll kraay using north dakota data

Magics and shell lines are commented out. Run with a normal Python interpreter."""



def main():
    # --- code cell ---

    data.columns


    # --- code cell ---

    import matplotlib.pyplot as plt
    import pandas as pd
    import statsmodels.api as sm
    from linearmodels.panel import PanelOLS

    # Load the dataset
    file_path = "/Users/kylejonespatricia/time_series/north_dakota_production.csv"
    data = pd.read_csv(file_path)

    # Convert ReportDate to datetime format
    data["ReportDate"] = pd.to_datetime(data["ReportDate"])

    # Set panel index (API_WELLNO as individual, ReportDate as time)
    data = data.set_index(["API_WELLNO", "ReportDate"])

    # Define independent variable(s)
    # Ensure Days is numeric
    data["Days"] = pd.to_numeric(data["Days"], errors="coerce")

    # Drop rows with missing values (optional)
    data = data.dropna(subset=["Days", "Oil"])

    # Add constant term for regression
    X_matrix = sm.add_constant(data["Days"])

    # Fit a panel regression model with entity effects using Driscoll-Kraay SEs
    panel_model = PanelOLS(data["Oil"], X_matrix, entity_effects=True).fit(
        cov_type="kernel", kernel="bartlett", bandwidth=3
    )

    # Print Driscoll-Kraay standard errors
    print("Driscoll-Kraay Standard Errors:")
    print(panel_model.std_errors)

    # Fit panel regression with clustered standard errors
    panel_model_clustered = PanelOLS(data["Oil"], X_matrix, entity_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )

    # Print clustered standard errors
    print("Clustered Standard Errors:")
    print(panel_model_clustered.std_errors)

    # Compare standard errors
    ols_se = panel_model.std_errors.to_numpy()
    dk_se = panel_model.std_errors.to_numpy()
    cluster_se = panel_model_clustered.std_errors.to_numpy()

    labels = ["Intercept", "Days"]

    # Plot standard errors
    plt.figure(figsize=(8, 5))
    plt.bar(labels, ols_se, color="black", alpha=0.7, label="OLS SEs")
    plt.bar(labels, dk_se, color="gray", alpha=0.5, label="Driscoll-Kraay SEs")
    plt.bar(labels, cluster_se, color="blue", alpha=0.3, label="Clustered SEs")
    plt.ylabel("Standard Error")
    plt.title("Comparison of OLS, Driscoll-Kraay, and Clustered Standard Errors")
    plt.legend()
    plt.savefig("panel_standard_errors.png")
    plt.show()


    # --- code cell ---

    # !pip install linearmodels  # Jupyter-only


    # --- code cell ---

    import matplotlib.pyplot as plt

    # Define the style
    plt.rcParams.update(
        {"font.family": "serif", "axes.spines.top": False, "axes.spines.right": False}
    )

    # Select 5 sample wells
    sample_wells = data.index.get_level_values("API_WELLNO").unique()[:5]

    # Time Series Plot for Selected Wells
    plt.figure(figsize=(12, 6))
    for well in sample_wells:
        well_data = data.xs(well, level="API_WELLNO")
        plt.plot(well_data.index, well_data["Oil"], label=f"Well {well}", linewidth=1)


    plt.title("Monthly Oil Production Over Time")
    plt.legend(frameon=False)

    plt.grid(False)
    plt.savefig("oil_production_timeseries.png")
    plt.show()

    # Boxplot of Production for Selected Wells
    plt.figure(figsize=(8, 5))
    subset = data.loc[sample_wells, :]
    plt.boxplot(
        [subset.xs(well, level="API_WELLNO")["Oil"].dropna() for well in sample_wells],
        labels=sample_wells,
    )


    plt.title("Monthly Oil Production Distribution")
    plt.grid(False)
    plt.savefig("oil_production_boxplot.png")
    plt.show()


    # --- code cell ---

    import os

    import matplotlib.pyplot as plt
    from PIL import Image

    # Define the style
    plt.rcParams.update(
        {"font.family": "serif", "axes.spines.top": False, "axes.spines.right": False}
    )

    # Select 5 sample wells
    sample_wells = data.index.get_level_values("API_WELLNO").unique()[:5]

    # Get the time index and range
    all_dates = sorted(data.index.get_level_values("ReportDate").unique())

    # Directory to save frames
    frame_dir = "frames"
    os.makedirs(frame_dir, exist_ok=True)

    # Create and save frames for the animation
    frames = []
    for i, date in enumerate(all_dates):
        plt.figure(figsize=(12, 6))

        for well in sample_wells:
            well_data = data.xs(well, level="API_WELLNO")
            well_data = well_data.loc[
                well_data.index <= date
            ]  # Show data up to the current date
            plt.plot(well_data.index, well_data["Oil"], label=f"Well {well}", linewidth=1)

        plt.title("Monthly Oil Production Over Time")

        plt.grid(False)

        # Save frame
        frame_path = f"{frame_dir}/frame_{i:03d}.png"
        plt.savefig(frame_path)
        plt.close()
        frames.append(Image.open(frame_path))

    # Save as GIF
    gif_path = "oil_production_animation.gif"
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=100, loop=0)

    print(f"GIF saved at: {gif_path}")


    # --- code cell ---

    data["WellName"].nunique()


if __name__ == "__main__":
    main()
