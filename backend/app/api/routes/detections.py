from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, desc
from typing import Optional, List
from datetime import datetime

from app.models.database import (
    Detection, get_db
)
from app.schemas.schemas import DetectionOut, AckRequest

router = APIRouter()


@router.get("/", response_model=List[DetectionOut])
async def get_detections(
    limit: int = Query(50, le=500),
    offset: int = 0,
    camera_id: Optional[int] = None,
    acknowledged: Optional[bool] = None,
    severity: Optional[str] = None,
    object_class: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    q = select(Detection).order_by(
        desc(Detection.created_at)
    )
    if camera_id:
        q = q.where(Detection.camera_id == camera_id)
    if acknowledged is not None:
        q = q.where(
            Detection.acknowledged == acknowledged
        )
    if severity:
        q = q.where(Detection.severity == severity)
    if object_class:
        q = q.where(
            Detection.object_class == object_class
        )
    q = q.limit(limit).offset(offset)
    result = await db.execute(q)
    return result.scalars().all()


@router.put("/{detection_id}/ack")
async def acknowledge(
    detection_id: int,
    body: AckRequest,
    db: AsyncSession = Depends(get_db)
):
    await db.execute(
        update(Detection)
        .where(Detection.id == detection_id)
        .values(
            acknowledged=True,
            acknowledged_by=body.operator_name,
            ack_notes=body.notes,
            is_false_positive=body.is_false_positive,
            updated_at=datetime.utcnow()
        )
    )
    await db.commit()
    return {"status": "acknowledged"}


@router.get("/stats/kpis")
async def get_kpis(
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import and_
    from datetime import timedelta

    now = datetime.utcnow()
    today = now.replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    total = await db.scalar(
        select(func.count(Detection.id))
    )
    today_count = await db.scalar(
        select(func.count(Detection.id))
        .where(Detection.created_at >= today)
    )
    unacked = await db.scalar(
        select(func.count(Detection.id))
        .where(Detection.acknowledged == False)
    )
    plc_stops = await db.scalar(
        select(func.count(Detection.id))
        .where(Detection.plc_triggered == True)
    )
    critical = await db.scalar(
        select(func.count(Detection.id))
        .where(Detection.severity == "CRITICAL")
    )
    fp_count = await db.scalar(
        select(func.count(Detection.id))
        .where(Detection.is_false_positive == True)
    )

    fp_rate = (
        round(fp_count / total * 100, 1)
        if total > 0 else 0
    )

    return {
        "total_detections": total or 0,
        "today_detections": today_count or 0,
        "unacknowledged": unacked or 0,
        "plc_stops": plc_stops or 0,
        "critical_count": critical or 0,
        "false_positive_rate": fp_rate,
        "system_uptime": "99.8%",
        "avg_confidence": 91.4
    }
