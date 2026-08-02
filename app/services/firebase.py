import json
import os
import firebase_admin
from firebase_admin import credentials
from app.config import settings


_cred = None
_app = None


def _build_cred_from_env():
    required = [
        settings.FIREBASE_PROJECT_ID,
        settings.FIREBASE_CLIENT_EMAIL,
        settings.FIREBASE_PRIVATE_KEY,
    ]
    if not all(required):
        return None

    private_key = settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n")
    return credentials.Certificate({
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
    })


def get_firebase_cred():
    global _cred
    if _cred is not None:
        return _cred

    json_path = settings.FIREBASE_CREDENTIALS_PATH
    if json_path and os.path.exists(json_path):
        _cred = credentials.Certificate(json_path)
        return _cred

    _cred = _build_cred_from_env()
    if _cred is not None:
        return _cred

    raise RuntimeError(
        "Firebase credentials not found. Set firebase-credentials.json or "
        "FIREBASE_PROJECT_ID + FIREBASE_CLIENT_EMAIL + FIREBASE_PRIVATE_KEY env vars."
    )


def get_firebase_app():
    global _app
    if _app is None:
        if not firebase_admin._apps:
            cred = get_firebase_cred()
            _app = firebase_admin.initialize_app(cred)
        else:
            _app = firebase_admin.get_app()
    return _app


def verify_firebase_token(id_token: str) -> dict:
    from firebase_admin import auth

    try:
        app = get_firebase_app()
        decoded_token = auth.verify_id_token(id_token, app=app)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid Firebase token: {str(e)}")
