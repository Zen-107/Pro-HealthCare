"""Session routes — เซสชันฝึก, reps, และ joint angles (JSON จาก On-device)"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession, get_current_patient_profile
from app.models.joint_angle import JointAngleRecord
from app.models.session import TherapySession, SessionRep
from app.schemas.session import (
    JointAngleBatch,
    SessionCreate,
    SessionOut,
    SessionRepCreate,
    SessionRepOut,
    SessionUpdate,
)

router = APIRouter()


@router.post("", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def start_session(payload: SessionCreate, user: CurrentUser, db: DbSession):
    """ผู้ป่วย: เริ่มเซสชันฝึกใหม่"""
    patient = get_current_patient_profile(user, db)
    session = TherapySession(
        patient_id=patient.id,
        plan_id=payload.plan_id,
        started_at=datetime.now(timezone.utc),
        status="in_progress",
        device_info=payload.device_info,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/mine", response_model=list[SessionOut])
def my_sessions(user: CurrentUser, db: DbSession):
    """ผู้ป่วย: ดูประวัติเซสชันของตัวเอง"""
    patient = get_current_patient_profile(user, db)
    stmt = select(TherapySession).where(TherapySession.patient_id == patient.id).order_by(TherapySession.started_at.desc())
    return list(db.scalars(stmt))


@router.patch("/{session_id}", response_model=SessionOut)
def update_session(session_id: int, payload: SessionUpdate, user: CurrentUser, db: DbSession):
    """อัปเดตเซสชัน (เช่นปิดเซสชัน, ใส่คะแนนเฉลี่ย)"""
    session = db.get(TherapySession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบเซสชัน")
    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "status" and value == "completed":
            session.ended_at = datetime.now(timezone.utc)
        setattr(session, field, value)
    db.commit()
    db.refresh(session)
    return session


@router.post("/{session_id}/reps", response_model=SessionRepOut, status_code=status.HTTP_201_CREATED)
def add_rep(session_id: int, payload: SessionRepCreate, user: CurrentUser, db: DbSession):
    """บันทึกผล rep หนึ่ง (คะแนน/ROM/feedback จาก AI Coach)"""
    session = db.get(TherapySession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบเซสชัน")
    rep = SessionRep(session_id=session_id, **payload.model_dump())
    db.add(rep)
    session.total_reps = (session.total_reps or 0) + 1
    db.commit()
    db.refresh(rep)
    return rep


@router.post("/{session_id}/angles", status_code=status.HTTP_201_CREATED)
def add_angles(session_id: int, payload: JointAngleBatch, user: CurrentUser, db: DbSession):
    """บันทึกมุมข้อต่อเป็นชุด (Time-Series) — ค่า JSON จาก On-device processing

    หมายเหตุ PDPA: เก็บเฉพาะค่าตัวเลข ไม่เก็บภาพ/วิดีโอ
    """
    session = db.get(TherapySession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบเซสชัน")
    records = [
        JointAngleRecord(session_id=session_id, **a.model_dump()) for a in payload.angles
    ]
    db.add_all(records)
    db.commit()
    return {"saved": len(records)}


@router.get("/{session_id}/angles")
def get_angles(session_id: int, user: CurrentUser, db: DbSession):
    """ดึง time-series มุมข้อต่อของเซสชันหนึ่ง — สำหรับพล็อตกราฟ"""
    session = db.get(TherapySession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบเซสชัน")
    stmt = (
        select(JointAngleRecord)
        .where(JointAngleRecord.session_id == session_id)
        .order_by(JointAngleRecord.timestamp_ms)
    )
    rows = db.scalars(stmt).all()
    return [
        {
            "timestamp_ms": r.timestamp_ms,
            "joint_name": r.joint_name,
            "angle_value": float(r.angle_value),
        }
        for r in rows
    ]
