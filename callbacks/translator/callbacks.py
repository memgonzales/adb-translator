from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from ..constants import Constants
from ..translator.util import hash_filename_with_timestamp, save_file, translate


def init_callback(app):
    @app.callback(
        Output("uploaded-filename", "children"),
        Output("true-uploaded-filename", "children"),
        Output("break-1", "style"),
        Output("uploaded-filename", "style"),
        # Output("true-uploaded-filename", "style"),
        Output("uploaded-successfully", "style"),
        Output("break-2", "style"),
        Input("upload-document", "filename"),
        Input("upload-document", "contents"),
    )
    def upload_file(filename, contents):
        if filename and contents:
            save_file(filename, contents)
            return (
                filename,
                hash_filename_with_timestamp(filename),
                {"display": "block"},
                {"display": "inline-block"},
                # {"display": "inline-block"},
                {"display": "inline-block"},
                {"display": "block"},
            )

        raise PreventUpdate

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
