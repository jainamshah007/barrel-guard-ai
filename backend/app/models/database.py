# =============================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution of
# this file, via any medium, is strictly prohibited.
# =============================================================

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, JSON, Text, ForeignKey
)
from sqlalchemy.sql import func
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


class Camera(Base):
    __tablename__ = "cameras"

    id                  = Column(Integer, primary_key=True, index=True)
    name                = Column(String(100), nullable=False)
    line_id             = Column(String(50), nullable=False)
    description         = Column(Text, nullable=True)
    confidence_threshold= Column(Float, default=0.75)
    plc_enabled         = Column(Boolean, default=True)
    sim_auto_inject     = Column(Boolean, default=True)
    sim_frequency_sec   = Column(Integer, default=20)
    status              = Column(String(20), default="active")
    created_at          = Column(DateTime(timezone=True), server_default=func.now())


class Detection(Base):
    __tablename__ = "detections"

    id                  = Column(Integer, primary_key=True, index=True)
    camera_id           = Column(Integer, ForeignKey("cameras.id"), nullable=True)
    conveyor_line_id    = Column(String(50), nullable=True)
    barrel_id           = Column(String(50), nullable=True)
    batch_id            = Column(String(50), nullable=True)
    object_class        = Column(String(100), nullable=False)
    confidence          = Column(Float, nullable=False)
    bounding_box        = Column(JSON, nullable=True)
    snapshot_path       = Column(String(255), nullable=True)
    plc_triggered       = Column(Boolean, default=False)
    severity            = Column(String(20), default="HIGH")
    acknowledged        = Column(Boolean, default=False)
    acknowledged_by     = Column(String(100), nullable=True)
    acknowledged_at     = Column(DateTime(timezone=True), nullable=True)
    notes               = Column(Text, nullable=True)
    is_false_positive   = Column(Boolean, default=False)
    sim_injected        = Column(Boolean, default=True)
    created_at          = Column(DateTime(timezone=True), server_default=func.now())


class ConveyorStopEvent(Base):
    __tablename__ = "conveyor_stop_events"

    id                  = Column(Integer, primary_key=True, index=True)
    line_id             = Column(String(50), nullable=False)
    detection_id        = Column(Integer, ForeignKey("detections.id"), nullable=True)
    triggered_by        = Column(String(100), nullable=True)
    stop_reason         = Column(Text, nullable=True)
    stopped_at          = Column(DateTime(timezone=True), server_default=func.now())
    resumed_at          = Column(DateTime(timezone=True), nullable=True)
    duration_seconds    = Column(Float, nullable=True)
    operator            = Column(String(100), nullable=True)


class NotificationRule(Base):
    __tablename__ = "notification_rules"

    id                  = Column(Integer, primary_key=True, index=True)
    name                = Column(String(100), nullable=False)
    severity_filter     = Column(String(20), default="HIGH")
    channel             = Column(String(50), default="in_app")
    recipient           = Column(String(255), nullable=True)
    enabled             = Column(Boolean, default=True)
    created_at          = Column(DateTime(timezone=True), server_default=func.now())


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id                  = Column(Integer, primary_key=True, index=True)
    rule_id             = Column(Integer, ForeignKey("notification_rules.id"), nullable=True)
    detection_id        = Column(Integer, ForeignKey("detections.id"), nullable=True)
    channel             = Column(String(50), nullable=True)
    recipient           = Column(String(255), nullable=True)
    message             = Column(Text, nullable=True)
    status              = Column(String(20), default="sent")
    sent_at             = Column(DateTime(timezone=True), server_default=func.now())


class SimulationSession(Base):
    __tablename__ = "simulation_sessions"

    id                  = Column(Integer, primary_key=True, index=True)
    started_at          = Column(DateTime(timezone=True), server_default=func.now())
    ended_at            = Column(DateTime(timezone=True), nullable=True)
    total_detections    = Column(Integer, default=0)
    total_stops         = Column(Integer, default=0)
    config              = Column(JSON, nullable=True)
    notes               = Column(Text, nullable=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_initial_data()
    logger.info("Database initialized successfully.")


async def seed_initial_data():
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(select(Camera))
        cameras = result.scalars().all()
        if not cameras:
            cam1 = Camera(
                name="Camera 1 – Line A",
                line_id="LINE_A",
                description="Monitors Conveyor Line A barrels",
                confidence_threshold=0.75,
                plc_enabled=True,
                sim_auto_inject=True,
                sim_frequency_sec=20,
                status="active"
            )
            cam2 = Camera(
                name="Camera 2 – Line B",
                line_id="LINE_B",
                description="Monitors Conveyor Line B barrels",
                confidence_threshold=0.75,
                plc_enabled=True,
                sim_auto_inject=True,
                sim_frequency_sec=25,
                status="active"
            )
            session.add_all([cam1, cam2])
            await session.commit()
            logger.info("Seeded 2 cameras.")

        result2 = await session.execute(select(NotificationRule))
        rules = result2.scalars().all()
        if not rules:
            rule = NotificationRule(
                name="Default High Severity Alert",
                severity_filter="HIGH",
                channel="in_app",
                recipient="operator",
                enabled=True
            )
            session.add(rule)
            await session.commit()
            logger.info("Seeded default notification rule.")


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
