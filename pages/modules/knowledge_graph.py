import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import dash_table, dcc, html

from callbacks.constants import Constants
from callbacks.knowledge_graph.util import convert_insights_to_df, make_graph

edit = [
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H4("Edit Nodes", className="mb-4"),
                    dbc.Label(
                        "Edit a node or its type",
                        className="mb-2",
                    ),
                    html.Br(),
                    dbc.Textarea(
                        id="edit-node-text",
                        value="NAME | Asian Infrastructure Investment Bank | AIIB\nTYPE | Asian Development Bank | MDB\nTYPE | Asian Infrastructure Investment Bank | MDB",
                        rows=6,
                    ),
                    html.Br(),
                    dbc.Label(
                        "Add a new node",
                        className="mb-2",
                    ),
                    html.Br(),
                    dbc.Textarea(
                        id="add-node-text", value="Multilateral development bank"
                    ),
                    html.Br(),
                    dbc.Label(
                        "Remove a node",
                        className="mb-2",
                    ),
                    html.Br(),
                    dbc.Textarea(
                        id="delete-node-text",
                        value="6 ADB Avenue, Mandaluyong, Metro Manila 1550, Philippines\n6 ADB Avenue, Mandaluyong, Metro Manila, Philippines",
                        rows=4,
                    ),
                ],
                md=6,
            ),
            dbc.Col(
                [
                    html.H4("Edit Relationships", className="mb-4"),
                    dbc.Label(
                        "Edit an existing relationship",
                        className="mb-2",
                    ),
                    html.Br(),
                    dbc.Textarea(
                        id="edit-relationship-text",
                        value="Asian Development Bank-Japan Scholarship Program (ADB-JSP) | 10 countries within the Region | LOCATED_IN | CATERS_TO",
                        rows=4,
                    ),
                    html.Br(),
                    dbc.Label(
                        "Add a new relationship",
                        className="mb-2",
                    ),
                    html.Br(),
                    dbc.Textarea(
                        id="add-relationship-text",
                        value="Asian Development Bank | Multilateral development bank | IS_A\nAsian Infrastructure Investment Bank | Multilateral development bank | IS_A",
                        rows=6,
                    ),
                    html.Br(),
                    dbc.Label(
                        "Remove a relationship",
                        className="mb-2",
                    ),
                    html.Br(),
                    dbc.Textarea(
                        id="delete-relationship-text",
                        value="Asian Development Bank | 3000 people | EMPLOYS",
                    ),
                ],
                md=6,
            ),
        ]
    ),
    html.Br(),
    dbc.Button(
        "Edit graph",
        id="edit-graph-submit",
        className="module-button",
        n_clicks=0,
        style={"width": "100%"},
    ),
]


graph, max_degree = make_graph(initial=True)

results = [
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            dbc.Button(
                                [
                                    html.I(className="bi bi-download me-2"),
                                    "Export View to CSV",
                                ],
                                id="lift-over-export-table",
                                n_clicks=0,
                                color="light",
                                size="sm",
                                className="table-button",
                            ),
                            dcc.Download(id="lift-over-download-df-to-csv"),
                            dbc.Button(
                                [
                                    html.I(className="bi bi-trash me-2"),
                                    "Remove Graph Filters",
                                ],
                                id="lift-over-reset-table",
                                color="light",
                                size="sm",
                                className="ms-3 table-button",
                            ),
                            dbc.Button(
                                [
                                    html.I(className="bi bi-arrow-clockwise me-2"),
                                    "Revert to Original Graph",
                                ],
                                id="lift-over-reset-table",
                                color="light",
                                size="sm",
                                className="ms-3 table-button",
                            ),
                        ],
                        style={"textAlign": "right"},
                    ),
                    html.Br(),
                    cyto.Cytoscape(
                        id="knowledge-graph",
                        layout={"name": "cose"},
                        style={"width": "100%", "height": "50vh"},
                        elements=graph,
                        stylesheet=[
                            {
                                "selector": "node",
                                "style": {
                                    "content": "data(name)",
                                    "text-halign": "center",
                                    "text-valign": "center",
                                    "width": f"mapData(degree, 0, {max_degree}, 50, 100)",
                                    "height": f"mapData(degree, 0, {max_degree}, 50, 100)",
                                    "padding": "10px",
                                    "font-size": "10px",
                                    "background-color": "data(bgcolor)",
                                    "color": "data(textcolor)",
                                },
                            },
                            {
                                "selector": "edge",
                                "style": {
                                    "content": "data(relationship)",
                                    "font-size": "7px",
                                    "curve-style": "bezier",
                                    "target-arrow-shape": "triangle",
                                },
                            },
                            {
                                "selector": "node:selected",
                                "style": {
                                    "border-width": "7px",
                                    "border-color": "black",
                                },
                            },
                            {
                                "selector": "edge:selected",
                                "style": {
                                    "width": "7px",
                                    "line-color": "black",
                                    "target-arrow-color": "black",
                                },
                            },
                        ],
                    ),
                ],
                className="w-100 pe-4",
            ),
        ],
        className="d-flex flex-row",
    ),
]


filter = html.Div(
    [
        html.H4("Filter Display", className="mb-4"),
        dbc.Label(
            "Enter criteria for filtering",
            className="mb-2",
        ),
        html.Br(),
        dbc.Textarea(
            id="filter-graph-text",
            value="NODE | Asian Development Bank\nTYPE | MDB\nREL | DELIVERED_SPEECH",
        ),
        html.Br(),
        dbc.Button(
            "Filter graph",
            id="sources-submit",
            className="module-button",
            n_clicks=0,
            style={"width": "100%"},
        ),
    ],
    className="p-3 module-intro",
)

info = html.Div(
    "Click on a node to display information about it",
    className="p-3 module-intro",
    id="node-info",
    style={"height": "22em", "overflowY": "scroll"},
)


insights = html.Div(
    [
        html.H4("Insights"),
        html.Br(),
        dash_table.DataTable(
            convert_insights_to_df().to_dict("records"),
            columns=[
                {"name": "Insight Group", "id": "Insight Group", "type": "text"},
                {"name": "Insight", "id": "Insight", "type": "text"},
            ],
            id="sources-results-table",
            style_cell={
                "whiteSpace": "pre-line",
                "height": "auto",
                "textAlign": "left",
            },
            sort_action="native",
            sort_mode="multi",
            filter_options={
                "case": "insensitive",
                "placeholder_text": "🔎︎ Search Column",
            },
            filter_action="native",
            page_action="native",
            page_size=15,
            cell_selectable=False,
            style_table={"overflowX": "auto"},
        ),
    ]
)


layout = html.Div(
    id={"type": "module-layout", "label": Constants.PAGE_LABELS["knowledge_graph"]},
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        edit,
                        className="module-intro p-3",
                    ),
                    md=3,
                ),
                dbc.Col(dcc.Loading(results), md=7),
                dbc.Col(
                    [filter, html.Br(), info],
                    md=2,
                ),
            ]
        ),
        html.Br(),
        insights,
    ],
)
