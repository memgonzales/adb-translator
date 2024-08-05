import dash_bootstrap_components as dbc
from dash import html


def navbar():
    return dbc.NavbarSimple(
        children=[],
        id="main-nav",
        brand=[
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src="assets/images/translator.png",
                            height="30px",
                            className="mx-auto",
                        ),
                        className="d-flex align-items-center",
                    ),
                    dbc.Col(dbc.NavbarBrand("ADB Translator", className="ms-3")),
                ],
                align="center",
                className="g-0",
            ),
        ],
        brand_href="/",
        color="#002069",
        dark=True,
        fluid=True,
        className="px-5",
    )
