import dash_bootstrap_components as dbc
from dash import html

from callbacks.constants import Constants

results = dbc.Row("Hello world")


layout = html.Div(
    id={"type": "module-layout", "label": Constants.PAGE_LABELS["translator"]},
    children=[results],
)
