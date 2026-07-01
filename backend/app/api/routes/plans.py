"""Plan routes — แผนกายภาพ (แพทย์เป็นผู้สร้าง/ปรับ — Human-in-the-loop)"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, DbSession, get_current_patient_profile
from app.core.enums import UserRole
from app.models.exercise_plan import ExercisePlan, PlanItem
from app.schemas.plan import (
    ExercisePlanCreate,
    ExercisePlanDetail,
    ExercisePlanOut,
    PlanItemOut,
)

router = APIRouter()


@router.get("/mine", response_model=list[ExercisePlanDetail])
def my_plans(user: CurrentUser, db: DbSession):
    """ผู้ป่วย: ดูแผนของตัวเองทั้งหมด"""
    patient = get_current_patient_profile(user, db)
    stmt = (
        select(ExercisePlan)
        .options(selectinload(ExercisePlan.items))
        .where(ExercisePlan.patient_id == patient.id)
        .order_by(ExercisePlan.created_at.desc())
    )
    return list(db.scalars(stmt))


@router.get("/patient/{patient_id}", response_model=list[ExercisePlanDetail])
def patient_plans(patient_id: int, user: CurrentUser, db: DbSession):
    """แพทย์: ดูแผนของผู้ป่วยคนหนึ่ง"""
    if UserRole(user.role) != UserRole.DOCTOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="สำหรับแพทย์เท่านั้น")
    stmt = (
        select(ExercisePlan)
        .options(selectinload(ExercisePlan.items))
        .where(ExercisePlan.patient_id == patient_id)
        .order_by(ExercisePlan.created_at.desc())
    )
    return list(db.scalars(stmt))


@router.post("", response_model=ExercisePlanDetail, status_code=status.HTTP_201_CREATED)
def create_plan(payload: ExercisePlanCreate, user: CurrentUser, db: DbSession):
    """แพทย์: สร้างแผนใหม่พร้อมท่า (items)"""
    if UserRole(user.role) != UserRole.DOCTOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="สำหรับแพทย์เท่านั้น")

    plan = ExercisePlan(
        patient_id=payload.patient_id,
        doctor_id=user.id,
        name=payload.name,
        status=payload.status.value,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )
    db.add(plan)
    db.flush()

    for item in payload.items:
        db.add(
            PlanItem(
                plan_id=plan.id,
                exercise_id=item.exercise_id,
                sets=item.sets,
                reps_per_set=item.reps_per_set,
                hold_seconds=item.hold_seconds,
                frequency_per_week=item.frequency_per_week,
                order_index=item.order_index,
            )
        )
    db.commit()
    db.refresh(plan)
    # โหลด items relationship สำหรับ response
    db.refresh(plan, attribute_names=["items"])
    return plan


@router.put("/{plan_id}", response_model=ExercisePlanDetail)
def update_plan_status(plan_id: int, status_value: str, user: CurrentUser, db: DbSession):
    """แพทย์: เปลี่ยนสถานะแผน (active/paused/completed ฯลฯ)"""
    if UserRole(user.role) != UserRole.DOCTOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="สำหรับแพทย์เท่านั้น")
    plan = db.get(ExercisePlan, plan_id, options=[selectinload(ExercisePlan.items)])
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบแผนนี้")
    valid = {"draft", "active", "paused", "completed", "cancelled"}
    if status_value not in valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="สถานะไม่ถูกต้อง"
        )
    plan.status = status_value
    db.commit()
    return plan
