"""ตาราง exercises — คลังท่ากายภาพ (เก็บ Ground Truth มุมมาตรฐาน)"""
from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class Exercise(TimestampMixin, Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    name_th: Mapped[str | None] = mapped_column(String(200), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)  # เช่น knee, shoulder
    difficulty: Mapped[str] = mapped_column(String(20), default="easy", nullable=False)

    # ข้อต่อที่เกี่ยวข้อง เช่น ["left_knee", "right_knee", "left_hip"]
    target_joints: Mapped[list | None] = mapped_column(JSON, nullable=True)

    # Ground Truth — มุมมาตรฐานจากวิดีโออ้างอิง
    # เช่น {"left_knee": {"min": 90, "max": 120, "target": 90}}
    ideal_angles: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<Exercise id={self.id} name={self.name!r}>"
