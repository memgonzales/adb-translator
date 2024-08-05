import base64
import os

from ..constants import Constants


def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]

    if not os.path.exists(Constants.UPLOAD_DIR):
        os.makedirs(Constants.UPLOAD_DIR)

    with open(f"{Constants.UPLOAD_DIR}/{name}", "wb") as f:
        f.write(base64.decodebytes(data))
