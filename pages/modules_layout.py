from collections import OrderedDict

from dash import html

import pages.modules.knowledge_graph as knowledge_graph
from callbacks.constants import Constants


def get_modules_layout_dictionary():
    return OrderedDict(
        {Constants.PAGE_LABELS["knowledge_graph"]: "Generate Knowledge Graph"}
    )


layout = html.Div(children=[knowledge_graph.layout], className="px-0")
