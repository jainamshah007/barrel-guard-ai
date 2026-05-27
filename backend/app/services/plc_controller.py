# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class PLCLineState:
    def __init__(self, line_id: str, name: str):
        self.line_id = line_id
        self.name = name
        self.status = "running"
        self.stopped_at: Optional[str] = None
        self.reason: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "line_id": self.line_id,
            "name": self.name,
            "status": self.status,
            "stopped_at": self.stopped_at,
            "reason": self.reason
        }

class PLCController:
    def __init__(self):
        self.lines: Dict[str, PLCLineState] = {
            "line_a": PLCLineState("line_a", "Conveyor Line A"),
            "line_b": PLCLineState("line_b", "Conveyor Line B"),
        }
        self.logs: List[dict] = []
        self.ws_manager = None

    def set_ws_manager(self, manager):
        self.ws_manager = manager

    def get_all_status(self) -> dict:
        return {
            "lines": {k: v.to_dict() for k, v in self.lines.items()},
            "total_stops": len([l for l in self.logs if l["event"] == "stop"])
        }

    def get_logs(self) -> List[dict]:
        return self.logs[-50:]

    async def stop_line(self, line_id: str, reason: str = "Manual stop") -> dict:
        # Accept both formats: "line_a" and "1" or "2"
        line_id = self._normalize_line_id(line_id)
        if line_id not in self.lines:
            raise ValueError(f"Unknown line_id: {line_id}. Valid: {list(self.lines.keys())}")
        line = self.lines[line_id]
        line.status = "stopped"
        line.stopped_at = datetime.utcnow().isoformat()
        line.reason = reason
        log_entry = {
            "event": "stop",
            "line_id": line_id,
            "name": line.name,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logs.append(log_entry)
        if self.ws_manager:
            await self.ws_manager.broadcast({
                "type": "plc_stop",
                "payload": line.to_dict()
            })
        logger.info(f"Line {line_id} stopped: {reason}")
        return {"success": True, "line": line.to_dict()}

    async def resume_line(self, line_id: str) -> dict:
        line_id = self._normalize_line_id(line_id)
        if line_id not in self.lines:
            raise ValueError(f"Unknown line_id: {line_id}. Valid: {list(self.lines.keys())}")
        line = self.lines[line_id]
        line.status = "running"
        line.stopped_at = None
        line.reason = None
        log_entry = {
            "event": "resume",
            "line_id": line_id,
            "name": line.name,
            "reason": "Manual resume",
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logs.append(log_entry)
        if self.ws_manager:
            await self.ws_manager.broadcast({
                "type": "plc_resume",
                "payload": line.to_dict()
            })
        logger.info(f"Line {line_id} resumed")
        return {"success": True, "line": line.to_dict()}

    def _normalize_line_id(self, line_id: str) -> str:
        """Accept line_a, line_b, 1, 2, Line A, Line B etc."""
        mapping = {
            "1": "line_a", "2": "line_b",
            "line_1": "line_a", "line_2": "line_b",
            "line a": "line_a", "line b": "line_b",
            "a": "line_a", "b": "line_b",
        }
        normalized = line_id.lower().strip()
        return mapping.get(normalized, normalized)

plc_controller = PLCController()