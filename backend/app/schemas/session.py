"""Session & rep schemas"""
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import RepQuality, SessionStatus


class SessionCreate(BaseModel):
    plan_id: int | None = None
    device_info: str | None = Field(default=None, max_length=255)


class SessionUpdate(BaseModel):
    status: SessionStatus | None = None
    total_reps: int | None = None
    accuracy_score_avg: Decimal | None = None


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    plan_id: int | None = None
    started_at: datetime
    ended_at: datetime | None = None
    status: SessionStatus
    total_reps: int
    accuracy_score_avg: Decimal | None = None
    device_info: str | None = None


class SessionRepCreate(BaseModel):
    exercise_id: int
    rep_number: int = Field(ge=1)
    accuracy_score: Decimal | None = Field(default=None, ge=0, le=100)
    max_rom: Decimal | None = Field(default=None, ge=0)
    duration_ms: int | None = Field(default=None, ge=0)
    quality: RepQuality = RepQuality.ACCEPTABLE
    feedback: str | None = None


class SessionRepOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    session_id: int
    exercise_id: int
    rep_number: int
    accuracy_score: Decimal | None = None
    max_rom: Decimal | None = None
    duration_ms: int | None = None
    quality: RepQuality
    feedback: str | None = None


class JointAngleCreate(BaseModel):
    """มุมข้อต่อหนึ่งจุด ณ เวลาหนึ่ง — ค่า JSON จาก On-device processing"""
    timestamp_ms: int = Field(ge=0)
    joint_name: str = Field(max_length=50)
    angle_value: Decimal = Field(ge=0, le=360)
    rep_id: int | None = None


class JointAngleBatch(BaseModel):
    """ส่งเป็นชุด — รองรับการ stream และ offline sync"""
    angles: list[JointAngleCreate]
