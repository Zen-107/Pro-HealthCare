"""ตาราง joint_angle_records — Time-Series มุมข้อต่อแต่ละจุด
เก็บเฉพาะค่าตัวเลขที่คำนวณแล้ว (ไม่เก็บภาพ/วิดีโอ — ตามหลัก PDPA)"""
from sqlalchemy import BigInteger, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class JointAngleRecord(TimestampMixin, Base):
    """จุดข้อมูลอนุกรมเวลา (Time-Series) ของมุมข้อต่อหนึ่งจุด ณ เวลาหนึ่ง"""

    __tablename__ = "joint_angle_records"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    rep_id: Mapped[int | None] = mapped_column(
        ForeignKey("session_reps.id", ondelete="CASCADE"), index=True, nullable=True
    )
    timestamp_ms: Mapped[int] = mapped_column(BigInteger, nullable=False)  # ms นับจาก start session
    joint_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # เช่น left_knee
    angle_value: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)  # degrees

    def __repr__(self) -> str:
        return f"<JointAngleRecord joint={self.joint_name!r} angle={self.angle_value}>"
