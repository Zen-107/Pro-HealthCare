# Backend — Pro-HealthCare (FastAPI)

## โครงสร้าง

```
backend/
├── pyproject.toml          # 依赖 (uv เป็นคนจัดการ)
├── alembic.ini
├── .env.example
├── app/
│   ├── main.py             # FastAPI app + CORS + router
│   ├── core/               # config, database, security
│   ├── models/             # SQLAlchemy ORM (9 ตาราง)
│   ├── schemas/            # Pydantic request/response
│   ├── api/routes/         # auth, users, exercises, plans, sessions, sync, reports
│   ├── api/deps.py         # DI (get_db, get_current_user)
│   ├── agents/             # stub Phase 2 (vision_tracker, ai_coach, reporter)
│   └── alembic/            # DB migrations
└── tests/
```

## เริ่มต้น

```bash
uv venv --python 3.11
uv pip install -e ".[dev]"
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```

- Swagger UI: http://localhost:8000/docs
- ตั้งค่าใน `.env` (คัดลอกจาก `.env.example`)

## Multi-Agent Architecture (Phase 2 — placeholder)

| Agent | หน้าที่ | ไฟล์ stub |
|-------|------|----------|
| 📷 Vision Tracker | รัน MediaPipe ดึง landmarks/angles | `app/agents/vision_tracker.py` |
| 🗣️ AI Coach | LLM รับค่ามุม เปรียบเทียบ baseline แล้วให้ feedback | `app/agents/ai_coach.py` |
| 📄 Clinical Reporter | สรุปเซสชันเป็น Clinical Note | `app/agents/reporter.py` |

> stub class สร้างไว้แล้ว แต่ยังไม่มี logic จะ implement ใน Step 2-3
