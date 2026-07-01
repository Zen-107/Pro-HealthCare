"""Exercise routes — คลังท่ากายภาพ (รวม ideal_angles = Ground Truth)"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.core.enums import UserRole
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseOut

router = APIRouter()


@router.get("", response_model=list[ExerciseOut])
def list_exercises(
    user: CurrentUser,
    db: DbSession,
    category: str | None = None,
):
    """ดูคลังท่าทั้งหมด (กรองตาม category ได้)"""
    stmt = select(Exercise).order_by(Exercise.category, Exercise.name)
    if category:
        stmt = stmt.where(Exercise.category == category)
    return list(db.scalars(stmt))


@router.get("/{exercise_id}", response_model=ExerciseOut)
def get_exercise(exercise_id: int, user: CurrentUser, db: DbSession):
    exercise = db.get(Exercise, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบท่ากายภาพนี้")
    return exercise


@router.post("", response_model=ExerciseOut, status_code=status.HTTP_201_CREATED)
def create_exercise(payload: ExerciseCreate, user: CurrentUser, db: DbSession):
    """เพิ่มท่ากายภาพใหม่ (แพทย์/แอดมิน)"""
    if UserRole(user.role) == UserRole.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="สำหรับแพทย์/แอดมินเท่านั้น")
    exercise = Exercise(**payload.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise
