"""User routes — profile ตัวเอง + รายชื่อผู้ป่วย (แพทย์)"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession, get_current_patient_profile
from app.core.enums import UserRole
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientUpdate, PatientWithUser
from app.schemas.user import UserOut, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserOut)
def get_me(user: CurrentUser):
    return user


@router.put("/me", response_model=UserOut)
def update_me(payload: UserUpdate, user: CurrentUser, db: DbSession):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.put("/me/patient", response_model=UserOut)
def update_my_patient_profile(
    payload: PatientUpdate,
    user: CurrentUser,
    db: DbSession,
):
    """ผู้ป่วยแก้ข้อมูลสุขภาพตัวเอง"""
    if UserRole(user.role) != UserRole.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="สำหรับผู้ป่วยเท่านั้น")
    patient = get_current_patient_profile(user, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.get("/patients", response_model=list[PatientWithUser])
def list_my_patients(user: CurrentUser, db: DbSession):
    """แพทย์: ดูรายชื่อผู้ป่วยที่ตนดูแล"""
    if UserRole(user.role) != UserRole.DOCTOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="สำหรับแพทย์เท่านั้น")
    rows = db.scalars(
        select(Patient).where(Patient.assigned_doctor_id == user.id)
    ).all()
    out = []
    for p in rows:
        u = db.get(User, p.user_id)
        out.append(PatientWithUser(patient=p, user=u))
    return out
