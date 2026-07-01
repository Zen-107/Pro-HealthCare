"""Clinical report schemas"""
from datetime import date

from pydantic import BaseModel, ConfigDict


class ClinicalReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    session_id: int | None = None
    period_start: date | None = None
    period_end: date | None = None
    summary_json: dict | None = None
    llm_note: str | None = None
    pdf_path: str | None = None
    created_by_agent: str | None = None
