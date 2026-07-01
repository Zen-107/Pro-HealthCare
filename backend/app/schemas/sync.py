"""Sync schemas — สำหรับ Offline Mode (sync queue จากมือถือ)"""
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.session import JointAngleCreate, SessionRepCreate


class SyncSessionPayload(BaseModel):
    """เซสชันหนึ่งที่ต้องการ sync (อาจจบแล้วหรือยังทำอยู่)"""
    client_session_id: str = Field(max_length=64)  # id ฝั่ง client สำหรับ dedupe
    plan_id: int | None = None
    started_at: datetime
    ended_at: datetime | None = None
    status: str = "completed"
    total_reps: int = 0
    accuracy_score_avg: float | None = None
    device_info: str | None = None
    reps: list[SessionRepCreate] = []
    angles: list[JointAngleCreate] = []


class SyncBatchRequest(BaseModel):
    """กลุ่มเซสชันที่คั่งในมือถือ ส่งขึ้นมาพร้อมกันเมื่อมีเครือข่าย"""
    sessions: list[SyncSessionPayload]


class SyncSessionResult(BaseModel):
    client_session_id: str
    server_session_id: int | None
    status: str  # created / skipped / error
    message: str | None = None


class SyncBatchResult(BaseModel):
    total: int
    created: int
    skipped: int
    errors: int
    results: list[SyncSessionResult]
