"""การตั้งค่าระบบ — อ่านจาก environment / .env ผ่าน pydantic-settings"""
from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- Database ----
    DATABASE_URL: str = "mysql+pymysql://prohealth:prohealthpass@127.0.0.1:3306/prohealthcare"

    # ---- Security ----
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 วัน

    # ---- CORS ----
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:4173"

    @field_validator("CORS_ORIGINS")
    @classmethod
    def _strip_cors(cls, v: str) -> str:
        return ",".join(origin.strip() for origin in v.split(",") if origin.strip())

    @property
    def cors_origins_list(self) -> List[str]:
        return self.CORS_ORIGINS.split(",")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
