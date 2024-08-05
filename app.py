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


app.layout = lambda: dbc.Container(
    [
        dbc.Row(main_nav.navbar()),
        dash.page_container,
    ],
    fluid=True,
)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(Constants.UPLOAD_DIR, path, as_attachment=True)


callbacks.translator.callbacks.init_callback(app)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)
