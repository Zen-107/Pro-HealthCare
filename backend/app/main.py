"""FastAPI application entrypoint — Pro-HealthCare backend"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.routes import api_router
from app.core.config import settings
from app.core.database import SessionLocal


@asynccontextmanager
async def lifespan(_: FastAPI):
    # import models เพื่อให้ Base.metadata รู้จักทุกตาราง
    import app.models  # noqa: F401
    yield


app = FastAPI(
    title="Pro-HealthCare API",
    description="AI-Driven Home Rehabilitation & Physical Therapy Tracker — Backend",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — อนุญาต frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["System"])
def health_check():
    """ตรวจสอบสถานะระบบ รวมการเชื่อมต่อฐานข้อมูล"""
    db_status = "unknown"
    db_error: str | None = None
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:  # noqa: BLE001
        db_status = "error"
        db_error = str(e)

    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "service": "prohealthcare-backend",
        "version": "0.1.0",
        "database": {"status": db_status, "error": db_error},
    }


@app.get("/", tags=["System"])
def root():
    return {
        "name": "Pro-HealthCare API",
        "docs": "/docs",
        "health": "/health",
    }
