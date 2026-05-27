# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

import asyncio
import logging
from datetime import datetime
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self._ws_manager = None
        self.notifications: List[Dict] = []
        self.rules: List[Dict] = [
            {
                "id": "rule_001",
                "name": "High Confidence Alert",
                "enabled": True,
                "threshold": 0.90,
                "channels": ["dashboard"],
            }
        ]

    def set_ws_manager(self, manager):
        self._ws_manager = manager

    async def send_notification(
        self,
        title: str,
        message: str,
        severity: str = "warning",
        detection_id: Optional[str] = None,
    ):
        notification = {
            "id": f"notif_{len(self.notifications) + 1:04d}",
            "title": title,
            "message": message,
            "severity": severity,
            "detection_id": detection_id,
            "timestamp": datetime.utcnow().isoformat(),
            "read": False,
        }
        self.notifications.append(notification)

        if self._ws_manager:
            await self._ws_manager.broadcast({
                "type": "notification",
                "payload": notification,
            })

        logger.info(f"Notification sent: {title}")
        return notification

    def get_notifications(
        self,
        unread_only: bool = False,
        limit: int = 50,
    ) -> List[Dict]:
        notifs = self.notifications
        if unread_only:
            notifs = [n for n in notifs if not n["read"]]
        return list(reversed(notifs))[:limit]

    def mark_read(self, notification_id: str) -> bool:
        for n in self.notifications:
            if n["id"] == notification_id:
                n["read"] = True
                return True
        return False

    def mark_all_read(self):
        for n in self.notifications:
            n["read"] = True

    def get_rules(self) -> List[Dict]:
        return self.rules

    def get_unread_count(self) -> int:
        return sum(1 for n in self.notifications if not n["read"])


notification_service = NotificationService()
