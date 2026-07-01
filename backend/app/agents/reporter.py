"""📄 Agent 3: Clinical Reporter (The Scribe) — STUB

หน้าที่ (เมื่อ implement ใน Step 3):
- เมื่อจบเซสชัน ดึง Log ความถูกต้อง, จำนวน reps, ROM
- Generate Clinical Summary Report (PDF/JSON) ส่งให้แพทย์ผ่าน Web Dashboard
"""
from dataclasses import dataclass


@dataclass
class SessionSummary:
    """สรุปเซสชันหนึ่งก่อนส่งให้แพทย์"""
    session_id: int
    total_reps: int
    accuracy_avg: float
    rom_improvement: float | None
    duration_minutes: float
    notes: str | None = None


class ClinicalReporter:
    """STUB — จะเชื่อม LLM + reportlab ใน Step 3"""

    def __init__(self, llm_provider: str = "stub") -> None:
        self.llm_provider = llm_provider

    def summarize_session(self, session_id: int) -> SessionSummary:
        """ดึงข้อมูลเซสชัน -> สรุปเป็น SessionSummary"""
        raise NotImplementedError("ClinicalReporter.summarize_session ยังไม่ implement — Step 3")

    def generate_pdf(self, summary: SessionSummary) -> str:
        """สร้างไฟล์ PDF รายงาน -> คืน path"""
        raise NotImplementedError("PDF generation ยังไม่ implement — Step 3")

    def generate_clinical_note(self, summary: SessionSummary) -> str:
        """LLM เขียน clinical note (ภาษาธรรมชาติ)"""
        raise NotImplementedError("Clinical note ยังไม่ implement — Step 3")
