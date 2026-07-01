"""Multi-Agent System — placeholder stub สำหรับ Phase 2 (จะ implement ใน Step 2-3)

สถาปัตยกรรม (ตาม concept ของโปรเจกต์):
    📷 VisionTracker  — รัน MediaPipe ดึง landmarks/คำนวณมุมข้อต่อ
    🗣️ AICoach        — LLM รับค่ามุม เปรียบเทียบ baseline ให้ feedback + XAI
    📄 ClinicalReporter — สรุปเซสชันเป็น Clinical Note ส่งแพทย์

คลาสในไฟล์นี้เป็น skeleton ที่ยังไม่มี logic จริง — เพื่อให้ระบบรันได้ตั้งแต่ Step 1
ก่อนเสียบ Computer Vision และ LLM
"""
from app.agents.ai_coach import AICoach
from app.agents.reporter import ClinicalReporter
from app.agents.vision_tracker import VisionTracker

__all__ = ["VisionTracker", "AICoach", "ClinicalReporter"]
