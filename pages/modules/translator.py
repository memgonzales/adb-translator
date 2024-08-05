import dash_bootstrap_components as dbc
from dash import dcc, html

from callbacks.constants import Constants

results = dbc.Row(
    [html.Span("Download the results here: "), html.Span(id="results-link")]
)


layout = html.Div(
    id={"type": "module-layout", "label": Constants.PAGE_LABELS["translator"]},
    children=[dcc.Loading(results)],
)
