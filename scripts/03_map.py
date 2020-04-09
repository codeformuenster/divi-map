""" Scatter map. """

from pathlib import Path

import pandas as pd
import plotly
import plotly.express as px


# HOVERING EXAMPLE
# us_cities = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv"
# )
# fig = px.scatter_mapbox(
#     us_cities,
#     lat="lat",
#     lon="lon",
#     hover_name="City",
#     hover_data=["City"],
#     color_discrete_sequence=["green"],
#     zoom=3,
# )
# fig.update_layout(mapbox_style="carto-darkmatter")
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# plotly.offline.plot(fig, filename=str(Path("data/map_us.html")))

CSV = Path("data/processed/df_clean.csv")

hospitals = (
    pd.read_csv(str(CSV))
    .dropna(subset=["statusHighCare"])  # drop rows with NA in color column
    .filter(items=["id", "latitude", "longitude", "statusHighCare"])  # select columns
)

fig = px.scatter_mapbox(
    hospitals,
    lat="latitude",
    lon="longitude",
    hover_data=["id"],
    color="statusHighCare",
    color_discrete_sequence=["green", "yellow", "red"],
    zoom=5.2,
)
fig.update_layout(mapbox_style="carto-darkmatter")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# legend
fig.update_layout(legend_title='<b> Status Intensivstationen ("High Care") </b>')
fig.update_layout(
    legend=dict(
        x=0.01,
        y=0.98,
        traceorder="normal",
        font=dict(family="sans-serif", size=12, color="black"),
        bgcolor="LightSteelBlue",
        bordercolor="Black",
        borderwidth=2,
    )
)

plotly.offline.plot(fig, filename=str(Path("data/map.html")))
