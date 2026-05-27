# =============================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# =============================================================

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "BARREL-GUARD AI"
    APP_VERSION: str = "1.0.0"
    FRONTEND_URL: str = "http://localhost:5173"

    DATABASE_URL: str = "sqlite+aiosqlite:///./barrel_guard.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
