"""Generated from Jupyter notebook: bakken workbook

Magics and shell lines are commented out. Run with a normal Python interpreter."""


# --- code cell ---

import pandas as pd


def main():
    # --- code cell ---

    df = pd.ExcelFile(r"C:\Users\ktjone1\Downloads\Bakken2018 Excel Well Workbook_2.xlsx")


    # --- code cell ---


    # --- code cell ---

    h = df.parse(0)


    # --- code cell ---

    h = h.merge(t, left_on="UWI", right_on="UWI", how="outer")


    # --- code cell ---

    t = df.parse("Formation")


    # --- code cell ---

    h.describe()


    # --- code cell ---

    list(h)


    # --- code cell ---

    test1 = [
        "UWI",
        "Operator Name",
        "Current Operator Name",
        "Lease Name",
        "Well Num",
        "OS Indicator",
        "Hole Direction",
        "Final Status",
        "Current Status",
        "Basin",
        "Basin Code",
        "Sub Basin",
        "Sub Basin Code",
        "Play Name",
        "Play Type",
        "Permit Date",
        "Depth Total Driller",
        "Depth Total Logger",
        "Depth True Vertical",
        "Depth Whipstock",
        "Class Initial Name",
        "Class Initial Code",
        "Class Final Name",
        "Class Final Code",
        "Status Final Code",
        "Formation Projected Name",
        "Depth Total Projected",
        "Formation at TD Name",
        "PRODFit Formation at TD Name",
        "Formation Producing Name",
        "PRODFit Top Formation Producing Name",
        "PRODFit Base Formation Producing Name",
        "Elevation Reference Value",
        "Elevation Reference Datum",
        "Ground Elevation",
        "Date First Spud",
        "Date Spud",
        "Date Completion",
        "Date Rig Release",
        "Date First Report",
        "Date Last Activity",
        "Depth Water Value",
        "Depth Water Datum",
        "Surface Latitude",
        "Surface Longitude",
        "Surface LL Source",
        "BH Latitude",
        "BH Longitude",
        "BH LL Source",
        "Activity Code",
        "Source_y",
        "Num Frac Stages",
        "Stages Avail",
        "Num Treatment Records",
        "Proppant - Sand (lbs)",
        "Proppant - Resin Coated Sand (lbs)",
        "Proppant - Ceramic (lbs)",
        "Proppant - Resin Coated Ceramic (lbs)",
        "Proppant - Sand, Ceramic (lbs)",
        "Proppant - Sand, Resin Coated Ceramic (lbs)",
        "Proppant - Sand, Ceramic, Resin Coated Sand (lbs)",
        "Proppant - Sand, Ceramic, Resin Coated Ceramic (lbs)",
        "Proppant - Sand, Resin Coated Sand, Ceramic, Resin Coated Ceramic (lbs)",
        "Proppant - Bauxite (lbs)",
        "Proppant - Walnut (lbs)",
        "Proppant - Marble (lbs)",
        "Proppant - Gravel (lbs)",
        "Proppant - Sand, Bauxite Ceramic (lbs)",
        "Proppant - Other (lbs)",
        "Total Proppant (lbs)",
        "Fluid/Water (Gals)",
        "Fluid - Slick Water (Gals)",
        "Fluid - Salt Water (Gals)",
        "Fluid - Foam (Gals)",
        "Fluid - Oil (Gals)",
        "Fluid - Potassium Chloride (Gals)",
        "Fluid - Surfactant (Gals)",
        "Fluid - Emulsion (Gals)",
        "N2/CO2 Gas (Gals)",
        "Acid (Gals)",
        "Gel/x-link (Gals)",
        "Fluid - Explosive (Gals)",
        "Fluid - Other (Gals)",
        "Total Fluid (gals)",
        "Total Proppant (lbs.) / Total Fluid (gal)",
        "Top Source",
        "Interpreter",
        "Code",
        "Name",
        "Depth Top",
        "Depth Top UOM",
        "Base Depth",
        "Base Depth UOM",
    ]


    # --- code cell ---

    g = h[test1]


    # --- code cell ---

    g.head()


    # --- code cell ---

    i = df.parse("Completion")
    g = g.merge(i, left_on="UWI", right_on="UWI", how="outer")


    # --- code cell ---

    list(g)


    # --- code cell ---

    e = [
        "UWI",
        "Operator Name",
        "Current Operator Name",
        "Lease Name",
        "Well Num",
        "OS Indicator",
        "Hole Direction",
        "Final Status",
        "Current Status",
        "Basin",
        "Basin Code",
        "Sub Basin",
        "Sub Basin Code",
        "Play Name",
        "Play Type",
        "Permit Date",
        "Depth Total Driller",
        "Depth Total Logger",
        "Depth True Vertical",
        "Depth Whipstock",
        "Class Initial Name",
        "Class Initial Code",
        "Class Final Name",
        "Class Final Code",
        "Status Final Code",
        "Formation Projected Name",
        "Depth Total Projected",
        "Formation at TD Name",
        "PRODFit Formation at TD Name",
        "Formation Producing Name",
        "PRODFit Top Formation Producing Name",
        "PRODFit Base Formation Producing Name",
        "Elevation Reference Value",
        "Elevation Reference Datum",
        "Ground Elevation",
        "Date First Spud",
        "Date Spud",
        "Date Completion",
        "Date Rig Release",
        "Date First Report",
        "Date Last Activity",
        "Depth Water Value",
        "Depth Water Datum",
        "Surface Latitude",
        "Surface Longitude",
        "Surface LL Source",
        "BH Latitude",
        "BH Longitude",
        "BH LL Source",
        "Activity Code",
        "Source_y",
        "Num Frac Stages",
        "Stages Avail",
        "Num Treatment Records",
        "Proppant - Sand (lbs)",
        "Proppant - Resin Coated Sand (lbs)",
        "Proppant - Ceramic (lbs)",
        "Proppant - Resin Coated Ceramic (lbs)",
        "Proppant - Sand, Ceramic (lbs)",
        "Proppant - Sand, Resin Coated Ceramic (lbs)",
        "Proppant - Sand, Ceramic, Resin Coated Sand (lbs)",
        "Proppant - Sand, Ceramic, Resin Coated Ceramic (lbs)",
        "Proppant - Sand, Resin Coated Sand, Ceramic, Resin Coated Ceramic (lbs)",
        "Proppant - Bauxite (lbs)",
        "Proppant - Walnut (lbs)",
        "Proppant - Marble (lbs)",
        "Proppant - Gravel (lbs)",
        "Proppant - Sand, Bauxite Ceramic (lbs)",
        "Proppant - Other (lbs)",
        "Total Proppant (lbs)",
        "Fluid/Water (Gals)",
        "Fluid - Slick Water (Gals)",
        "Fluid - Salt Water (Gals)",
        "Fluid - Foam (Gals)",
        "Fluid - Oil (Gals)",
        "Fluid - Potassium Chloride (Gals)",
        "Fluid - Surfactant (Gals)",
        "Fluid - Emulsion (Gals)",
        "N2/CO2 Gas (Gals)",
        "Acid (Gals)",
        "Gel/x-link (Gals)",
        "Fluid - Explosive (Gals)",
        "Fluid - Other (Gals)",
        "Total Fluid (gals)",
        "Total Proppant (lbs.) / Total Fluid (gal)",
        "Top Source",
        "Interpreter",
        "Code",
        "Name",
        "Depth Top_x",
        "Depth Top UOM_x",
        "Base Depth",
        "Base Depth UOM",
        "Source_x",
        "Test Type",
        "Pressure Obs Number",
        "Fluid Type",
        "BH Pressure Obs Number",
        "Date",
        "Formation Top Name_x",
        "Formation Base Name_x",
        "Depth Top_y",
        "Depth Base_x",
        "PRODFit Top Formation",
        "PRODFit Base Formation",
        "Pressure Flowing Tubing",
        "Pressure Flowing Casing",
        "Pressure Shutin Tubing",
        "Pressure Shutin Casing",
        "Bottom Hole Run Depth",
        "Pressure Bottom Hole",
        "Source_y",
        "Number",
        "Formation Top Name_y",
        "Formation Base Name_y",
        "Depth Top",
        "Depth Top UOM_y",
        "Depth Base_y",
        "Depth Base UOM",
        "Type",
        "Method",
    ]


    # --- code cell ---

    g = g[e]


    # --- code cell ---

    g.describe()


    # --- code cell ---

    g.UWI.value_counts()


if __name__ == "__main__":
    main()
