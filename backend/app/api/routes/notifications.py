# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

from fastapi import APIRouter
from app.services.notification import notification_service

router = APIRouter()

@router.get("")
async def get_notifications(limit: int = 50):
    return {
        "notifications": notification_service.get_notifications(limit),
        "total": len(notification_service.notifications)
    }

@router.post("/mark-read")
async def mark_all_read():
    notification_service.mark_all_read()
    return {"message": "All notifications marked as read"}
