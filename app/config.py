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

    class Config:
        env_file = '../.env'


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


