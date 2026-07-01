"""Pytest fixtures — ใช้ SQLite in-memory เพื่อให้ test รันได้โดยไม่ต้องพึ่ง Docker MySQL

Pattern มาตรฐานสำหรับ FastAPI integration test:
1. สร้าง engine + session ของ SQLite ขึ้นมาใหม่
2. override dependency `get_db` ของ FastAPI ให้ชี้ไปที่ test session
3. สร้างตารางทุกตารางจาก Base.metadata ก่อนเริ่ม test
"""
from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.core.database import Base
from app.main import app as fastapi_app

# import models เพื่อ register ทุกตารางเข้า Base.metadata
import app.models  # noqa: F401


# -------------------------------------------------------------------
# Database fixtures
# -------------------------------------------------------------------

@pytest.fixture(scope="function")
def engine():
    """SQLite in-memory engine — สร้างใหม่ทุก test เพื่อ isolation สมบูรณ์"""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # ใช้ connection เดียวกัน (in-memory)
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Session, None, None]:
    """Session สำหรับแต่ละ test"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """TestClient ที่ใช้ test DB ผ่าน dependency override"""

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass  # ปิด session ที่ fixture หลัก

    fastapi_app.dependency_overrides[get_db] = _override_get_db
    with TestClient(fastapi_app) as c:
        yield c
    fastapi_app.dependency_overrides.clear()


# -------------------------------------------------------------------
# Auth helper fixtures
# -------------------------------------------------------------------

def _register(client: TestClient, email: str, password: str = "pass1234",
              full_name: str = "Test User", role: str = "patient") -> dict:
    """สมัครผู้ใช้ แล้วคืน token payload"""
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": full_name, "role": role},
    )
    assert resp.status_code == 201, f"register failed: {resp.text}"
    return resp.json()


@pytest.fixture
def patient_token(client: TestClient) -> dict:
    """ผู้ป่วย 1 คน + token"""
    return _register(client, "patient@test.com", full_name="Patient One", role="patient")


@pytest.fixture
def doctor_token(client: TestClient) -> dict:
    """แพทย์ 1 คน + token"""
    return _register(client, "doctor@test.com", full_name="Doctor One", role="doctor")


@pytest.fixture
def second_patient_token(client: TestClient) -> dict:
    """ผู้ป่วยอีกคน (สำหรับทดสอบการเข้าถึงข้ามผู้ใช้)"""
    return _register(client, "patient2@test.com", full_name="Patient Two", role="patient")


def auth_header(token: str) -> dict:
    """สร้าง Authorization header"""
    return {"Authorization": f"Bearer {token}"}


# -------------------------------------------------------------------
# Domain helper fixtures — สร้าง state ที่ซับซ้อนให้ใช้ใน test
# -------------------------------------------------------------------

@pytest.fixture
def assigned_patient(client: TestClient, patient_token: dict, doctor_token: dict,
                      db_session: Session) -> dict:
    """ผู้ป่วยที่ assigned ให้แพทย์แล้ว — คืน dict พร้อม token, patient_id, doctor_token"""
    from app.models.patient import Patient
    from sqlalchemy import select

    # หา patient profile ของผู้ป่วยที่สมัคร
    patient = db_session.scalar(
        select(Patient).where(Patient.user_id == patient_token["user_id"])
    )
    # assign ให้แพทย์
    patient.assigned_doctor_id = doctor_token["user_id"]
    db_session.commit()

    return {
        "patient_token": patient_token,
        "patient_id": patient.id,
        "doctor_token": doctor_token,
    }


@pytest.fixture
def exercise_id(client: TestClient, doctor_token: dict) -> int:
    """สร้าง exercise ตัวอย่าง 1 ท่า แล้วคืน id"""
    resp = client.post(
        "/api/v1/exercises",
        json={
            "name": "Plan Test Exercise",
            "name_th": "ท่าทดสอบแผน",
            "category": "knee",
            "difficulty": "easy",
            "target_joints": ["left_knee"],
            "ideal_angles": {"left_knee": {"min": 0, "max": 15, "target": 5}},
        },
        headers=auth_header(doctor_token["access_token"]),
    )
    assert resp.status_code == 201, f"create exercise failed: {resp.text}"
    return resp.json()["id"]
