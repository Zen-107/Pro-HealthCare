"""ตาราง exercise_plans และ plan_items — แผนกายภาพที่แพทย์สั่ง"""
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class ExercisePlan(TimestampMixin, Base):
    """แผนกายภาพของผู้ป่วยหนึ่งคน — ประกอบด้วยหลาย plan_item"""

    __tablename__ = "exercise_plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"), index=True, nullable=False
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    items: Mapped[list["PlanItem"]] = relationship(
        back_populates="plan", cascade="all, delete-orphan", order_by="PlanItem.order_index"
    )

    def __repr__(self) -> str:
        return f"<ExercisePlan id={self.id} patient_id={self.patient_id} status={self.status}>"


class PlanItem(TimestampMixin, Base):
    """ท่าหนึ่งท่าในแผน — กำหนด sets/reps/hold/frequency"""

    __tablename__ = "plan_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("exercise_plans.id", ondelete="CASCADE"), index=True, nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    sets: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    reps_per_set: Mapped[int] = mapped_column(SmallInteger, default=10, nullable=False)
    hold_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    frequency_per_week: Mapped[int] = mapped_column(SmallInteger, default=3, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    plan: Mapped["ExercisePlan"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"<PlanItem id={self.id} plan_id={self.plan_id} exercise_id={self.exercise_id}>"
