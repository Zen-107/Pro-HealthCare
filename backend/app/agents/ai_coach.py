"""🗣️ Agent 2: AI Coach (The Brain) — STUB

หน้าที่ (เมื่อ implement ใน Step 3):
- LLM ที่รับค่ามุมข้อต่อ (JSON) เปรียบเทียบกับทฤษฎีกายภาพบำบัด (ดึงจาก RAG)
- Generate ข้อความ/เสียง (TTS) แบบ Real-time เช่น "งอเข่าอีกนิดครับ ขาดอีก 1 คืบ"
- XAI Feature: อธิบายเหตุผล เช่น "มุมเข่า 120° (เป้าหมาย: 90°)"

หลักการ Safety: ใช้แนะนำ/เตือนเท่านั้น — ห้ามเปลี่ยนแผนการรักษาเอง
"""
from dataclasses import dataclass


@dataclass
class CoachingFeedback:
    """ผลลัพธ์ feedback จาก AI Coach"""
    message: str
    accuracy_score: float  # 0-100
    is_correct: bool
    explanation: str | None = None  # ส่วน XAI


class AICoach:
    """STUB — จะเชื่อม LLM (LangChain) ใน Step 3"""

    def __init__(self, llm_provider: str = "stub") -> None:
        self.llm_provider = llm_provider

    def evaluate(
        self,
        joint_angles: dict[str, float],
        ideal_angles: dict[str, dict],
    ) -> CoachingFeedback:
        """รับมุมปัจจุบัน + baseline -> คืน feedback + คะแนน + คำอธิบาย

        Step 3: ส่ง prompt ให้ LLM พร้อม context จาก RAG (ความรู้กายภาพบำบัด)
        """
        raise NotImplementedError("AICoach.evaluate ยังไม่ implement — อยู่ใน Step 3")

    def to_speech(self, feedback: CoachingFeedback) -> bytes:
        """แปลง feedback เป็นเสียง (TTS)"""
        raise NotImplementedError("TTS ยังไม่ implement — อยู่ใน Step 3+")
