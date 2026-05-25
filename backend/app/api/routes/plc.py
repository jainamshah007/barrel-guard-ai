from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.database import (
    ConveyorStopEvent, get_db
)
from app.services.plc_controller import plc_controller
from app.schemas.schemas import PLCCommand
from app.websockets.manager import manager
from datetime import datetime

router = APIRouter()


@router.get("/status")
async def get_status():
    return plc_controller.get_status()


@router.post("/stop")
async def stop_line(body: PLCCommand):
    result = plc_controller.send_stop(body.line_id)
    await manager.broadcast({
        "type": "plc_update",
        "line_id": body.line_id,
        "status": "STOPPED",
        "operator": body.operator,
        "timestamp": datetime.utcnow().isoformat()
    })
    return result


@router.post("/resume")
async def resume_line(body: PLCCommand):
    result = plc_controller.send_resume(
        body.line_id, body.operator
    )
    await manager.broadcast({
        "type": "plc_update",
        "line_id": body.line_id,
        "status": "RUNNING",
        "operator": body.operator,
        "timestamp": datetime.utcnow().isoformat()
    })
    return result


@router.get("/relay-logs")
async def get_relay_logs(
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConveyorStopEvent)
        .order_by(desc(ConveyorStopEvent.stopped_at))
        .limit(limit)
    )
    events = result.scalars().all()
    return [
        {
            "id": e.id,
            "camera_id": e.camera_id,
            "stopped_at": e.stopped_at,
            "resumed_at": e.resumed_at,
            "duration_sec": e.duration_sec,
            "trigger_type": e.trigger_type
        }
        for e in events
    ]
