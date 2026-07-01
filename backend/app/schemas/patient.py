"""Patient schemas"""
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.core.enums import Gender
from app.schemas.user import UserOut


class PatientUpdate(BaseModel):
    dob: date | None = None
    gender: Gender | None = None
    height_cm: Decimal | None = None
    weight_kg: Decimal | None = None
    medical_notes: str | None = None


class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    dob: date | None = None
    gender: Gender | None = None
    height_cm: Decimal | None = None
    weight_kg: Decimal | None = None
    assigned_doctor_id: int | None = None
    medical_notes: str | None = None


class PatientWithUser(BaseModel):
    """ผู้ป่วย + ข้อมูลบัญชี — สำหรับหน้าแพทย์"""
    model_config = ConfigDict(from_attributes=True)
    patient: PatientOut
    user: UserOut
