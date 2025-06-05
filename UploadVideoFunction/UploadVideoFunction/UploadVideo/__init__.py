import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
import uuid

# Set via App Settings in Azure or local.settings.json
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "videos"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Uploading video file...')

    try:
        file = req.files.get('file')
        if not file:
            return func.HttpResponse("Missing file", status_code=400)

        filename = f"{uuid.uuid4()}.mp4"

        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=filename)
        blob_client.upload_blob(file.stream.read(), blob_type="BlockBlob", overwrite=True)

        blob_url = blob_client.url  # Only public if container allows it

        return func.HttpResponse(f"Uploaded successfully: {blob_url}", status_code=200)

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(f"Error uploading file: {str(e)}", status_code=500)
