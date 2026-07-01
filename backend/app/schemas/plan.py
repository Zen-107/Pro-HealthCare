"""Plan schemas"""
from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import PlanStatus


class PlanItemCreate(BaseModel):
    exercise_id: int
    sets: int = Field(default=1, ge=1, le=20)
    reps_per_set: int = Field(default=10, ge=1, le=100)
    hold_seconds: int | None = Field(default=None, ge=1, le=120)
    frequency_per_week: int = Field(default=3, ge=1, le=7)
    order_index: int = 0


class PlanItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    plan_id: int
    exercise_id: int
    sets: int
    reps_per_set: int
    hold_seconds: int | None = None
    frequency_per_week: int
    order_index: int


class ExercisePlanCreate(BaseModel):
    """แพทย์สร้าง/ปรับแผน (Human-in-the-loop)"""
    patient_id: int
    name: str = Field(max_length=200)
    status: PlanStatus = PlanStatus.DRAFT
    start_date: date | None = None
    end_date: date | None = None
    items: list[PlanItemCreate] = Field(default_factory=list)


class ExercisePlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    doctor_id: int | None = None
    name: str
    status: PlanStatus
    start_date: date | None = None
    end_date: date | None = None


class ExercisePlanDetail(ExercisePlanOut):
    """แผนพร้อมรายการท่า"""
    items: list[PlanItemOut] = []
