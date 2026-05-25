from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import get_db
from app.schemas.schemas import (
    InjectRequest, SimConfigRequest
)
from app.services.simulator import (
    sim_state, inject_detection
)
from app.websockets.manager import manager
from app.models.database import AsyncSessionLocal

router = APIRouter()


@router.get("/status")
async def get_status():
    return sim_state


@router.post("/inject")
async def manual_inject(
    body: InjectRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    background_tasks.add_task(
        inject_detection,
        body.camera_id,
        body.object_class,
        AsyncSessionLocal,
        manager
    )
    return {
        "status": "injected",
        "camera_id": body.camera_id,
        "object_class": body.object_class
    }


@router.post("/config")
async def update_config(body: SimConfigRequest):
    sim_state["auto_mode"] = body.auto_mode
    if body.interval_min:
        sim_state["interval_min"] = body.interval_min
    if body.interval_max:
        sim_state["interval_max"] = body.interval_max
    return {"status": "updated", "config": sim_state}


@router.post("/resume/{camera_id}")
async def resume_line(camera_id: int):
    if camera_id in sim_state["camera_states"]:
        sim_state["camera_states"][camera_id].update({
            "stopped": False,
            "alert_active": False,
            "last_detection": None
        })
        await manager.broadcast({
            "type": "plc_update",
            "camera_id": camera_id,
            "status": "RUNNING"
        })
    return {"status": "resumed"}
