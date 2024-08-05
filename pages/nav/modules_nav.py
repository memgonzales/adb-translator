import dash_bootstrap_components as dbc

import pages.modules_layout as modules_layout


def nav():
    modules_layout_dict = modules_layout.get_modules_layout_dictionary()
    nav_list = [
        dbc.NavItem(
            dbc.NavLink(
                modules_layout,
                className="ps-4",
                id={"type": "modules-nav", "label": key},
                n_clicks=0,
            )
        )
        for key, modules_layout in modules_layout_dict.items()
    ]

    return dbc.Nav(
        [item for item in nav_list],
        vertical=True,
        pills=True,
        className="bg-light",
        id="modules-nav",
    )
