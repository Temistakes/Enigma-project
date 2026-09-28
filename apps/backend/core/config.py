import os
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

MODE = os.getenv("MODE", "DEV").lower()
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / f".env.{MODE}"


class Settings(BaseSettings):
    MODE: Literal["TEST", "DEV", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    REDIS: str

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS}"

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


settings: Settings = Settings()  # pyright: ignore[reportCallIssue]
