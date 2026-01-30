"""
Config file to manage application settings.
"""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", env_file_encoding="utf-8"
    )

    tg_token: str
    allow_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"

    redis: RedisSettings


settings = Settings()  # type: ignore

redis = Redis(host=settings.redis.host, port=settings.redis.port, db=settings.redis.db)
