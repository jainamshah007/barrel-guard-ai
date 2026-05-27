# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

import asyncio
import random
import logging
from datetime import datetime
from typing import Optional, List, Callable

logger = logging.getLogger(__name__)

OBJECT_CLASSES = ["hard_helmet", "glove", "mask", "keys", "wallet", "tool", "bottle"]
CAMERA_NAMES = {
    0: "Camera 1 - Line A",
    1: "Camera 2 - Line B"
}

class SimulationState:
    def __init__(self):
        self.running = False
        self.auto_mode = True
        self.interval = 5.0
        self.num_cameras = 2
        self.total_injected = 0

sim_state = SimulationState()

class SimulatorService:
    def __init__(self):
        self.task: Optional[asyncio.Task] = None
        self.on_detection: Optional[Callable] = None
        self.ws_manager = None

    def set_ws_manager(self, manager):
        self.ws_manager = manager

    def set_detection_callback(self, callback: Callable):
        self.on_detection = callback

    async def start(self):
        if not sim_state.running:
            sim_state.running = True
            self.task = asyncio.create_task(self._run_loop())
            logger.info("Simulator started")

    async def stop(self):
        sim_state.running = False
        if self.task:
            self.task.cancel()
            self.task = None
        logger.info("Simulator stopped")

    async def _run_loop(self):
        while sim_state.running:
            try:
                if sim_state.auto_mode:
                    await self.inject_detection()
                await asyncio.sleep(sim_state.interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Simulator error: {e}")
                await asyncio.sleep(1)

    async def inject_detection(
        self,
        camera_id: Optional[int] = None,
        object_class: Optional[str] = None
    ):
        cam_id = camera_id if camera_id is not None else random.randint(0, sim_state.num_cameras - 1)
        obj_class = object_class if object_class in OBJECT_CLASSES else random.choice(OBJECT_CLASSES)
        confidence = round(random.uniform(0.75, 0.99), 3)
        now = datetime.utcnow().isoformat()

        detection = {
            "id": random.randint(1000, 9999),
            "camera_id": cam_id,
            "camera_name": CAMERA_NAMES.get(cam_id, f"Camera {cam_id + 1}"),
            "object_class": obj_class,
            "confidence": confidence,
            "timestamp": now,
            "line_id": "line_a" if cam_id == 0 else "line_b",
            "barrel_id": f"BARREL-{random.randint(100, 999)}",
            "batch_id": f"BATCH-{random.randint(10, 99)}",
            "bbox": {
                "x": random.randint(50, 400),
                "y": random.randint(50, 300),
                "width": random.randint(40, 120),
                "height": random.randint(40, 120)
            }
        }

        sim_state.total_injected += 1

        # Broadcast via WebSocket
        if self.ws_manager:
            await self.ws_manager.broadcast({
                "type": "new_detection",
                "payload": detection
            })

        # Save to DB via callback
        if self.on_detection:
            try:
                await self.on_detection(detection)
            except Exception as e:
                logger.error(f"Detection callback error: {e}")

        logger.info(f"Injected: {obj_class} on {CAMERA_NAMES.get(cam_id)} confidence={confidence}")
        return detection

simulator = SimulatorService()