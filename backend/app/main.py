# =============================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution of
# this file, via any medium, is strictly prohibited.
# =============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging

from app.core.config import settings
from app.models.database import init_db
from app.services.simulator import SimulatorService
from app.services.plc_controller import PLCController
from app.services.notification import NotificationService
from app.websockets.manager import ws_manager
from app.api.routes import detections, cameras, simulation, analytics, plc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

simulator_service = SimulatorService()
plc_controller = PLCController()
notification_service = NotificationService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting BARREL-GUARD AI Platform...")
    await init_db()
    asyncio.create_task(simulator_service.start())
    asyncio.create_task(plc_controller.start())
    asyncio.create_task(notification_service.start())
    yield
    logger.info("Shutting down BARREL-GUARD AI Platform...")
    await simulator_service.stop()
    await plc_controller.stop()
    await notification_service.stop()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Foreign Object Detection Platform for Industrial Conveyor Lines. "
        "Copyright (c) 2024 Jainam K Shah. All Rights Reserved."
    ),
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://barrel-guard-ai.vercel.app",
        settings.FRONTEND_URL,
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(detections.router, prefix="/api/v1", tags=["Detections"])
app.include_router(cameras.router,    prefix="/api/v1", tags=["Cameras"])
app.include_router(simulation.router, prefix="/api/v1", tags=["Simulation"])
app.include_router(analytics.router,  prefix="/api/v1", tags=["Analytics"])
app.include_router(plc.router,        prefix="/api/v1", tags=["PLC"])

# WebSocket endpoint
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "copyright": "Copyright (c) 2024 Jainam K Shah. All Rights Reserved."
    }
