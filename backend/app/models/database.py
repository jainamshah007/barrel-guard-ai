# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)
Base = declarative_base()

class Detection(Base):
    __tablename__ = "detections"
    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, nullable=False)
    camera_name = Column(String(100), nullable=False)
    object_class = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    line_id = Column(String(20), nullable=False)
    barrel_id = Column(String(50), nullable=True)
    batch_id = Column(String(50), nullable=True)
    bbox_x = Column(Integer, nullable=True)
    bbox_y = Column(Integer, nullable=True)
    bbox_width = Column(Integer, nullable=True)
    bbox_height = Column(Integer, nullable=True)

class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    line_id = Column(String(20), nullable=False)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="warning")
    camera_id = Column(Integer, nullable=True)
    object_class = Column(String(50), nullable=True)
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

class ConveyorStopEvent(Base):
    __tablename__ = "conveyor_stop_events"
    id = Column(Integer, primary_key=True, index=True)
    line_id = Column(String(20), nullable=False)
    reason = Column(String(200), nullable=True)
    stopped_at = Column(DateTime, default=datetime.utcnow)
    resumed_at = Column(DateTime, nullable=True)

engine = create_async_engine(
    settings.get_database_url(),
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            result = await session.execute(select(Camera))
            cameras = result.scalars().all()
            if not cameras:
                session.add(Camera(id=1, name="Camera 1 - Line A", line_id="line_a", status="active"))
                session.add(Camera(id=2, name="Camera 2 - Line B", line_id="line_b", status="active"))
                await session.commit()
                logger.info("Cameras seeded successfully")
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database init error: {e}")
        raise
