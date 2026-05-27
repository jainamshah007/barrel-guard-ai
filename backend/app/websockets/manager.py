 
# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

import json
import logging
from fastapi import WebSocket
from typing import Dict

logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"WebSocket connected: {client_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"WebSocket disconnected: {client_id}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        data = json.dumps(message)
        disconnected = []
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(data)
            except Exception:
                disconnected.append(client_id)
        for client_id in disconnected:
            self.disconnect(client_id)

    async def send_to(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(
                    json.dumps(message)
                )
            except Exception:
                self.disconnect(client_id)


ws_manager = WebSocketManager()
