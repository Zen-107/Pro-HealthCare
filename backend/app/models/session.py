"""ตาราง sessions และ session_reps — การฝึกแต่ละครั้ง"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class Session(TimestampMixin, Base):
    """หนึ่งเซสชันฝึกของผู้ป่วย"""

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"), index=True, nullable=False
    )
    plan_id: Mapped[int | None] = mapped_column(
        ForeignKey("exercise_plans.id", ondelete="SET NULL"), index=True, nullable=True
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="in_progress", nullable=False)
    total_reps: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    accuracy_score_avg: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    device_info: Mapped[str | None] = mapped_column(String(255), nullable=True)  # offline sync metadata

    def __repr__(self) -> str:
        return f"<Session id={self.id} patient_id={self.patient_id} status={self.status}>"


class SessionRep(TimestampMixin, Base):
    """ผลการทำท่าทีละ rep"""

    __tablename__ = "session_reps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    rep_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    accuracy_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)  # 0-100
    max_rom: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # degrees
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quality: Mapped[str] = mapped_column(String(20), default="acceptable", nullable=False)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)  # ข้อความจาก AI Coach

    def __repr__(self) -> str:
        return f"<SessionRep id={self.id} session_id={self.session_id} rep={self.rep_number}>"
