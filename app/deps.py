from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, auth
import uuid


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


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


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        try:
            user_bin = hex_to_bin(user_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user id in token")
        user = crud.get_user_by_id(db, user_bin)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user