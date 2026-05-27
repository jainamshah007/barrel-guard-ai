# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.database import init_db, AsyncSessionLocal, Detection, Notification
from app.websockets.manager import ws_manager
from app.services.simulator import simulator, sim_state
from app.services.plc_controller import plc_controller
from app.services.notification import notification_service
from app.api.routes import detections, cameras, simulation, analytics, plc, notifications

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def save_detection_to_db(detection: dict):
    try:
        async with AsyncSessionLocal() as session:
            db_detection = Detection(
                camera_id=detection["camera_id"],
                camera_name=detection["camera_name"],
                object_class=detection["object_class"],
                confidence=detection["confidence"],
                line_id=detection["line_id"],
                barrel_id=detection.get("barrel_id"),
                batch_id=detection.get("batch_id"),
                bbox_x=detection.get("bbox", {}).get("x"),
                bbox_y=detection.get("bbox", {}).get("y"),
                bbox_width=detection.get("bbox", {}).get("width"),
                bbox_height=detection.get("bbox", {}).get("height"),
            )
            session.add(db_detection)
            await session.commit()
            await notification_service.notify_detection(detection)
    except Exception as e:
        logger.error(f"Failed to save detection: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("BARREL-GUARD AI starting up...")
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"DB init failed: {e}")

    simulator.set_ws_manager(ws_manager)
    simulator.set_detection_callback(save_detection_to_db)
    plc_controller.set_ws_manager(ws_manager)
    notification_service.set_ws_manager(ws_manager)

    try:
        await simulator.start()
        logger.info("Simulator started")
    except Exception as e:
        logger.error(f"Simulator start failed: {e}")

    yield

    await simulator.stop()
    logger.info("BARREL-GUARD AI shut down")

app = FastAPI(
    title="BARREL-GUARD AI",
    description="Foreign Object Detection Platform — Copyright (c) 2024 Jainam K Shah",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detections.router, prefix="/api/v1/detections", tags=["detections"])
app.include_router(cameras.router, prefix="/api/v1/cameras", tags=["cameras"])
app.include_router(simulation.router, prefix="/api/v1/simulation", tags=["simulation"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(plc.router, prefix="/api/v1/plc", tags=["plc"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "BARREL-GUARD AI",
        "version": "1.0.0",
        "simulation_running": sim_state.running,
        "total_detections": sim_state.total_injected
    }

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)
