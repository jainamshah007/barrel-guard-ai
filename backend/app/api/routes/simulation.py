# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

from fastapi import APIRouter, HTTPException
from app.services.simulator import simulator, sim_state, OBJECT_CLASSES, CAMERA_NAMES
from app.core.config import settings

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.get("/status")
async def get_simulation_status():
    return {
        "running": sim_state.running,
        "auto_mode": sim_state.auto_mode,
        "interval": sim_state.interval,
        "num_cameras": sim_state.num_cameras,
        "injection_count": sim_state.injection_count,
        "session_start": sim_state.session_start.isoformat() if sim_state.session_start else None,
        "object_classes": OBJECT_CLASSES,
        "cameras": CAMERA_NAMES,
    }


@router.post("/start")
async def start_simulation():
    if sim_state.running:
        return {"message": "Simulation already running"}
    await simulator.start()
    return {"message": "Simulation started", "running": sim_state.running}


@router.post("/stop")
async def stop_simulation():
    await simulator.stop()
    return {"message": "Simulation stopped", "running": sim_state.running}


@router.post("/inject")
async def inject_detection(camera_id: int = None, object_class: str = None):
    if object_class and object_class not in OBJECT_CLASSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid object class. Choose from: {OBJECT_CLASSES}"
        )
    detection = await simulator.inject_detection(
        camera_id=camera_id,
        object_class=object_class,
    )
    return {"message": "Detection injected", "detection": detection}


@router.post("/config")
async def update_simulation_config(
    interval: float = None,
    auto_mode: bool = None,
):
    if interval is not None:
        if interval < 1.0 or interval > 60.0:
            raise HTTPException(
                status_code=400,
                detail="Interval must be between 1 and 60 seconds"
            )
        sim_state.interval = interval

    if auto_mode is not None:
        sim_state.auto_mode = auto_mode

    return {
        "message": "Configuration updated",
        "interval": sim_state.interval,
        "auto_mode": sim_state.auto_mode,
    }