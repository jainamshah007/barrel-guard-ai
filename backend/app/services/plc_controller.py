# =============================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution of
# this file, via any medium, is strictly prohibited.
# =============================================================

import asyncio
import logging
from datetime import datetime
from app.core.config import settings
from app.models.database import AsyncSessionLocal, ConveyorStopEvent
from app.websockets.manager import ws_manager

logger = logging.getLogger(__name__)


class PLCController:
    def __init__(self):
        self.running = False
        self.line_states = {
            "LINE_A": {"status": "RUNNING", "stopped_at": None, "stop_event_id": None},
            "LINE_B": {"status": "RUNNING", "stopped_at": None, "stop_event_id": None}
        }

    async def start(self):
        self.running = True
        logger.info("PLC Controller started.")
        while self.running:
            await self._broadcast_status()
            await asyncio.sleep(5)

    async def stop(self):
        self.running = False
        logger.info("PLC Controller stopped.")

    async def _broadcast_status(self):
        await ws_manager.broadcast({
            "type": "plc_status",
            "data": {
                line: {
                    "status":     state["status"],
                    "stopped_at": state["stopped_at"].isoformat()
                                  if state["stopped_at"] else None
                }
                for line, state in self.line_states.items()
            }
        })

    async def stop_line(
        self,
        line_id: str,
        detection_id: int = None,
        operator: str = "SYSTEM",
        reason: str = "Foreign object detected"
    ):
        if line_id not in self.line_states:
            logger.warning(f"Unknown line_id: {line_id}")
            return None

        self.line_states[line_id]["status"]     = "STOPPED"
        self.line_states[line_id]["stopped_at"] = datetime.utcnow()

        async with AsyncSessionLocal() as session:
            event = ConveyorStopEvent(
                line_id=line_id,
                detection_id=detection_id,
                triggered_by=operator,
                stop_reason=reason,
                stopped_at=datetime.utcnow()
            )
            session.add(event)
            await session.commit()
            await session.refresh(event)
            self.line_states[line_id]["stop_event_id"] = event.id

        await ws_manager.broadcast({
            "type": "plc_stop",
            "data": {
                "line_id":    line_id,
                "operator":   operator,
                "reason":     reason,
                "stopped_at": self.line_states[line_id]["stopped_at"].isoformat()
            }
        })
        logger.info(f"Line {line_id} STOPPED by {operator}. Reason: {reason}")
        return event.id

    async def resume_line(
        self,
        line_id: str,
        operator: str = "OPERATOR"
    ):
        if line_id not in self.line_states:
            return

        stopped_at = self.line_states[line_id].get("stopped_at")
        duration   = (
            (datetime.utcnow() - stopped_at).total_seconds()
            if stopped_at else None
        )

        self.line_states[line_id]["status"]     = "RUNNING"
        self.line_states[line_id]["stopped_at"] = None

        event_id = self.line_states[line_id].get("stop_event_id")
        if event_id:
            async with AsyncSessionLocal() as session:
                from sqlalchemy import select
                result = await session.execute(
                    select(ConveyorStopEvent).where(ConveyorStopEvent.id == event_id)
                )
                event = result.scalar_one_or_none()
                if event:
                    event.resumed_at        = datetime.utcnow()
                    event.duration_seconds  = duration
                    event.operator          = operator
                    await session.commit()

        await ws_manager.broadcast({
            "type": "plc_resume",
            "data": {
                "line_id":   line_id,
                "operator":  operator,
                "resumed_at": datetime.utcnow().isoformat(),
                "duration":  duration
            }
        })
        logger.info(f"Line {line_id} RESUMED by {operator}.")

    def get_status(self):
        return {
            line: {
                "status":     state["status"],
                "stopped_at": state["stopped_at"].isoformat()
                              if state["stopped_at"] else None
            }
            for line, state in self.line_states.items()
        }
