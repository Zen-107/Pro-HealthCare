"""Exercise flow tests — คลังท่ากายภาพ (CRUD + permission)"""
from fastapi.testclient import TestClient

from tests.conftest import auth_header

EXERCISE_PAYLOAD = {
    "name": "Test Knee Extension",
    "name_th": "เเข้งขาตรงทดสอบ",
    "category": "knee",
    "difficulty": "easy",
    "target_joints": ["left_knee", "right_knee"],
    "ideal_angles": {
        "left_knee": {"min": 0, "max": 15, "target": 5},
        "right_knee": {"min": 0, "max": 15, "target": 5},
    },
    "instructions": "ยกขาขึ้นจนตรง ค้าง 3 วินาที",
}


def test_doctor_can_create_exercise(client: TestClient, doctor_token: dict):
    """แพทย์สร้าง exercise ได้ และได้ข้อมูลกลับมาครบ"""
    resp = client.post(
        "/api/v1/exercises",
        json=EXERCISE_PAYLOAD,
        headers=auth_header(doctor_token["access_token"]),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"]
    assert data["name"] == "Test Knee Extension"
    assert data["name_th"] == "เเข้งขาตรงทดสอบ"
    assert data["category"] == "knee"
    assert data["target_joints"] == ["left_knee", "right_knee"]
    assert data["ideal_angles"]["left_knee"]["target"] == 5


def test_patient_cannot_create_exercise(client: TestClient, patient_token: dict):
    """ผู้ป่วยสร้าง exercise ไม่ได้ ต้องได้ 403"""
    resp = client.post(
        "/api/v1/exercises",
        json=EXERCISE_PAYLOAD,
        headers=auth_header(patient_token["access_token"]),
    )
    assert resp.status_code == 403


def test_list_exercises(client: TestClient, doctor_token: dict):
    """สร้างแล้ว list ต้องเห็นที่สร้าง"""
    client.post(
        "/api/v1/exercises",
        json=EXERCISE_PAYLOAD,
        headers=auth_header(doctor_token["access_token"]),
    )
    resp = client.get(
        "/api/v1/exercises",
        headers=auth_header(doctor_token["access_token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(e["name"] == "Test Knee Extension" for e in data)


def test_list_exercises_filter_by_category(client: TestClient, doctor_token: dict):
    """กรอง exercise ตาม category ได้"""
    client.post(
        "/api/v1/exercises",
        json=EXERCISE_PAYLOAD,
        headers=auth_header(doctor_token["access_token"]),
    )
    resp = client.get(
        "/api/v1/exercises?category=knee",
        headers=auth_header(doctor_token["access_token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert all(e["category"] == "knee" for e in data)


def test_get_exercise_by_id(client: TestClient, doctor_token: dict):
    """ดู exercise ตาม id"""
    create_resp = client.post(
        "/api/v1/exercises",
        json=EXERCISE_PAYLOAD,
        headers=auth_header(doctor_token["access_token"]),
    )
    exercise_id = create_resp.json()["id"]

    resp = client.get(
        f"/api/v1/exercises/{exercise_id}",
        headers=auth_header(doctor_token["access_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["id"] == exercise_id


def test_get_nonexistent_exercise_returns_404(client: TestClient, doctor_token: dict):
    """ดู exercise ที่ไม่มี ต้องได้ 404"""
    resp = client.get(
        "/api/v1/exercises/99999",
        headers=auth_header(doctor_token["access_token"]),
    )
    assert resp.status_code == 404


def test_list_exercises_requires_auth(client: TestClient):
    """ไม่ใส่ token ต้องได้ 401"""
    resp = client.get("/api/v1/exercises")
    assert resp.status_code == 401
