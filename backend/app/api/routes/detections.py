# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

from fastapi import APIRouter
from app.services.simulator import simulator, sim_state

router = APIRouter(prefix="/detections", tags=["Detections"])

_detections_store = []


@router.get("/")
async def get_detections(limit: int = 50, skip: int = 0):
    return {
        "detections": list(reversed(_detections_store))[skip: skip + limit],
        "total": len(_detections_store),
    }


@router.get("/recent")
async def get_recent_detections(limit: int = 10):
    return {
        "detections": list(reversed(_detections_store))[:limit]
    }


@router.get("/stats")
async def get_detection_stats():
    total = len(_detections_store)
    stopped = sum(1 for d in _detections_store if d.get("line_stopped"))
    classes = {}
    for d in _detections_store:
        cls = d.get("object_class", "unknown")
        classes[cls] = classes.get(cls, 0) + 1
    return {
        "total_detections": total,
        "lines_stopped": stopped,
        "by_class": classes,
    }
