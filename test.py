from dotenv import dotenv_values

DOCUMENT = "adb-chinese-doc.pdf"
TARGET_LANGUAGE = "en"

import datetime

from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobClient, BlobServiceClient, generate_container_sas

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
        print(f"Creating container: {container_name}")
    except ResourceExistsError:
        print(f"The container with name {container_name} already exists")
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

# Upload document to container
blob_names = [blob.name for blob in source_container.list_blobs()]

if DOCUMENT not in blob_names:
    with open(DOCUMENT, "rb") as f:
        source_container.upload_blob(DOCUMENT, f)
else:
    print(f"{DOCUMENT} already exists in the container.")


# Generate SAS url
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
    print(f"Generating {container.container_name} SAS URL")
    return container_sas_url


source_container_sas_url = generate_sas_url(source_container, permissions="rl")
target_container_sas_url = generate_sas_url(target_container, permissions="wl")


poller = translation_client.begin_translation(
    source_container_sas_url, target_container_sas_url, TARGET_LANGUAGE
)
print(f"Created translation operation with ID: {poller.id}")
print("Waiting until translation completes...")

result = poller.result()
print(f"Status: {poller.status()}")

print("\nDocument results:")
for document in result:
    print(f"Document ID: {document.id}")
    print(f"Document status: {document.status}")
    if document.status == "Succeeded":
        print(f"Source document location: {document.source_document_url}")
        print(f"Translated document location: {document.translated_document_url}")
        print(f"Translated to language: {document.translated_to}\n")

        blob_client = BlobClient.from_blob_url(
            document.translated_document_url,
            credential=config["AZURE_STORAGE_ACCOUNT_KEY"],
        )
        with open("translated_" + DOCUMENT, "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())

        print("Downloaded {} locally".format("translated_" + DOCUMENT))
    else:
        print("\nThere was a problem translating your document.")
        print(
            f"Document Error Code: {document.error.code}, Message: {document.error.message}\n"
        )
