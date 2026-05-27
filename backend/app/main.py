# ==============================================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.
# ==============================================================================

import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.models.database import init_db
from app.websockets.manager import ws_manager
from app.services.simulator import simulator
from app.services.plc_controller import plc_controller
from app.services.notification import notification_service
from app.api.routes import detections, cameras, simulation, analytics, plc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ────────────────────────────────────────────────────────────────
    logger.info("BARREL-GUARD AI starting up...")
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database init failed: {e}")

    try:
        simulator.set_ws_manager(ws_manager)
        plc_controller.set_ws_manager(ws_manager)
        notification_service.set_ws_manager(ws_manager)
        if settings.SIMULATION_ENABLED:
            asyncio.create_task(simulator.start())
            logger.info("Simulator started")
    except Exception as e:
        logger.error(f"Service startup failed: {e}")

    yield

    # ── Shutdown ───────────────────────────────────────────────────────────────
    logger.info("BARREL-GUARD AI shutting down...")
    await simulator.stop()


app = FastAPI(
    title="BARREL-GUARD AI",
    description="Foreign Object Detection Platform — Copyright (c) 2024 Jainam K Shah",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(detections.router, prefix="/api/v1")
app.include_router(cameras.router, prefix="/api/v1")
app.include_router(simulation.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(plc.router, prefix="/api/v1")


# ── WebSocket ──────────────────────────────────────────────────────────────────
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)


# ── Health ─────────────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "BARREL-GUARD AI",
        "version": "1.0.0",
        "copyright": "Copyright (c) 2024 Jainam K Shah",
    }


@app.get("/")
async def root():
    return {
        "message": "BARREL-GUARD AI — Foreign Object Detection Platform",
        "docs": "/docs",
        "health": "/health",
    }
