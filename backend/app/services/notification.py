# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

import asyncio
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.ws_manager = None
        self.notifications = []

    def set_ws_manager(self, manager):
        self.ws_manager = manager

    async def create_notification(
        self,
        title: str,
        message: str,
        severity: str = "warning",
        camera_id: Optional[int] = None,
        object_class: Optional[str] = None
    ):
        notification = {
            "id": len(self.notifications) + 1,
            "title": title,
            "message": message,
            "severity": severity,
            "camera_id": camera_id,
            "object_class": object_class,
            "is_read": False,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.notifications.append(notification)

        if self.ws_manager:
            await self.ws_manager.broadcast({
                "type": "notification",
                "payload": notification
            })

        logger.info(f"Notification created: {title}")
        return notification

    async def notify_detection(self, detection: dict):
        camera_name = detection.get("camera_name", "Unknown Camera")
        object_class = detection.get("object_class", "unknown")
        confidence = detection.get("confidence", 0)
        barrel_id = detection.get("barrel_id", "Unknown")
        batch_id = detection.get("batch_id", "Unknown")

        await self.create_notification(
            title=f"⚠️ Foreign Object Detected — {camera_name}",
            message=(
                f"Object: {object_class.replace('_', ' ').title()} | "
                f"Confidence: {confidence:.1%} | "
                f"Barrel: {barrel_id} | "
                f"Batch: {batch_id}"
            ),
            severity="critical" if confidence > 0.9 else "warning",
            camera_id=detection.get("camera_id"),
            object_class=object_class
        )

    def get_notifications(self, limit: int = 50):
        return self.notifications[-limit:]

    def mark_all_read(self):
        for n in self.notifications:
            n["is_read"] = True

notification_service = NotificationService()
