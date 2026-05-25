from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, text
from datetime import datetime, timedelta
from app.models.database import Detection, get_db

router = APIRouter()


@router.get("/trends")
async def get_trends(
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    since = datetime.utcnow() - timedelta(days=days)

    # Hourly (today)
    today = datetime.utcnow().replace(
        hour=0, minute=0, second=0
    )
    hourly_result = await db.execute(
        select(
            func.strftime('%H', Detection.created_at)
            .label('hour'),
            func.count(Detection.id).label('count')
        )
        .where(Detection.created_at >= today)
        .group_by(
            func.strftime('%H', Detection.created_at)
        )
        .order_by('hour')
    )
    hourly = [
        {"hour": int(r.hour), "count": r.count}
        for r in hourly_result
    ]

    # Daily
    daily_result = await db.execute(
        select(
            func.strftime(
                '%Y-%m-%d', Detection.created_at
            ).label('date'),
            func.count(Detection.id).label('count')
        )
        .where(Detection.created_at >= since)
        .group_by(
            func.strftime(
                '%Y-%m-%d', Detection.created_at
            )
        )
        .order_by('date')
    )
    daily = [
        {"date": r.date, "count": r.count}
        for r in daily_result
    ]

    # By class
    class_result = await db.execute(
        select(
            Detection.object_class.label('class'),
            func.count(Detection.id).label('count')
        )
        .where(Detection.created_at >= since)
        .group_by(Detection.object_class)
        .order_by(desc('count'))
    )
    by_class = [
        {"class": r.class_, "count": r.count}
        for r in class_result
    ]

    # By line
    line_result = await db.execute(
        select(
            Detection.conveyor_line_id.label('line'),
            func.count(Detection.id).label('count')
        )
        .where(Detection.created_at >= since)
        .group_by(Detection.conveyor_line_id)
    )
    by_line = [
        {"line": r.line or "Unknown", "count": r.count}
        for r in line_result
    ]

    # Confidence distribution
    conf_result = await db.execute(
        select(Detection.confidence)
        .where(Detection.created_at >= since)
    )
    confs = [r[0] for r in conf_result]
    ranges = [
        "50-60%", "60-70%", "70-80%",
        "80-90%", "90-95%", "95-100%"
    ]
    bounds = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.01]
    conf_dist = []
    for i, label in enumerate(ranges):
        count = sum(
            1 for c in confs
            if bounds[i] <= c < bounds[i + 1]
        )
        conf_dist.append({"range": label, "count": count})

    return {
        "hourly": hourly,
        "daily": daily,
        "by_class": by_class,
        "by_line": by_line,
        "confidence_dist": conf_dist
    }


@router.get("/heatmap")
async def get_heatmap(
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    since = datetime.utcnow() - timedelta(days=days)
    result = await db.execute(
        select(
            func.strftime(
                '%H', Detection.created_at
            ).label('hour'),
            func.strftime(
                '%w', Detection.created_at
            ).label('weekday'),
            func.count(Detection.id).label('count')
        )
        .where(Detection.created_at >= since)
        .group_by('hour', 'weekday')
    )
    heatmap = [
        {
            "hour": int(r.hour),
            "weekday": int(r.weekday),
            "count": r.count
        }
        for r in result
    ]
    return {"heatmap": heatmap}


@router.get("/summary-table")
async def get_summary(
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    since = datetime.utcnow() - timedelta(days=days)
    result = await db.execute(
        select(
            Detection.object_class,
            func.count(Detection.id).label('total'),
            func.avg(Detection.confidence).label('avg_conf'),
            func.sum(
                func.cast(
                    Detection.is_false_positive, int
                )
            ).label('fp_count'),
            func.sum(
                func.cast(Detection.plc_triggered, int)
            ).label('stops')
        )
        .where(Detection.created_at >= since)
        .group_by(Detection.object_class)
        .order_by(desc('total'))
    )
    rows = []
    for r in result:
        total = r.total or 0
        fp = r.fp_count or 0
        rows.append({
            "object_class": r.object_class,
            "total": total,
            "avg_confidence": round(
                (r.avg_conf or 0) * 100, 1
            ),
            "fp_rate": round(
                fp / total * 100, 1
            ) if total > 0 else 0,
            "stops_triggered": r.stops or 0
        })
    return {"rows": rows}
