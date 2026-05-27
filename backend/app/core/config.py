# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "BARREL-GUARD AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "change-this-secret-key-in-production"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./barrelguard.db"

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # Simulation
    SIMULATION_ENABLED: bool = True
    SIMULATION_INTERVAL: float = 5.0
    NUM_CAMERAS: int = 2

    # Storage
    STORAGE_PATH: str = "./data/storage"

    # MQTT (optional)
    MQTT_ENABLED: bool = False
    MQTT_HOST: str = "localhost"
    MQTT_PORT: int = 1883

    # PLC
    PLC_ENABLED: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

    def get_database_url(self) -> str:
        url = self.DATABASE_URL
        # Normalize for asyncpg on Railway
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    def get_cors_origins(self) -> List[str]:
        return [
            self.FRONTEND_URL,
            "http://localhost:3000",
            "http://localhost:5173",
            "https://barrel-guard-ai.vercel.app",
        ]


settings = Settings()