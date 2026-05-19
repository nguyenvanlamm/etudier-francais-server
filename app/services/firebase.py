import firebase_admin
from firebase_admin import credentials
from app.config import settings


_cred = None
_app = None


def get_firebase_cred():
    global _cred
    if _cred is None:
        _cred = credentials.Certificate({
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "token_uri": "https://oauth2.googleapis.com/token",
        })
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