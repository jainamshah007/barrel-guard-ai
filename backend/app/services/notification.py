# =============================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution of
# this file, via any medium, is strictly prohibited.
# =============================================================

import asyncio
import logging
from datetime import datetime
from app.models.database import (
    AsyncSessionLocal, NotificationRule,
    NotificationLog, Detection
)
from app.websockets.manager import ws_manager
from sqlalchemy import select

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.running = False
        self.processed_ids = set()

    async def start(self):
        self.running = True
        logger.info("Notification service started.")
        while self.running:
            await self._check_new_detections()
            await asyncio.sleep(3)

    async def stop(self):
        self.running = False
        logger.info("Notification service stopped.")

    async def _check_new_detections(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Detection)
                .where(Detection.acknowledged == False)
                .order_by(Detection.created_at.desc())
                .limit(20)
            )
            detections = result.scalars().all()

            rules_result = await session.execute(
                select(NotificationRule).where(NotificationRule.enabled == True)
            )
            rules = rules_result.scalars().all()

            for detection in detections:
                if detection.id in self.processed_ids:
                    continue
                self.processed_ids.add(detection.id)

                for rule in rules:
                    if rule.severity_filter in (detection.severity, "ALL"):
                        await self._send_notification(session, rule, detection)

    async def _send_notification(self, session, rule, detection):
        message = (
            f"[{detection.severity}] Foreign object detected: "
            f"{detection.object_class} on {detection.conveyor_line_id} | "
            f"Barrel: {detection.barrel_id} | "
            f"Confidence: {detection.confidence:.0%}"
        )

        log = NotificationLog(
            rule_id=rule.id,
            detection_id=detection.id,
            channel=rule.channel,
            recipient=rule.recipient,
            message=message,
            status="sent",
            sent_at=datetime.utcnow()
        )
        session.add(log)
        await session.commit()

        await ws_manager.broadcast({
            "type": "notification",
            "data": {
                "id":          detection.id,
                "severity":    detection.severity,
                "object_class":detection.object_class,
                "line_id":     detection.conveyor_line_id,
                "barrel_id":   detection.barrel_id,
                "confidence":  detection.confidence,
                "message":     message,
                "channel":     rule.channel,
                "sent_at":     log.sent_at.isoformat()
            }
        })
        logger.info(f"Notification sent: {message}")
