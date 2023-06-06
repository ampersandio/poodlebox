from functools import lru_cache
from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    secret_key: str
    access_token_expires_minutes: int
    algorithm: str

    db_name: str
    db_host: str
    db_user: str
    db_password: str
    db_port: int

    api_key: str
    api_secret: str

    video_api_key: str


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# Manually load the environmental variables
settings.secret_key = os.getenv("SECRET_KEY")
settings.access_token_expires_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES"))
settings.algorithm = os.getenv("ALGORITHM")
settings.db_name = os.getenv("DB_NAME")
settings.db_host = os.getenv("DB_HOST")
settings.db_user = os.getenv("DB_USER")
settings.db_password = os.getenv("DB_PASSWORD")
settings.db_port = int(os.getenv("DB_PORT"))
settings.api_key = os.getenv("API_KEY")
settings.api_secret = os.getenv("API_SECRET")
settings.video_api_key = os.getenv("VIDEO_API_KEY")

