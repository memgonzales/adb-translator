import dash
import dash_bootstrap_components as dbc
from flask import Flask, send_from_directory

import callbacks.translator.callbacks
import pages.nav.main_nav as main_nav
from callbacks.constants import Constants

server = Flask(__name__, static_folder="static")
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],
    server=server,
    title="ADB Translator",
    update_title="Loading...",
    meta_tags=[
        {"name": "viewport", "content": "width=1024"}
    ],  # Same desktop and mobile views
)

disclaimer = dbc.Row(
    dbc.Col(
        "This app runs on limited computational resources. Please do not upload long or confidential documents. For demo purposes only.",
        className="p-1 text-center",
        id="demo-banner",
        style={"borderBottom": "1px solid white"},
    )
)

app.layout = lambda: dbc.Container(
    [
        disclaimer,
        dbc.Row(main_nav.navbar()),
        dash.page_container,
    ],
    fluid=True,
)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(Constants.DOCS_DIR, path, as_attachment=True)


callbacks.translator.callbacks.init_callback(app)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)
