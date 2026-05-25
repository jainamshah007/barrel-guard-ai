# =============================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# =============================================================

from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class DetectionOut(BaseModel):
    id: int
    camera_id: Optional[int]
    conveyor_line_id: Optional[str]
    barrel_id: Optional[str]
    batch_id: Optional[str]
    object_class: str
    confidence: float
    bounding_box: Optional[Any]
    plc_triggered: Optional[bool]
    severity: Optional[str]
    acknowledged: Optional[bool]
    acknowledged_by: Optional[str]
    is_false_positive: Optional[bool]
    sim_injected: Optional[bool]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class AckRequest(BaseModel):
    operator_name: str
    notes: Optional[str] = None
    is_false_positive: bool = False


class CameraOut(BaseModel):
    id: int
    name: str
    line_id: str
    description: Optional[str]
    confidence_threshold: float
    plc_enabled: bool
    sim_auto_inject: bool
    sim_frequency_sec: int
    status: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    confidence_threshold: Optional[float] = None
    plc_enabled: Optional[bool] = None
    sim_auto_inject: Optional[bool] = None
    sim_frequency_sec: Optional[int] = None
    status: Optional[str] = None


class InjectRequest(BaseModel):
    camera_id: int
    object_class: Optional[str] = None


class SimConfigRequest(BaseModel):
    auto_mode: bool
    interval_min: Optional[int] = None
    interval_max: Optional[int] = None


class PLCCommand(BaseModel):
    line_id: str
    operator: Optional[str] = "OPERATOR"
    notes: Optional[str] = None