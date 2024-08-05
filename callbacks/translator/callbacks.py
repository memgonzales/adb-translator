from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from ..constants import Constants
from ..translator.util import save_file, translate


def init_callback(app):
    @app.callback(
        Output("uploaded-filename", "children"),
        Input("upload-document", "filename"),
        Input("upload-document", "contents"),
    )
    def upload_file(filenames, contents):
        filename = ""
        if filenames and contents is not None:
            for name, data in zip(filenames, contents):
                filename = name
                save_file(name, data)
                break

        return filename

    @app.callback(
        Output("results-link", "children"),
        Input("translate-submit", "n_clicks"),
        State("uploaded-filename", "children"),
        State("source-language", "value"),
        State("target-language", "value"),
    )
    def translate_document(
        translate_submit_clicks, filename, source_language, target_languages
    ):
        if translate_submit_clicks > 0:
            return translate(
                filename, source_language, Constants.LANGUAGES[target_languages[0]]
            )

        raise PreventUpdate
