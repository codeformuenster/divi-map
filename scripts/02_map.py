""" Scatter map. """

from pathlib import Path

import pandas as pd
import plotly
import plotly.express as px


CSV = Path("data/intenstivregister.csv")

# us_cities = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv"
# )

hospitals = pd.read_csv(str(CSV))

hospitals["bettenStatus.statusHighCare"].unique()
hospitals = hospitals[~hospitals["bettenStatus.statusHighCare"].isnull()]


fig = px.scatter_mapbox(
    hospitals,
    lat="krankenhausStandort.position.latitude",
    lon="krankenhausStandort.position.longitude",
    # hover_name="krankenhausStandort.bezeichnung",
    hover_data=[
        "faelleCovidAktuell",
    ],
    color="bettenStatus.statusHighCare",
    color_discrete_sequence=["yellow", "green", "red"],
    zoom=5,
)
fig.update_layout(mapbox_style="carto-darkmatter")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

plotly.offline.plot(fig, filename=str(Path("data/map.html")))
