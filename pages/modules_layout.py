from collections import OrderedDict

from dash import html

import pages.modules.translator as translator
from callbacks.constants import Constants


def get_modules_layout_dictionary():
    return OrderedDict({Constants.PAGE_LABELS["translator"]: "Generate ADB Translator"})


layout = html.Div(children=[translator.layout], className="px-0")
