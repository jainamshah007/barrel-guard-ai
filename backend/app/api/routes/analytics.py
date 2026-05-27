# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

from fastapi import APIRouter
from app.services.simulator import sim_state, OBJECT_CLASSES
from app.services.plc_controller import plc_controller

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
async def get_summary():
    plc_status = plc_controller.get_all_status()
    stopped_lines = sum(1 for l in plc_status if l["status"] == "stopped")
    return {
        "total_injections": sim_state.injection_count,
        "active_lines": len(plc_status) - stopped_lines,
        "stopped_lines": stopped_lines,
        "simulation_running": sim_state.running,
        "object_classes": OBJECT_CLASSES,
    }


@router.get("/kpis")
async def get_kpis():
    plc_status = plc_controller.get_all_status()
    total_stops = sum(l["stop_count"] for l in plc_status)
    return {
        "total_detections": sim_state.injection_count,
        "total_line_stops": total_stops,
        "lines": plc_status,
    }
