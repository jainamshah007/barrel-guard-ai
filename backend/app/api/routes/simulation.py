# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.simulator import simulator, sim_state, OBJECT_CLASSES, CAMERA_NAMES

router = APIRouter()

class SimulationConfig(BaseModel):
    interval: Optional[float] = None
    num_cameras: Optional[int] = None
    auto_mode: Optional[bool] = None

class InjectRequest(BaseModel):
    camera_id: Optional[int] = None
    object_class: Optional[str] = None

@router.get("/status")
async def get_simulation_status():
    return {
        "running": sim_state.running,
        "auto_mode": sim_state.auto_mode,
        "interval": sim_state.interval,
        "num_cameras": sim_state.num_cameras,
        "total_injected": sim_state.total_injected,
        "object_classes": OBJECT_CLASSES,
        "camera_names": CAMERA_NAMES
    }

@router.post("/start")
async def start_simulation():
    await simulator.start()
    return {"message": "Simulation started", "running": sim_state.running}

@router.post("/stop")
async def stop_simulation():
    await simulator.stop()
    return {"message": "Simulation stopped", "running": sim_state.running}

@router.post("/inject")
async def inject_detection(request: InjectRequest = None):
    try:
        camera_id = None
        object_class = None
        if request:
            camera_id = request.camera_id
            object_class = request.object_class
        await simulator.inject_detection(
            camera_id=camera_id,
            object_class=object_class
        )
        return {"message": "Detection injected successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config")
async def update_config(config: SimulationConfig):
    if config.interval is not None:
        if config.interval < 1 or config.interval > 60:
            raise HTTPException(status_code=400, detail="Interval must be between 1 and 60 seconds")
        sim_state.interval = config.interval
    if config.num_cameras is not None:
        sim_state.num_cameras = config.num_cameras
    if config.auto_mode is not None:
        sim_state.auto_mode = config.auto_mode
    return {"message": "Configuration updated", "config": {
        "interval": sim_state.interval,
        "num_cameras": sim_state.num_cameras,
        "auto_mode": sim_state.auto_mode
    }}