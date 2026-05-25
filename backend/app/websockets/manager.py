# =============================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution of
# this file, via any medium, is strictly prohibited.
# =============================================================

import json
import logging
from typing import Dict
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"WebSocket connected: {client_id}")

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
        logger.info(f"WebSocket disconnected: {client_id}")

    async def broadcast(self, message: dict):
        disconnected = []
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.warning(f"Failed to send to {client_id}: {e}")
                disconnected.append(client_id)
        for client_id in disconnected:
            self.disconnect(client_id)

    async def send_personal(self, client_id: str, message: dict):
        websocket = self.active_connections.get(client_id)
        if websocket:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.warning(f"Failed to send personal to {client_id}: {e}")
                self.disconnect(client_id)


ws_manager = WebSocketManager()
