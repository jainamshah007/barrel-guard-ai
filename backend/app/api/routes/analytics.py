# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from datetime import datetime, timedelta
from app.models.database import get_db, Detection

router = APIRouter()

@router.get("/summary")
async def get_summary(db: AsyncSession = Depends(get_db)):
    try:
        total = await db.execute(select(func.count(Detection.id)))
        total_count = total.scalar() or 0
        today = datetime.utcnow().replace(hour=0, minute=0, second=0)
        today_result = await db.execute(
            select(func.count(Detection.id)).where(Detection.timestamp >= today)
        )
        today_count = today_result.scalar() or 0
        return {
            "total_detections": total_count,
            "today_detections": today_count,
            "cameras_active": 2,
            "lines_active": 2
        }
    except Exception as e:
        return {"total_detections": 0, "today_detections": 0, "cameras_active": 2, "lines_active": 2}

@router.get("/trends")
async def get_trends(
    hours: int = Query(24, ge=1, le=168),
    db: AsyncSession = Depends(get_db)
):
    try:
        since = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select(Detection).where(Detection.timestamp >= since).order_by(Detection.timestamp)
        )
        detections = result.scalars().all()
        return {
            "detections": [
                {
                    "timestamp": d.timestamp.isoformat() + "Z",
                    "object_class": d.object_class,
                    "camera_id": d.camera_id,
                    "line_id": d.line_id,
                    "confidence": d.confidence
                }
                for d in detections
            ]
        }
    except Exception as e:
        return {"detections": []}

@router.get("/by-class")
async def get_by_class(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Detection.object_class, func.count(Detection.id))
            .group_by(Detection.object_class)
            .order_by(desc(func.count(Detection.id)))
        )
        rows = result.all()
        return [{"object_class": r[0], "count": r[1]} for r in rows]
    except Exception as e:
        return []

@router.get("/by-camera")
async def get_by_camera(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Detection.camera_name, func.count(Detection.id))
            .group_by(Detection.camera_name)
            .order_by(desc(func.count(Detection.id)))
        )
        rows = result.all()
        return [{"camera_name": r[0], "count": r[1]} for r in rows]
    except Exception as e:
        return []
