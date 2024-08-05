import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

import pages.modules_layout as modules_layout
from callbacks.constants import Constants

dash.register_page(__name__, path="/", name="ADB Translator")

submit_clear_buttons = dbc.Row(
    [
        dbc.Col(
            dbc.Button(
                "Translate Document",
                id="translate-submit",
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
        html.Div(
            [
                html.H5(
                    "Upload a document (PDF, Word document, Excel spreadsheet, etc.)"
                )
            ],
            className="mb-4",
        ),
        dcc.Upload(
            id="upload-document",
            children=html.Div(["Drag and Drop or ", html.A("Select a file")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
            },
        ),
        html.Br(id="break-1", style={"display": "none"}),
        html.Span(id="uploaded-filename", style={"display": "none"}),
        html.Span(id="true-uploaded-filename", style={"display": "none"}),
        html.Span(
            id="uploaded-successfully",
            children=" has been successfully uploaded!",
            style={"display": "none"},
        ),
        html.Br(id="break-2", style={"display": "none"}),
        html.Br(),
        dbc.Label(
            "Select an source language",
            className="mb-2",
        ),
        dcc.Dropdown(
            ["Detect automatically"] + list(Constants.LANGUAGES.keys()),
            id="source-language",
            className="mt-1",
            value="Detect automatically",
        ),
        html.Br(),
        dbc.Label(
            "Select a target language",
            className="mb-2",
        ),
        dcc.Dropdown(
            list(Constants.LANGUAGES.keys()),
            id="target-language",
            className="mt-1",
            value=["English"],
            multi=True,
        ),
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
            id="translate-results-container",
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
