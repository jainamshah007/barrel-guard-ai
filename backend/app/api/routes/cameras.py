from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from app.models.database import Camera, get_db
from app.schemas.schemas import CameraOut, CameraUpdate

router = APIRouter()


@router.get("/", response_model=List[CameraOut])
async def get_cameras(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Camera))
    return result.scalars().all()


@router.put("/{camera_id}")
async def update_camera(
    camera_id: int,
    body: CameraUpdate,
    db: AsyncSession = Depends(get_db)
):
    cam = await db.get(Camera, camera_id)
    if not cam:
        from fastapi import HTTPException
        raise HTTPException(404, "Camera not found")

    for field, value in body.model_dump(
        exclude_none=True
    ).items():
        setattr(cam, field, value)
    cam.updated_at = datetime.utcnow()
    await db.commit()
    return {"status": "updated"}
