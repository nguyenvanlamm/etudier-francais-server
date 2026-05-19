from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models.user import User, RefreshToken
from app.schemas.user import (
    LoginRequest, RegisterRequest, GoogleLoginRequest,
    RefreshTokenRequest, LogoutRequest, UserResponse, TokenResponse
)
from app.services.auth import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token, decode_token
)
from app.services.firebase import verify_firebase_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(user_id=user.id, token=refresh_token, expires_at=expires_at)
    db.add(db_token)
    db.commit()

    return TokenResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            image=user.image,
            is_pro=user.is_pro,
            is_verified=user.is_verified
        ),
        accessToken=access_token,
        refreshToken=refresh_token
    )


@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = User(
        email=request.email,
        name=request.name,
        hashed_password=get_password_hash(request.password),
        auth_provider="email"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(user_id=user.id, token=refresh_token, expires_at=expires_at)
    db.add(db_token)
    db.commit()

    return TokenResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            image=user.image,
            is_pro=user.is_pro,
            is_verified=user.is_verified
        ),
        accessToken=access_token,
        refreshToken=refresh_token
    )


@router.post("/google", response_model=TokenResponse)
async def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        user_info = verify_firebase_token(request.idToken)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    email = user_info.get("email")
    name = user_info.get("name")
    picture = user_info.get("picture")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            name=name,
            image=picture,
            auth_provider="google"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.name = name or user.name
        user.image = picture or user.image
        db.commit()

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(user_id=user.id, token=refresh_token, expires_at=expires_at)
    db.add(db_token)
    db.commit()

    return TokenResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            image=user.image,
            is_pro=user.is_pro,
            is_verified=user.is_verified
        ),
        accessToken=access_token,
        refreshToken=refresh_token
    )


def handle_firebase_auth(user_info: dict, db: Session, provider: str = "firebase") -> TokenResponse:
    email = user_info.get("email")
    name = user_info.get("name")
    picture = user_info.get("picture")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            name=name,
            image=picture,
            auth_provider=provider
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.name = name or user.name
        user.image = picture or user.image
        db.commit()

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(user_id=user.id, token=refresh_token, expires_at=expires_at)
    db.add(db_token)
    db.commit()

    return TokenResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            image=user.image,
            is_pro=user.is_pro,
            is_verified=user.is_verified
        ),
        accessToken=access_token,
        refreshToken=refresh_token
    )


@router.post("/firebase/register", response_model=TokenResponse)
async def firebase_register(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        user_info = verify_firebase_token(request.idToken)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    return handle_firebase_auth(user_info, db, "firebase")


@router.post("/firebase/login", response_model=TokenResponse)
async def firebase_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        user_info = verify_firebase_token(request.idToken)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    return handle_firebase_auth(user_info, db, "firebase")


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refreshToken)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    stored_token = db.query(RefreshToken).filter(
        RefreshToken.token == request.refreshToken,
        RefreshToken.user_id == int(user_id)
    ).first()

    if not stored_token or stored_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    db.delete(stored_token)
    db.commit()

    access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(user_id=user.id, token=new_refresh_token, expires_at=expires_at)
    db.add(db_token)
    db.commit()

    return TokenResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            image=user.image,
            is_pro=user.is_pro,
            is_verified=user.is_verified
        ),
        accessToken=access_token,
        refreshToken=new_refresh_token
    )


@router.post("/logout")
def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    token = db.query(RefreshToken).filter(RefreshToken.token == request.refreshToken).first()
    if token:
        db.delete(token)
        db.commit()
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        image=current_user.image,
        is_pro=current_user.is_pro,
        is_verified=current_user.is_verified
    )


@router.patch("/me", response_model=UserResponse)
def update_me(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if "name" in data and data["name"]:
        current_user.name = data["name"]
    if "image" in data and data["image"]:
        current_user.image = data["image"]
    db.commit()
    db.refresh(current_user)

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        image=current_user.image,
        is_pro=current_user.is_pro,
        is_verified=current_user.is_verified
    )