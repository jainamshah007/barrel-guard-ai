# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

from fastapi import APIRouter, HTTPException
from app.services.plc_controller import plc_controller

router = APIRouter(prefix="/plc", tags=["PLC Control"])


@router.get("/status")
async def get_all_plc_status():
    return {
        "lines": plc_controller.get_all_status()
    }


@router.get("/status/{line_id}")
async def get_line_status(line_id: int):
    status = plc_controller.get_line_status(line_id)
    if status is None:
        raise HTTPException(status_code=404, detail=f"Line {line_id} not found")
    return status


@router.post("/stop/{line_id}")
async def stop_line(line_id: int, reason: str = "Manual stop"):
    result = await plc_controller.stop_line(line_id=line_id, reason=reason)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return {"message": f"Line {line_id} stopped", "status": result}


@router.post("/resume/{line_id}")
async def resume_line(line_id: int):
    result = await plc_controller.resume_line(line_id=line_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return {"message": f"Line {line_id} resumed", "status": result}


@router.get("/logs")
async def get_all_relay_logs():
    return {
        "logs": plc_controller.get_relay_logs()
    }


@router.get("/logs/{line_id}")
async def get_line_relay_logs(line_id: int):
    logs = plc_controller.get_relay_logs(line_id=line_id)
    return {
        "line_id": line_id,
        "logs": logs
    }