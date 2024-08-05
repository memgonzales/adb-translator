from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate

from ..constants import Constants
from ..translator.util import (
    append_timestamp_to_filename,
    get_link_to_file,
    save_file,
    translate,
)


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
            filename_with_timestamp = append_timestamp_to_filename(filename)
            save_file(filename_with_timestamp, contents)
            return (
                html.A(
                    filename,
                    href=get_link_to_file(filename_with_timestamp),
                    download="hi",
                ),
                filename_with_timestamp,
                {"display": "block"},
                {"display": "inline-block"},
                # {"display": "inline-block"},
                {"display": "inline-block", "whiteSpace": "pre"},
                {"display": "block"},
            )

        raise PreventUpdate

    @app.callback(
        Output("results-link", "children"),
        Input("translate-submit", "n_clicks"),
        State("true-uploaded-filename", "children"),
        State("source-language", "value"),
        State("target-language", "value"),
    )
    def translate_document(
        translate_submit_clicks, filename, source_language, target_languages
    ):
        if translate_submit_clicks > 0:
            if not filename:
                return html.H5("Error: Kindly upload a document to be translated")

            if not source_language:
                source_language = "Detect automatically"

            if not target_languages:
                return html.H5("Error: Kindly specify a source language")

            translated_documents = []

            for target_language in target_languages:
                translated_documents.append(
                    translate(
                        filename, source_language, Constants.LANGUAGES[target_language]
                    )
                )

            return "hello"

        raise PreventUpdate
