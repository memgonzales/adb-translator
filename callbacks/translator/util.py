import base64
import datetime
import os
import random
import string
import time

from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobClient, BlobServiceClient, generate_container_sas
from dotenv import dotenv_values

from ..constants import Constants

# Set environment variables
config = dotenv_values(".env")

# Initialize clients
translation_client = DocumentTranslationClient(
    config["AZURE_DOCUMENT_TRANSLATION_ENDPOINT"],
    AzureKeyCredential(config["AZURE_DOCUMENT_TRANSLATION_KEY"]),
)

blob_service_client = BlobServiceClient(
    config["AZURE_STORAGE_ACCOUNT_ENDPOINT"],
    credential=config["AZURE_STORAGE_ACCOUNT_KEY"],
)

# Initialize clients
translation_client = DocumentTranslationClient(
    config["AZURE_DOCUMENT_TRANSLATION_ENDPOINT"],
    AzureKeyCredential(config["AZURE_DOCUMENT_TRANSLATION_KEY"]),
)

blob_service_client = BlobServiceClient(
    config["AZURE_STORAGE_ACCOUNT_ENDPOINT"],
    credential=config["AZURE_STORAGE_ACCOUNT_KEY"],
)


def generate_random_container_name():
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(20)
    )


# Create containers
def create_container(blob_service_client):
    while True:
        try:
            container_name = generate_random_container_name()
            container_client = blob_service_client.create_container(container_name)
            break

        except ResourceExistsError:
            pass

    return container_client


def get_file_extension(filename):
    return filename.split(".")[-1]


def remove_file_extension(filename):
    return ".".join(filename.split(".")[:-1])


def append_timestamp_to_filename(filename):
    return f"{remove_file_extension(filename)}-{time.time_ns() // 1000}.{get_file_extension(filename)}"


def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]

    if not os.path.exists(Constants.DOCS_DIR):
        os.makedirs(Constants.DOCS_DIR)

    with open(f"{Constants.DOCS_DIR}/{name}", "wb") as f:
        f.write(base64.decodebytes(data))


def construct_filename_with_language(filename, target_language):
    if filename.startswith(Constants.DOCS_DIR):
        # Add 1 to also remove the slash
        filename = filename[len(Constants.DOCS_DIR) + 1 :]

    return f"{remove_file_extension(filename)}-{target_language}.{get_file_extension(filename)}"


def upload_document_to_container(filename, source_container, target_language):
    with open(filename, "rb") as f:
        source_container.upload_blob(
            construct_filename_with_language(filename, target_language), f
        )


def generate_sas_url(container, permissions):
    sas_token = generate_container_sas(
        account_name=config["AZURE_STORAGE_ACCOUNT_NAME"],
        container_name=container.container_name,
        account_key=config["AZURE_STORAGE_ACCOUNT_KEY"],
        permission=permissions,
        expiry=datetime.datetime.now() + datetime.timedelta(hours=1),
    )

    container_sas_url = (
        config["AZURE_STORAGE_ACCOUNT_ENDPOINT"]
        + container.container_name
        + "?"
        + sas_token
    )

    return container_sas_url


def translate(filename, source_language, target_language):
    filename = f"{Constants.DOCS_DIR}/{filename}"

    # Perform translation only if translated document does not exist
    path_to_translated_document = f"{Constants.DOCS_DIR}/{construct_filename_with_language(filename, target_language)}"

    if not os.path.exists(path_to_translated_document):
        source_container = create_container(
            blob_service_client,
        )

        target_container = create_container(
            blob_service_client,
        )

        try:
            upload_document_to_container(filename, source_container, target_language)
        except ResourceExistsError:
            pass

        source_container_sas_url = generate_sas_url(source_container, permissions="rl")
        target_container_sas_url = generate_sas_url(target_container, permissions="wl")

        poller = translation_client.begin_translation(
            source_container_sas_url,
            target_container_sas_url,
            target_language=target_language,
            source_language=source_language,
        )

        for document in poller.result():
            if document.status == "Succeeded":
                blob_client = BlobClient.from_blob_url(
                    document.translated_document_url,
                    credential=config["AZURE_STORAGE_ACCOUNT_KEY"],
                )

                with open(path_to_translated_document, "wb") as f:
                    f.write(blob_client.download_blob().readall())

                break

        # Clean up
        source_container.delete_container()
        target_container.delete_container()

    return construct_filename_with_language(filename, target_language)


def get_link_to_file(filename):
    return f"/download/{filename}"
