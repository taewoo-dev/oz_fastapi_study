import os
from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerEnv(StrEnum):
    Local = "local"
    DEV = "dev"
    PROD = "prod"


SERVER_ENV = os.getenv("ENV", ServerEnv.Local)


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str

    # model_config = SettingsConfigDict(env_file=f".env.{SERVER_ENV}")
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), f".env.{SERVER_ENV}")
    )


settings = Settings()
