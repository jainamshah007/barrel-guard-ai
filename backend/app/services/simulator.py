# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

import asyncio
import random
import uuid
from datetime import datetime
from typing import Optional
from app.core.config import settings

# ── Simulation state object (imported by routes) ──────────────────────────────
class SimulationState:
    def __init__(self):
        self.running: bool = False
        self.auto_mode: bool = True
        self.interval: float = settings.SIMULATION_INTERVAL
        self.num_cameras: int = settings.NUM_CAMERAS
        self.injection_count: int = 0
        self.session_start: Optional[datetime] = None

sim_state = SimulationState()

# ── Foreign object classes ─────────────────────────────────────────────────────
OBJECT_CLASSES = [
    "hard_helmet",
    "glove",
    "face_mask",
    "key",
    "wallet",
    "bottle",
    "tool",
    "cloth",
]

CAMERA_NAMES = [
    f"Camera {i+1} — Line {'A' if i % 2 == 0 else 'B'}"
    for i in range(settings.NUM_CAMERAS)
]


# ── Simulator service ──────────────────────────────────────────────────────────
class SimulatorService:
    def __init__(self):
        self._task: Optional[asyncio.Task] = None
        self._ws_manager = None
        self._db_callback = None

    def set_ws_manager(self, manager):
        self._ws_manager = manager

    def set_db_callback(self, callback):
        self._db_callback = callback

    async def start(self):
        if not settings.SIMULATION_ENABLED:
            return
        sim_state.running = True
        sim_state.session_start = datetime.utcnow()
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        sim_state.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def inject_detection(self, camera_id: int = None, object_class: str = None):
        cam_id = camera_id if camera_id is not None else random.randint(0, settings.NUM_CAMERAS - 1)
        obj_class = object_class if object_class else random.choice(OBJECT_CLASSES)
        confidence = round(random.uniform(0.82, 0.99), 3)

        detection = {
            "id": str(uuid.uuid4()),
            "camera_id": cam_id,
            "camera_name": CAMERA_NAMES[cam_id] if cam_id < len(CAMERA_NAMES) else f"Camera {cam_id}",
            "object_class": obj_class,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat(),
            "bbox": {
                "x": random.randint(50, 400),
                "y": random.randint(50, 300),
                "width": random.randint(40, 120),
                "height": random.randint(40, 120),
            },
            "line_stopped": confidence > 0.90,
        }

        sim_state.injection_count += 1

        # Broadcast via WebSocket
        if self._ws_manager:
            await self._ws_manager.broadcast({
                "type": "new_detection",
                "payload": detection,
            })

        # Persist to DB
        if self._db_callback:
            await self._db_callback(detection)

        return detection

    async def _run_loop(self):
        while sim_state.running and sim_state.auto_mode:
            try:
                await asyncio.sleep(sim_state.interval)
                if sim_state.running and sim_state.auto_mode:
                    await self.inject_detection()
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(2)


simulator = SimulatorService()