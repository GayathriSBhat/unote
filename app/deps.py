from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, auth
import uuid


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
bearer = HTTPBearer()  # this reads Authorization: Bearer <token>

# DB session dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# helper to convert uuid hex strings to bin and vice versa


def hex_to_bin(hex_id: str) -> bytes:
    return uuid.UUID(hex=hex_id).bytes



async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):
    # DEBUG prints - watch your uvicorn console
    print(">>> get_current_user called")
    print(">>> credentials object:", credentials)

    if not credentials:
        print(">>> no credentials provided")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = credentials.credentials
    print(">>> raw token:", token[:20] + "..." if token else None)  # don't print whole token in prod

    # use your existing decode function
    payload = auth.decode_access_token(token)
    print(">>> decoded payload:", payload)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_hex = payload.get("sub")
    print(">>> payload.sub (user_hex):", user_hex)
    if not user_hex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    try:
        user_bin = hex_to_bin(user_hex)
    except Exception as e:
        print(">>> hex_to_bin failed:", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user id in token")

    user = crud.get_user_by_id(db, user_bin)
    print(">>> user from DB:", bool(user), getattr(user, "user_email", None) if user else None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # success
    return user