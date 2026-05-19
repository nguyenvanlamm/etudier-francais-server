import os
import firebase_admin
from firebase_admin import credentials
from pathlib import Path


_cred = None
_app = None


def get_firebase_cred():
    global _cred
    if _cred is None:
        base_dir = Path(__file__).parent.parent.parent
        cred_path = os.path.join(base_dir, "firebase-credentials.json")
        _cred = credentials.Certificate(cred_path)
    return _cred


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
    app = get_firebase_app()
    from firebase_admin import auth
    
    try:
        decoded_token = auth.verify_id_token(id_token, app=app)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid Firebase token: {str(e)}")