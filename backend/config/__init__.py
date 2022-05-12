import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "To do API"
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "insecure")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 1 day


settings = Settings()