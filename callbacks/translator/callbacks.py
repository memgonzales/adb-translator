from dash import Input, Output

from ..translator.util import save_file


def init_callback(app):
    @app.callback(
        Output("uploaded-filename", "children"),
        Input("upload-document", "filename"),
        Input("upload-document", "contents"),
    )
    def upload_file(filenames, contents):
        print("yo")
        filename = ""
        if filenames and contents is not None:
            for name, data in zip(filenames, contents):
                filename = name
                save_file(name, data)
                break

        return f"{filename} has been uploaded!"
