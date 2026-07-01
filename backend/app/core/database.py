"""การเชื่อมต่อฐานข้อมูล SQLAlchemy — engine + session factory"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # ตรวจสอบ connection ก่อนใช้ (ป้องกัน stale connection)
    pool_recycle=3600,   # รีไซเคิลทุกชั่วโมง (MySQL wait_timeout)
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class สำหรับทุก ORM model"""


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — เปิด/ปิด session อัตโนมัติ"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
