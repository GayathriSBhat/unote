# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "notes-backend"
    SECRET_KEY: str = "replace-with-secure-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    MYSQL_USER: str = "notes_user"
    MYSQL_PASSWORD: str = "notes_pass"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "notesdb"

    class Config:
        env_file = ".env"

settings = Settings()
