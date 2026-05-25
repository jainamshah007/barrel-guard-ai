# =============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# =============================================================================

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "BARREL-GUARD AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Database — SQLite locally, PostgreSQL on Railway
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./barrelguard.db"
    )

    # Redis — optional
    REDIS_URL: str = os.getenv("REDIS_URL", "memory://")

    # MQTT — simulated
    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_ENABLED: bool = os.getenv("MQTT_ENABLED", "false").lower() == "true"

    # Storage
    STORAGE_MODE: str = os.getenv("STORAGE_MODE", "local")
    LOCAL_STORAGE_PATH: str = os.getenv("LOCAL_STORAGE_PATH", "./data/snapshots")
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "barrelguard")

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "barrel-guard-ai-secret-key-2024"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # CORS — allow Railway and Vercel domains
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
    ]

    # Simulation
    SIMULATION_ENABLED: bool = True
    SIMULATION_INTERVAL_SECONDS: float = float(
        os.getenv("SIMULATION_INTERVAL_SECONDS", "3.0")
    )
    FOREIGN_OBJECT_PROBABILITY: float = float(
        os.getenv("FOREIGN_OBJECT_PROBABILITY", "0.3")
    )

    # Detection
    DETECTION_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("DETECTION_CONFIDENCE_THRESHOLD", "0.75")
    )

    # PLC
    PLC_ENABLED: bool = os.getenv("PLC_ENABLED", "false").lower() == "true"
    PLC_STOP_DURATION_SECONDS: int = int(
        os.getenv("PLC_STOP_DURATION_SECONDS", "10")
    )

    # Camera
    NUM_CAMERAS: int = int(os.getenv("NUM_CAMERAS", "2"))

    # Port — Railway injects PORT automatically
    PORT: int = int(os.getenv("PORT", "8000"))

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
