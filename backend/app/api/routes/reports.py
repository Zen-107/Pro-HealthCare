"""Reports routes — placeholder ก่อน Agent 3 (Clinical Reporter) พร้อมใช้ใน Step 3"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.core.enums import UserRole
from app.models.clinical_report import ClinicalReport
from app.models.patient import Patient
from app.schemas.report import ClinicalReportOut

router = APIRouter()


@router.get("/patient/{patient_id}", response_model=list[ClinicalReportOut])
def patient_reports(patient_id: int, user: CurrentUser, db: DbSession):
    """ดูรายงานสรุปของผู้ป่วยคนหนึ่ง

    ผู้ป่วยดูของตัวเองได้ / แพทย์ดูของผู้ป่วยที่ตัวเองดูแลได้
    รายงานยังเป็น placeholder — Agent 3 จะ generate จริงใน Step 3
    """
    # ตรวจสิทธิ์
    patient = db.get(Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบผู้ป่วย")
    if UserRole(user.role) == UserRole.PATIENT:
        if patient.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ไม่มีสิทธิ์เข้าถึง")
    elif UserRole(user.role) == UserRole.DOCTOR:
        if patient.assigned_doctor_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ไม่ใช่ผู้ป่วยของคุณ")

    stmt = (
        select(ClinicalReport)
        .where(ClinicalReport.patient_id == patient_id)
        .order_by(ClinicalReport.created_at.desc())
    )
    return list(db.scalars(stmt))
