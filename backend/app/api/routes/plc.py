# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.plc_controller import plc_controller

router = APIRouter()

class PLCCommand(BaseModel):
    line_id: str
    reason: Optional[str] = None

from typing import Optional

@router.get("/status")
async def get_plc_status():
    return plc_controller.get_all_status()

@router.post("/stop")
async def stop_line(command: PLCCommand):
    try:
        result = await plc_controller.stop_line(
            line_id=command.line_id,
            reason=command.reason or "Manual stop"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resume")
async def resume_line(command: PLCCommand):
    try:
        result = await plc_controller.resume_line(
            line_id=command.line_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def get_plc_logs():
    return plc_controller.get_logs()