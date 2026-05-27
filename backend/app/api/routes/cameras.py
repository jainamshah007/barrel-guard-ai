# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.services.simulator import CAMERA_NAMES

router = APIRouter(prefix="/cameras", tags=["Cameras"])


@router.get("/")
async def get_cameras():
    cameras = [
        {
            "id": i,
            "name": CAMERA_NAMES[i],
            "status": "active",
            "line": "A" if i % 2 == 0 else "B",
        }
        for i in range(settings.NUM_CAMERAS)
    ]
    return {"cameras": cameras}


@router.get("/{camera_id}")
async def get_camera(camera_id: int):
    if camera_id < 0 or camera_id >= settings.NUM_CAMERAS:
        raise HTTPException(status_code=404, detail="Camera not found")
    return {
        "id": camera_id,
        "name": CAMERA_NAMES[camera_id],
        "status": "active",
        "line": "A" if camera_id % 2 == 0 else "B",
    }
