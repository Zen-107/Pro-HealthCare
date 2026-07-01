"""ตาราง clinical_reports — รายงานสรุปที่ Agent 3 (Clinical Reporter) generate"""
from datetime import date

from sqlalchemy import JSON, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class ClinicalReport(TimestampMixin, Base):
    """รายงานสรุประยะเวลาหนึ่ง หรือเซสชันหนึ่ง — ส่งให้แพทย์"""

    __tablename__ = "clinical_reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"), index=True, nullable=False
    )
    session_id: Mapped[int | None] = mapped_column(
        ForeignKey("sessions.id", ondelete="SET NULL"), index=True, nullable=True
    )
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    summary_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # ตัวเลข/กราฟ
    llm_note: Mapped[str | None] = mapped_column(Text, nullable=True)  # คำอธิบายจาก LLM
    pdf_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_by_agent: Mapped[str | None] = mapped_column(String(50), nullable=True)

    def __repr__(self) -> str:
        return f"<ClinicalReport id={self.id} patient_id={self.patient_id}>"
