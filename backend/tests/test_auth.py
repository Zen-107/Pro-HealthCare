"""Auth flow tests — register / login / me"""
from fastapi.testclient import TestClient

from tests.conftest import auth_header


def test_register_patient_returns_token(client: TestClient):
    """ผู้ป่วยสมัครใหม่ต้องได้ token + role = patient"""
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newpatient@test.com",
            "password": "secret123",
            "full_name": "New Patient",
            "role": "patient",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"
    assert data["role"] == "patient"
    assert isinstance(data["user_id"], int)


def test_register_doctor_returns_token(client: TestClient):
    """แพทย์สมัครใหม่ต้องได้ role = doctor"""
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newdoctor@test.com",
            "password": "secret123",
            "full_name": "New Doctor",
            "role": "doctor",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["role"] == "doctor"


def test_register_duplicate_email_returns_409(client: TestClient):
    """สมัครซ้ำ email เดิมต้องได้ 409"""
    payload = {
        "email": "dup@test.com",
        "password": "secret123",
        "full_name": "Dup User",
        "role": "patient",
    }
    resp1 = client.post("/api/v1/auth/register", json=payload)
    assert resp1.status_code == 201

    resp2 = client.post("/api/v1/auth/register", json=payload)
    assert resp2.status_code == 409


def test_login_with_valid_credentials(client: TestClient):
    """Login ด้วย email/password ที่ถูกต้องต้องได้ token"""
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@test.com",
            "password": "secret123",
            "full_name": "Login User",
            "role": "patient",
        },
    )
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "login@test.com", "password": "secret123"},
    )
    assert resp.status_code == 200
    assert resp.json()["access_token"]


def test_login_with_wrong_password_returns_401(client: TestClient):
    """Login ผิด password ต้องได้ 401"""
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrong@test.com",
            "password": "secret123",
            "full_name": "Wrong User",
            "role": "patient",
        },
    )
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@test.com", "password": "WRONG"},
    )
    assert resp.status_code == 401


def test_get_me_with_token(client: TestClient, patient_token: dict):
    """GET /auth/me ด้วย token ต้องได้ข้อมูล user"""
    resp = client.get("/api/v1/auth/me", headers=auth_header(patient_token["access_token"]))
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "patient@test.com"
    assert data["role"] == "patient"


def test_get_me_without_token_returns_401(client: TestClient):
    """GET /auth/me ไม่ใส่ token ต้องได้ 401"""
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401
