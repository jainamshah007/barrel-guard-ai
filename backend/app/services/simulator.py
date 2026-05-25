# =============================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution of
# this file, via any medium, is strictly prohibited.
# =============================================================

import asyncio
import random
import logging
from datetime import datetime
from app.core.config import settings
from app.models.database import AsyncSessionLocal, Detection, Camera, SimulationSession
from app.websockets.manager import ws_manager
from sqlalchemy import select

logger = logging.getLogger(__name__)


class SimulatorService:
    def __init__(self):
        self.running = False
        self.auto_mode = True
        self.session_id = None
        self.total_detections = 0
        self.total_stops = 0

    async def start(self):
        self.running = True
        logger.info("Simulator started.")
        await self._create_session()
        while self.running:
            if self.auto_mode:
                await self._run_cycle()
            await asyncio.sleep(1)

    async def stop(self):
        self.running = False
        await self._close_session()
        logger.info("Simulator stopped.")

    async def _create_session(self):
        async with AsyncSessionLocal() as session:
            sim = SimulationSession(
                config={
                    "auto_mode": self.auto_mode,
                    "interval_min": settings.SIM_DEFAULT_INTERVAL_MIN,
                    "interval_max": settings.SIM_DEFAULT_INTERVAL_MAX
                }
            )
            session.add(sim)
            await session.commit()
            await session.refresh(sim)
            self.session_id = sim.id

    async def _close_session(self):
        if self.session_id:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(SimulationSession).where(SimulationSession.id == self.session_id)
                )
                sim = result.scalar_one_or_none()
                if sim:
                    sim.ended_at = datetime.utcnow()
                    sim.total_detections = self.total_detections
                    sim.total_stops = self.total_stops
                    await session.commit()

    async def _run_cycle(self):
        interval = random.randint(
            settings.SIM_DEFAULT_INTERVAL_MIN,
            settings.SIM_DEFAULT_INTERVAL_MAX
        )
        await asyncio.sleep(interval)
        await self._inject_detection()

    async def _inject_detection(self, camera_id: int = None, object_class: str = None):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Camera).where(Camera.status == "active"))
            cameras = result.scalars().all()
            if not cameras:
                return

            camera = (
                next((c for c in cameras if c.id == camera_id), None)
                if camera_id else random.choice(cameras)
            )
            if not camera:
                return

            obj_class = object_class or random.choice(settings.SIM_OBJECT_CLASSES)
            confidence = round(random.uniform(0.78, 0.99), 3)
            barrel_id = f"BRL-{random.randint(1000, 9999)}"
            batch_id  = f"BATCH-{random.randint(100, 999)}"

            detection = Detection(
                camera_id=camera.id,
                conveyor_line_id=camera.line_id,
                barrel_id=barrel_id,
                batch_id=batch_id,
                object_class=obj_class,
                confidence=confidence,
                bounding_box={
                    "x": random.randint(50, 400),
                    "y": random.randint(50, 300),
                    "w": random.randint(40, 120),
                    "h": random.randint(40, 120)
                },
                plc_triggered=camera.plc_enabled,
                severity="HIGH" if confidence > 0.85 else "MEDIUM",
                sim_injected=True
            )
            session.add(detection)
            await session.commit()
            await session.refresh(detection)
            self.total_detections += 1

            await ws_manager.broadcast({
                "type": "new_detection",
                "data": {
                    "id":               detection.id,
                    "camera_id":        detection.camera_id,
                    "conveyor_line_id": detection.conveyor_line_id,
                    "barrel_id":        detection.barrel_id,
                    "batch_id":         detection.batch_id,
                    "object_class":     detection.object_class,
                    "confidence":       detection.confidence,
                    "severity":         detection.severity,
                    "plc_triggered":    detection.plc_triggered,
                    "created_at":       detection.created_at.isoformat()
                                        if detection.created_at else None
                }
            })
            logger.info(
                f"Injected detection: {obj_class} on {camera.line_id} "
                f"(confidence={confidence})"
            )

    async def manual_inject(self, camera_id: int, object_class: str = None):
        await self._inject_detection(camera_id=camera_id, object_class=object_class)

    def set_auto_mode(self, enabled: bool):
        self.auto_mode = enabled
        logger.info(f"Simulator auto mode set to: {enabled}")
