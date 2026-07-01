# 🏥 Pro-HealthCare — AI-Driven Home Rehabilitation & Physical Therapy Tracker

ระบบกายภาพบำบัดที่บ้านผ่านเว็บแคม/มือถือ ใช้ Computer Vision (MediaPipe) ตรวจจับท่าทาง + Multi-Agent LLM ให้ Feedback แบบ Real-time พร้อมส่งรายงานให้แพทย์

> 📄 รายละเอียดไอเดีย/แนวคิด: ดูใน `ระบบกายภาพบำบัดผ่านเว็บแคม.md`

โปรเจกต์นี้ครอบคลุมวิชา **CPE310** — Phase 1 (Core ML/DL) และ Phase 2 (Agentic AI)

---

## 🧱 โครงสร้างโปรเจกต์ (Monorepo)

```
Pro-HealthCare/
├── docker-compose.yml      # MySQL 8 + Adminer
├── backend/                # FastAPI + SQLAlchemy + Alembic (uv + Python 3.11)
└── frontend/               # React + Vite + Tailwind (+ Capacitor สำหรับ Android)
```

## 🚀 เริ่มต้นอย่างรวดเร็ว

### 1. เตรียม environment
```bash
cp .env.example .env          # แล้วแก้ค่า SECRET_KEY ให้เป็นคีย์สุ่ม
```

### 2. รันฐานข้อมูล (Docker)
```bash
docker compose up -d
# MySQL → localhost:3306   |   Adminer (GUI) → http://localhost:8080
```

### 3. รัน Backend
```bash
cd backend
uv venv --python 3.11
# บน Windows:  .venv\Scripts\activate
uv pip install -e .
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
# Swagger docs → http://localhost:8000/docs
```

### 4. รัน Frontend
```bash
cd frontend
npm install
npm run dev                   # → http://localhost:5173
```

## 🗺️ Roadmap

| Step | ขอบเขต | สถานะ |
|------|--------|------|
| **1** | Backend + Database + Frontend scaffold | 🚧 กำลังทำ |
| 2 | Computer Vision (MediaPipe) + Angle/ROM logic | ⏳ ถัดไป |
| 3 | Agentic AI (Vision Tracker / AI Coach / Reporter) + Predictive | ⏳ |
| 4 | Play Store Preparation & Launch (Capacitor APK) | ⏳ |

## ⚠️ หลักการสำคัญ (PDPA & Safety)

- **ห้าม** ส่งภาพวิดีโอจากกล้องขึ้น Server — ประมวลผล On-device แล้วส่งขึ้นเฉพาะค่า JSON (Landmarks/Angles)
- **AI Coach** ใช้แนะนำ/เตือนเท่านั้น การปรับแผนการรักษาต้องให้แพทย์ Approve (Human-in-the-loop)
- คำสั่งสุขภาพหลีกเลี่ยงคำว่า "รักษาหายขาด" ใช้ "ช่วยฟื้นฟู" ตาม Google Play Policy
