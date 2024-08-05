from dash import Input, Output, State, html

from ..knowledge_graph.util import (
    get_relationships_with_node,
    make_graph,
    parse_add_node_queries,
    parse_add_relationship_queries,
    parse_delete_node_queries,
    parse_delete_relationship_queries,
    parse_edit_node_queries,
    parse_edit_relationship_queries,
)


def init_callback(app):
    @app.callback(
        Output("knowledge-graph", "elements", allow_duplicate=True),
        Input("edit-graph-submit", "n_clicks"),
        State("edit-node-text", "value"),
        State("add-node-text", "value"),
        State("delete-node-text", "value"),
        State("edit-relationship-text", "value"),
        State("add-relationship-text", "value"),
        State("delete-relationship-text", "value"),
        prevent_initial_call=True,
    )
    def edit_graph(
        edit_graph_submit,
        edit_node_text,
        add_node_text,
        delete_node_text,
        edit_relationship_text,
        add_relationship_text,
        delete_relationship_text,
    ):
        initial = False
        if edit_graph_submit == 0:
            initial = True

        else:
            if edit_node_text:
                parse_edit_node_queries(edit_node_text)

            if add_node_text:
                parse_add_node_queries(add_node_text)

            if delete_node_text:
                parse_delete_node_queries(delete_node_text)

            if edit_relationship_text:
                parse_edit_relationship_queries(edit_relationship_text)

            if add_relationship_text:
                parse_add_relationship_queries(add_relationship_text)

            if delete_relationship_text:
                parse_delete_relationship_queries(delete_relationship_text)

        graph = make_graph(initial)

        return graph[0]

    @app.callback(
        Output("node-info", "children"), Input("knowledge-graph", "tapNodeData")
    )
    def display_node_info(node_data):
        if not node_data:
            return "Click on a node to display information about it"

        relationships = get_relationships_with_node(node_data["id"])
        formatted_relationships = []
        for relationship in relationships:
            formatted_relationships += [html.Span(relationship), html.Br(), html.Br()]

        return [
            html.H4(node_data["id"], className="mb-2"),
            html.Span(html.B(node_data["type"])),
            html.Br(),
            html.Br(),
        ] + formatted_relationships

    @app.callback(
        Output("knowledge-graph", "elements", allow_duplicate=True),
        Input("filter-graph-text", "value"),
        prevent_initial_call=True,
    )
    def filter_graph(filter_graph_text):
        pass
