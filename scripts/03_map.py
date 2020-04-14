""" Scatter map. """

from pathlib import Path

import jinja2
import pandas as pd
import plotly
import plotly.express as px

CSV = Path("data/processed/df_clean.csv")

hospitals = (
    pd.read_csv(str(CSV))
    .dropna(subset=["statusHighCare"])  # drop rows with NA in color column
    .filter(
        items=[
            "id",
            "meldezeitpunkt",
            "bezeichnung",
            "faelleCovidAktuell",
            "latitude",
            "longitude",
            "statusLowCare",
            "statusHighCare",
            "statusECMO",
        ]
    )
    .query("latitude <= 90")  # latitude <= max value of 90 degrees
    .query("longitude <= 180")  # longitude <= max value of 180 degrees
)

hospitals_latest = (
    hospitals.sort_values(by="meldezeitpunkt")
    .groupby("id")
    .tail(1)
    .reset_index()
    .sort_values(by="id")
)

fig = px.scatter_mapbox(
    hospitals_latest,
    lat="latitude",
    lon="longitude",
    hover_name="bezeichnung",
    hover_data=["faelleCovidAktuell", "statusLowCare", "statusHighCare", "statusECMO"],
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

fig_html = fig.to_html(
    include_plotlyjs=False,
    full_html=False,
    config={"locale": "de"},
)

with open('docs/index.j2') as f:
    t = jinja2.Template(f.read())
with open('docs/index.html', 'w') as f:
    f.write(t.render(plot=fig_html))
