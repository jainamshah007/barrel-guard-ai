# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

import asyncio
import uuid
from datetime import datetime
from typing import Optional, List, Dict
from app.core.config import settings


# ── PLC Line State ─────────────────────────────────────────────────────────────
class PLCLineState:
    def __init__(self, line_id: int, name: str):
        self.line_id = line_id
        self.name = name
        self.status: str = "running"        # "running" | "stopped"
        self.stopped_at: Optional[datetime] = None
        self.stopped_reason: Optional[str] = None
        self.stop_count: int = 0
        self.relay_logs: List[Dict] = []

    def to_dict(self) -> dict:
        return {
            "line_id": self.line_id,
            "name": self.name,
            "status": self.status,
            "stopped_at": self.stopped_at.isoformat() if self.stopped_at else None,
            "stopped_reason": self.stopped_reason,
            "stop_count": self.stop_count,
        }


# ── PLC Controller Service ─────────────────────────────────────────────────────
class PLCController:
    def __init__(self):
        self._ws_manager = None
        self.lines: Dict[int, PLCLineState] = {}
        self._init_lines()

    def _init_lines(self):
        for i in range(settings.NUM_CAMERAS):
            line_id = i
            name = f"Line {'A' if i % 2 == 0 else 'B'} — Conveyor {i + 1}"
            self.lines[line_id] = PLCLineState(line_id=line_id, name=name)

    def set_ws_manager(self, manager):
        self._ws_manager = manager

    async def start(self):
        """Placeholder for future real PLC connection logic."""
        pass

    async def stop_line(self, line_id: int, reason: str = "Foreign object detected") -> dict:
        if line_id not in self.lines:
            return {"error": f"Line {line_id} not found"}

        line = self.lines[line_id]
        line.status = "stopped"
        line.stopped_at = datetime.utcnow()
        line.stopped_reason = reason
        line.stop_count += 1

        log_entry = {
            "id": str(uuid.uuid4()),
            "line_id": line_id,
            "event": "STOP",
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
        }
        line.relay_logs.append(log_entry)

        # Broadcast via WebSocket
        if self._ws_manager:
            await self._ws_manager.broadcast({
                "type": "plc_stop",
                "payload": {
                    **line.to_dict(),
                    "log": log_entry,
                },
            })

        return line.to_dict()

    async def resume_line(self, line_id: int) -> dict:
        if line_id not in self.lines:
            return {"error": f"Line {line_id} not found"}

        line = self.lines[line_id]
        line.status = "running"
        line.stopped_at = None
        line.stopped_reason = None

        log_entry = {
            "id": str(uuid.uuid4()),
            "line_id": line_id,
            "event": "RESUME",
            "reason": "Manual resume",
            "timestamp": datetime.utcnow().isoformat(),
        }
        line.relay_logs.append(log_entry)

        # Broadcast via WebSocket
        if self._ws_manager:
            await self._ws_manager.broadcast({
                "type": "plc_resume",
                "payload": {
                    **line.to_dict(),
                    "log": log_entry,
                },
            })

        return line.to_dict()

    def get_all_status(self) -> List[dict]:
        return [line.to_dict() for line in self.lines.values()]

    def get_line_status(self, line_id: int) -> Optional[dict]:
        if line_id not in self.lines:
            return None
        return self.lines[line_id].to_dict()

    def get_relay_logs(self, line_id: int = None) -> List[dict]:
        if line_id is not None:
            if line_id not in self.lines:
                return []
            return self.lines[line_id].relay_logs
        all_logs = []
        for line in self.lines.values():
            all_logs.extend(line.relay_logs)
        all_logs.sort(key=lambda x: x["timestamp"], reverse=True)
        return all_logs


# ── Singleton instance (imported by routes) ────────────────────────────────────
plc_controller = PLCController()