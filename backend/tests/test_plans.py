"""Plan flow tests — แพทย์สร้างแผน / ผู้ป่วยดูแผนตัวเอง"""
from fastapi.testclient import TestClient

from tests.conftest import auth_header


def _make_plan_payload(patient_id: int, exercise_id: int) -> dict:
    return {
        "patient_id": patient_id,
        "name": "แผนฟื้นฟูเข่า",
        "status": "active",
        "start_date": "2026-01-01",
        "end_date": "2026-03-01",
        "items": [
            {
                "exercise_id": exercise_id,
                "sets": 3,
                "reps_per_set": 10,
                "hold_seconds": 5,
                "frequency_per_week": 4,
                "order_index": 0,
            }
        ],
    }


def test_doctor_creates_plan_for_patient(client: TestClient, assigned_patient: dict,
                                          exercise_id: int):
    """แพทย์สร้างแผนให้ผู้ป่วยได้ พร้อม items"""
    payload = _make_plan_payload(assigned_patient["patient_id"], exercise_id)
    resp = client.post(
        "/api/v1/plans",
        json=payload,
        headers=auth_header(assigned_patient["doctor_token"]["access_token"]),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"]
    assert data["name"] == "แผนฟื้นฟูเข่า"
    assert data["status"] == "active"
    assert data["patient_id"] == assigned_patient["patient_id"]
    assert data["doctor_id"] == assigned_patient["doctor_token"]["user_id"]
    assert len(data["items"]) == 1
    assert data["items"][0]["exercise_id"] == exercise_id
    assert data["items"][0]["sets"] == 3
    assert data["items"][0]["reps_per_set"] == 10


def test_patient_cannot_create_plan(client: TestClient, patient_token: dict,
                                      assigned_patient: dict, exercise_id: int):
    """ผู้ป่วยสร้างแผนไม่ได้ ต้องได้ 403"""
    payload = _make_plan_payload(assigned_patient["patient_id"], exercise_id)
    resp = client.post(
        "/api/v1/plans",
        json=payload,
        headers=auth_header(patient_token["access_token"]),
    )
    assert resp.status_code == 403


def test_patient_views_own_plans(client: TestClient, assigned_patient: dict, exercise_id: int):
    """ผู้ป่วยดูแผนของตัวเองได้ผ่าน /plans/mine"""
    # แพทย์สร้างแผนก่อน
    payload = _make_plan_payload(assigned_patient["patient_id"], exercise_id)
    client.post(
        "/api/v1/plans",
        json=payload,
        headers=auth_header(assigned_patient["doctor_token"]["access_token"]),
    )

    # ผู้ป่วยดูแผนของตัวเอง
    resp = client.get(
        "/api/v1/plans/mine",
        headers=auth_header(assigned_patient["patient_token"]["access_token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert data[0]["name"] == "แผนฟื้นฟูเข่า"
    assert data[0]["status"] == "active"


def test_doctor_views_patient_plans(client: TestClient, assigned_patient: dict, exercise_id: int):
    """แพทย์ดูแผนของผู้ป่วยที่ตนดูแลได้"""
    payload = _make_plan_payload(assigned_patient["patient_id"], exercise_id)
    client.post(
        "/api/v1/plans",
        json=payload,
        headers=auth_header(assigned_patient["doctor_token"]["access_token"]),
    )

    resp = client.get(
        f"/api/v1/plans/patient/{assigned_patient['patient_id']}",
        headers=auth_header(assigned_patient["doctor_token"]["access_token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert any(p["name"] == "แผนฟื้นฟูเข่า" for p in data)


def test_patient_cannot_view_other_patient_via_doctor_endpoint(
    client: TestClient, assigned_patient: dict, second_patient_token: dict
):
    """ผู้ป่วยเข้า endpoint ของแพทย์ (/plans/patient/{id}) ไม่ได้ ต้องได้ 403"""
    resp = client.get(
        f"/api/v1/plans/patient/{assigned_patient['patient_id']}",
        headers=auth_header(second_patient_token["access_token"]),
    )
    assert resp.status_code == 403


def test_update_plan_status(client: TestClient, assigned_patient: dict, exercise_id: int):
    """แพทย์เปลี่ยนสถานะแผนได้"""
    payload = _make_plan_payload(assigned_patient["patient_id"], exercise_id)
    create_resp = client.post(
        "/api/v1/plans",
        json=payload,
        headers=auth_header(assigned_patient["doctor_token"]["access_token"]),
    )
    plan_id = create_resp.json()["id"]

    resp = client.put(
        f"/api/v1/plans/{plan_id}?status_value=paused",
        headers=auth_header(assigned_patient["doctor_token"]["access_token"]),
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "paused"
