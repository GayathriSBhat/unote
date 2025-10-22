# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import engine, Base
from .deps import get_db, get_current_user
from .config import settings
from datetime import timedelta
import uuid
from .init_db import init_database

# Initialize database before creating tables
init_database()

# create tables (dev convenience)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# -----------------------
# Homepage: bootstrapping endpoints (backend-only)
# -----------------------

@app.get("/", include_in_schema=False)
def root():
    # Redirect root to /home
    return RedirectResponse(url="/homepage")


@app.get("/homepage", response_class=PlainTextResponse, tags=["homepage"])
def homepage():
    """
    Plaintext homepage for backend-only testing.
    """
    return "welcome, please login"


@app.get("/homepage/login", tags=["homepage"])
def homepage_login_info():
    """
    Returns JSON describing available actions for login/signup (backend-only).
    No HTML returned — just instructions so you can call endpoints from Postman.
    """
    return {
        "message": "Use POST /homepage/login to login (JSON or form: email,password).",
        "signup": {
            "url": "/homepage/signup",
            "method": "POST",
            "body_json_example": {"user_name": "Alice", "user_email": "a@x.com", "password": "pw", "confirm_password": "pw"}
        },
        "login": {
            "url": "/homepage/login",
            "method": "POST",
            "body_json_example": {"email": "a@x.com", "password": "pw"}
        }
    }


@app.post("/homepage/login", tags=["homepage"])
async def homepage_login_post(request: Request, db: Session = Depends(get_db)):
    """
    Accepts either:
      - form data (email, password) (use Postman form-data or curl --form)
      - or JSON body { "email": "...", "password": "..." }
    Returns a JSON with access_token and token_type if credentials are valid.
    """
    # Try form data first (works with Postman form-data or curl --form)
    form_email = None
    form_password = None
    try:
        form = await request.form()
        form_email = form.get("email")
        form_password = form.get("password")
    except Exception:
        form_email = None
        form_password = None

    # If form data not present, try JSON
    if not form_email:
        try:
            body = await request.json()
            form_email = body.get("email")
            form_password = body.get("password")
        except Exception:
            form_email = form_email
            form_password = form_password

    if not form_email or not form_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing email or password. Provide form data or JSON."
        )

    # Authenticate user
    user = crud.get_user_by_email(db, form_email)
    if not user or not auth.verify_password(form_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    # Successful auth — create token
    user_hex = uuid.UUID(bytes=user.user_id).hex

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = auth.create_access_token(data={"sub": user_hex}, expires_delta=access_token_expires)
    print(access_token)
    
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})


@app.post("/homepage/signup", response_model=schemas.UserOut, tags=["homepage"])
async def homepage_signup(request: Request, db: Session = Depends(get_db)):
    """
    Create a new user when the provided email does not exist.
    Accepts either JSON:
      { "user_name": "...", "user_email": "...", "password": "...", "confirm_password": "..." }
    or form-data with the same keys.
    Returns the created user (user_id is returned as hex string).
    """
    # parse form first
    try:
        form = await request.form()
        if form:
            user_name = form.get("user_name")
            user_email = form.get("user_email")
            password = form.get("password")
            confirm_password = form.get("confirm_password")
        else:
            user_name = user_email = password = confirm_password = None
    except Exception:
        user_name = user_email = password = confirm_password = None

    # if not form, try JSON
    if not user_email:
        try:
            body = await request.json()
            user_name = body.get("user_name")
            user_email = body.get("user_email")
            password = body.get("password")
            confirm_password = body.get("confirm_password")
        except Exception:
            user_name = user_email = password = confirm_password = None

    # Validate presence
    if not user_name or not user_email or not password or not confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Missing one of required fields: user_name, user_email, password, confirm_password")

    if password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password and confirm_password do not match")

    # Check existing user
    existing = crud.get_user_by_email(db, user_email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Create user
    user_in = schemas.UserCreate(user_name=user_name, user_email=user_email, password=password)
    created = crud.create_user(db, user_in)
    # convert binary id to hex for response
    created.user_id = uuid.UUID(bytes=created.user_id).hex
    return created



@app.get("/homepage/notes", response_model=list[schemas.NoteOut], tags=["notes"])
def get_user_notes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all notes for the currently authenticated user.
    Requires a valid Bearer token.
    """
    user_id_bytes = current_user.user_id
    notes = crud.get_notes_by_user(db, user_id_bytes)
    if not notes:
        raise HTTPException(status_code=404, detail="No notes found for this user.")
    return notes


@app.get("/notes/{note_id}", response_model=schemas.NoteOut, tags=["notes"])
def get_note(note_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = crud.get_note_by_id(db, note_id, current_user.user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")
    return note
