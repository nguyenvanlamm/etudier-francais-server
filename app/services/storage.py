import os
from google.cloud import storage
from pathlib import Path


_credential_path = None
_client = None


def get_storage_client():
    global _client
    if _client is None:
        from app.config import settings
        credential_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
        
        if not os.path.isabs(credential_path):
            base_dir = Path(__file__).parent.parent.parent
            credential_path = os.path.join(base_dir, credential_path)
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
        _client = storage.Client()
    return _client


def upload_file(file_path: str, destination_blob_name: str, bucket_name: str = None) -> str:
    """Upload a file to Firebase Storage and return the public URL."""
    from app.config import settings
    
    if bucket_name is None:
        bucket_name = getattr(settings, 'FIREBASE_STORAGE_BUCKET', None)
    
    if not bucket_name:
        raise ValueError("FIREBASE_STORAGE_BUCKET not configured")
    
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(file_path)
    
    blob.make_public()
    
    return blob.public_url


def delete_file(destination_blob_name: str, bucket_name: str = None) -> bool:
    """Delete a file from Firebase Storage."""
    from app.config import settings
    
    if bucket_name is None:
        bucket_name = getattr(settings, 'FIREBASE_STORAGE_BUCKET', None)
    
    if not bucket_name:
        raise ValueError("FIREBASE_STORAGE_BUCKET not configured")
    
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    if blob.exists():
        blob.delete()
        return True
    return False