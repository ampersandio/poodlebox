from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Dr. Blalexolai E-University'
    secret_key: str
    access_token_expires_minutes: int
    algorithm: str
    database: str
    db_host: str
    db_user: str
    db_password: str
    db_port: int

    class Config:
        env_file = '.env'
        