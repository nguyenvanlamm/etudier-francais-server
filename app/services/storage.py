import os
import json
from google.cloud import storage
from google.oauth2 import service_account
from app.config import settings


_client = None


def _get_credentials():
    json_path = getattr(settings, "FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    if json_path and os.path.exists(json_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
        return None

    required = [
        settings.FIREBASE_PROJECT_ID,
        settings.FIREBASE_CLIENT_EMAIL,
        settings.FIREBASE_PRIVATE_KEY,
    ]
    if not all(required):
        raise RuntimeError(
            "Google Cloud credentials not found. Set firebase-credentials.json or "
            "FIREBASE_PROJECT_ID + FIREBASE_CLIENT_EMAIL + FIREBASE_PRIVATE_KEY env vars."
        )

    private_key = settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n")
    info = {
        "type": "service_account",
        "project_id": settings.FIREBASE_PROJECT_ID,
        "private_key_id": "",
        "private_key": private_key,
        "client_email": settings.FIREBASE_CLIENT_EMAIL,
        "client_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{settings.FIREBASE_CLIENT_EMAIL}",
    }
    return service_account.Credentials.from_service_account_info(info)


def get_storage_client():
    global _client
    if _client is not None:
        return _client

    creds = _get_credentials()
    if creds is not None:
        _client = storage.Client(credentials=creds, project=settings.FIREBASE_PROJECT_ID)
    else:
        _client = storage.Client()
    return _client


def upload_file(file_path: str, destination_blob_name: str, bucket_name: str = None) -> str:
    if bucket_name is None:
        bucket_name = getattr(settings, "FIREBASE_STORAGE_BUCKET", None)

    if not bucket_name:
        raise ValueError("FIREBASE_STORAGE_BUCKET not configured")

    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(file_path)
    blob.make_public()

    return blob.public_url


def delete_file(destination_blob_name: str, bucket_name: str = None) -> bool:
    if bucket_name is None:
        bucket_name = getattr(settings, "FIREBASE_STORAGE_BUCKET", None)

    if not bucket_name:
        raise ValueError("FIREBASE_STORAGE_BUCKET not configured")

    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    if blob.exists():
        blob.delete()
        return True
    return False
