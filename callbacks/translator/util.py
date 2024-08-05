import base64
import datetime
import hashlib
import os
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


# Create containers
def create_container(blob_service_client, container_name):
    try:
        container_client = blob_service_client.create_container(container_name)
    except ResourceExistsError:
        container_client = blob_service_client.get_container_client(
            container=container_name
        )
    return container_client


source_container = create_container(
    blob_service_client,
    "translation-source-container",
)

target_container = create_container(
    blob_service_client,
    "translation-target-container",
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


def append_timestamp_to_filename(filename):
    return f"{filename}.{time.time_ns() // 1000}"


def hash_filename_with_timestamp(filename):
    return hashlib.sha256(
        append_timestamp_to_filename(filename).encode("utf-8")
    ).hexdigest()


def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]

    if not os.path.exists(Constants.UPLOAD_DIR):
        os.makedirs(Constants.UPLOAD_DIR)

    with open(f"{Constants.UPLOAD_DIR}/{name}", "wb") as f:
        f.write(base64.decodebytes(data))


def upload_document_to_container(filename):
    blob_names = [blob.name for blob in source_container.list_blobs()]
    if filename not in blob_names:
        with open(filename, "rb") as f:
            source_container.upload_blob(filename, f)


def generate_sas_url(container, permissions):
    sas_token = generate_container_sas(
        account_name=config["AZURE_STORAGE_ACCOUNT_NAME"],
        container_name=container.container_name,
        account_key=config["AZURE_STORAGE_ACCOUNT_KEY"],
        permission=permissions,
        expiry=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
    )

    container_sas_url = (
        config["AZURE_STORAGE_ACCOUNT_ENDPOINT"]
        + container.container_name
        + "?"
        + sas_token
    )

    return container_sas_url


def translate(filename, source_language, target_language):
    upload_document_to_container(filename)

    source_container_sas_url = generate_sas_url(source_container, permissions="rl")
    target_container_sas_url = generate_sas_url(target_container, permissions="wl")

    poller = translation_client.begin_translation(
        source_container_sas_url, target_container_sas_url, target_language
    )

    result = poller.result()
    print(f"Status: {poller.status()}")

    for document in result:
        if document.status == "Succeeded":
            blob_client = BlobClient.from_blob_url(
                document.translated_document_url,
                credential=config["AZURE_STORAGE_ACCOUNT_KEY"],
            )
            with open(
                f"{Constants.UPLOAD_DIR}/{filename}_{target_language}", "wb"
            ) as f:
                f.write(blob_client.download_blob().readall())

            print("Done!")
            break

    return f"{Constants.UPLOAD_DIR}/{filename}_{target_language}"
