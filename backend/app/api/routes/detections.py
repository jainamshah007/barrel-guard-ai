# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional, List
from app.models.database import get_db, Detection
from datetime import datetime

router = APIRouter()

@router.get("")
async def get_detections(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    camera_id: Optional[int] = None,
    object_class: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(Detection).order_by(desc(Detection.timestamp))
        if camera_id is not None:
            query = query.where(Detection.camera_id == camera_id)
        if object_class:
            query = query.where(Detection.object_class == object_class)
        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        detections = result.scalars().all()
        return {
            "detections": [
                {
                    "id": d.id,
                    "camera_id": d.camera_id,
                    "camera_name": d.camera_name,
                    "object_class": d.object_class,
                    "confidence": d.confidence,
                    "timestamp": d.timestamp.isoformat() if isinstance(d.timestamp, datetime) else d.timestamp,
                    "line_id": d.line_id,
                    "barrel_id": d.barrel_id,
                    "batch_id": d.batch_id,
                }
                for d in detections
            ],
            "total": len(detections)
        }
    except Exception as e:
        return {"detections": [], "total": 0, "error": str(e)}

@router.get("/recent")
async def get_recent_detections(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(Detection).order_by(desc(Detection.timestamp)).limit(limit)
        result = await db.execute(query)
        detections = result.scalars().all()
        return [
            {
                "id": d.id,
                "camera_id": d.camera_id,
                "camera_name": d.camera_name,
                "object_class": d.object_class,
                "confidence": d.confidence,
                "timestamp": d.timestamp.isoformat() if isinstance(d.timestamp, datetime) else d.timestamp,
                "line_id": d.line_id,
                "barrel_id": d.barrel_id,
                "batch_id": d.batch_id,
            }
            for d in detections
        ]
    except Exception as e:
        return []