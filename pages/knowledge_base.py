import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

import pages.modules_layout as modules_layout
from callbacks.constants import Constants

dash.register_page(__name__, path="/", name="Knowledge Graph")

submit_clear_buttons = dbc.Row(
    [
        dbc.Col(
            dbc.Button(
                "Generate Knowledge Graph",
                id="keyword-submit",
                n_clicks=0,
                className="keyword-button",
            ),
            xs=4,
            sm=4,
            md=2,
            lg=2,
            xl=2,
            xxl=2,
        ),
        dbc.Col(
            dbc.Button(
                "Reset All Analyses",
                color="danger",
                outline=True,
                id="keyword-reset",
                n_clicks=0,
                className="keyword-button",
            ),
            xs=4,
            sm=4,
            md=2,
            lg=2,
            xl=2,
            xxl=2,
            id="reset-analyses-container",
        ),
        dbc.Col(
            dbc.Button(
                "Clear Cache",
                id="keyword-clear-cache",
                color="danger",
                outline=True,
                n_clicks=0,
                className="keyword-button",
            ),
            xs=4,
            sm=4,
            md=2,
            lg=2,
            xl=2,
            xxl=2,
        ),
    ],
    className="pt-2",
)

keyword_input = dbc.Col(
    [
        html.Div([html.H5("Upload some documents")], className="mb-4"),
        dcc.Upload(
            id="upload-image",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Br(),
        dbc.Label(
            "Select an LLM",
            className="mb-2",
        ),
        dcc.Dropdown(Constants.LLMs, id="sources-llms", className="mt-1"),
        html.Br(),
        submit_clear_buttons,
    ]
)

layout = html.Div(
    [
        dbc.Row(
            keyword_input, className="px-5 pt-4 pb-5", id="keyword-input-container"
        ),
        html.Br(),
        html.Div(
            id="keyword-results-container",
            children=[
                html.Div(
                    id="modules-container",
                    children=[
                        dbc.Row(
                            children=modules_layout.layout,
                            id="page",
                            className="pe-5 py-2 pb-5",
                        )
                    ],
                ),
            ],
        ),
    ]
)
