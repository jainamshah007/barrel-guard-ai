# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.database import get_db, Camera
from app.services.simulator import sim_state

router = APIRouter()

@router.get("")
async def get_cameras(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Camera))
        cameras = result.scalars().all()
        return [
            {
                "id": c.id,
                "name": c.name,
                "line_id": c.line_id,
                "status": "active" if sim_state.running else "idle"
            }
            for c in cameras
        ]
    except Exception as e:
        return []

@router.get("/{camera_id}")
async def get_camera(camera_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Camera).where(Camera.id == camera_id))
        camera = result.scalar_one_or_none()
        if not camera:
            return {"error": "Camera not found"}
        return {
            "id": camera.id,
            "name": camera.name,
            "line_id": camera.line_id,
            "status": "active" if sim_state.running else "idle"
        }
    except Exception as e:
        return {"error": str(e)}
