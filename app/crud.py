from sqlalchemy.orm import Session
from . import models, schemas, auth
import uuid


# helper to handle UUID bytes <-> hex string


def bin_to_uuid_str(b: bytes) -> str:
    return uuid.UUID(bytes=b).hex


def uuid_str_to_bin(u: str) -> bytes:
    return uuid.UUID(u).bytes


# Users


def create_user(db: Session, user: schemas.UserCreate):
    hashed = auth.get_password_hash(user.password)
    u = models.User(user_name=user.user_name, user_email=user.user_email, password_hash=hashed)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.user_email == email).first()


def get_user_by_id(db: Session, user_id_bin: bytes):
    return db.query(models.User).filter(models.User.user_id == user_id_bin).first()


# Notes


def create_note(db: Session, user_id_bin: bytes, note_in: schemas.NoteCreate):
    n = models.Note(user_id=user_id_bin, note_title=note_in.note_title, note_content=note_in.note_content)
    db.add(n)
    db.commit()
    db.refresh(n)
    return n


def get_notes_by_user(db: Session, user_id_bin: bytes, limit: int = 50, offset: int = 0):
    return db.query(models.Note).filter(models.Note.user_id == user_id_bin).order_by(models.Note.created_on.desc()).offset(offset).limit(limit).all()


def get_note_by_id(db: Session, note_id_bin: bytes, user_id_bin: bytes):
    return db.query(models.Note).filter(models.Note.note_id == note_id_bin, models.Note.user_id == user_id_bin).first()


def update_note(db: Session, note_obj: models.Note, note_in: schemas.NoteCreate):
    if note_in.note_title is not None:
        note_obj.note_title = note_in.note_title
    if note_in.note_content is not None:
        note_obj.note_content = note_in.note_content
    db.add(note_obj)
    db.commit()
    db.refresh(note_obj)
    return note_obj


def delete_note(db: Session, note_obj: models.Note):
    db.delete(note_obj)
    db.commit()