"""Session flow tests — เซสชันฝึก / reps / joint angles (Time-Series)"""
from fastapi.testclient import TestClient

from tests.conftest import auth_header


def test_patient_starts_session(client: TestClient, patient_token: dict):
    """ผู้ป่วยเริ่มเซสชันได้ ได้ status=in_progress"""
    resp = client.post(
        "/api/v1/sessions",
        json={"plan_id": None, "device_info": "test-device"},
        headers=auth_header(patient_token["access_token"]),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"]
    assert data["status"] == "in_progress"
    assert data["total_reps"] == 0
    assert data["device_info"] == "test-device"
    assert data["started_at"] is not None
    assert data["ended_at"] is None


def test_doctor_cannot_start_session(client: TestClient, doctor_token: dict):
    """แพทย์เริ่มเซสชันเองไม่ได้ (ไม่มี patient profile) ต้องได้ 404"""
    resp = client.post(
        "/api/v1/sessions",
        json={"plan_id": None},
        headers=auth_header(doctor_token["access_token"]),
    )
    assert resp.status_code == 404


def test_patient_adds_rep(client: TestClient, patient_token: dict, exercise_id: int):
    """ผู้ป่วยบันทึก rep ได้ และ total_reps เพิ่มขึ้น"""
    # เริ่ม session
    sess_resp = client.post(
        "/api/v1/sessions",
        json={"plan_id": None},
        headers=auth_header(patient_token["access_token"]),
    )
    session_id = sess_resp.json()["id"]

    # บันทึก rep
    rep_resp = client.post(
        f"/api/v1/sessions/{session_id}/reps",
        json={
            "exercise_id": exercise_id,
            "rep_number": 1,
            "accuracy_score": 88.5,
            "max_rom": 95.0,
            "duration_ms": 2500,
            "quality": "good",
            "feedback": "ทำได้ดีมาก",
        },
        headers=auth_header(patient_token["access_token"]),
    )
    assert rep_resp.status_code == 201
    rep_data = rep_resp.json()
    assert rep_data["rep_number"] == 1
    assert float(rep_data["accuracy_score"]) == 88.5
    assert rep_data["quality"] == "good"


def test_add_rep_to_nonexistent_session_returns_404(client: TestClient, patient_token: dict,
                                                      exercise_id: int):
    """บันทึก rep ใน session ที่ไม่มี ต้องได้ 404"""
    resp = client.post(
        "/api/v1/sessions/99999/reps",
        json={"exercise_id": exercise_id, "rep_number": 1},
        headers=auth_header(patient_token["access_token"]),
    )
    assert resp.status_code == 404


def test_patient_records_joint_angles(client: TestClient, patient_token: dict):
    """ผู้ป่วยบันทึก joint angles เป็นชุด (Time-Series)"""
    sess_resp = client.post(
        "/api/v1/sessions",
        json={"plan_id": None},
        headers=auth_header(patient_token["access_token"]),
    )
    session_id = sess_resp.json()["id"]

    angles_payload = {
        "angles": [
            {"timestamp_ms": 0, "joint_name": "left_knee", "angle_value": 90.5},
            {"timestamp_ms": 100, "joint_name": "left_knee", "angle_value": 85.2},
            {"timestamp_ms": 200, "joint_name": "left_knee", "angle_value": 75.0},
            {"timestamp_ms": 300, "joint_name": "left_knee", "angle_value": 10.0},
        ]
    }
    resp = client.post(
        f"/api/v1/sessions/{session_id}/angles",
        json=angles_payload,
        headers=auth_header(patient_token["access_token"]),
    )
    assert resp.status_code == 201
    assert resp.json()["saved"] == 4


def test_get_session_angles_returns_timeseries(client: TestClient, patient_token: dict):
    """ดึง time-series angles กลับมาได้ เรียงตาม timestamp"""
    sess_resp = client.post(
        "/api/v1/sessions",
        json={"plan_id": None},
        headers=auth_header(patient_token["access_token"]),
    )
    session_id = sess_resp.json()["id"]

    client.post(
        f"/api/v1/sessions/{session_id}/angles",
        json={
            "angles": [
                {"timestamp_ms": 200, "joint_name": "left_knee", "angle_value": 75.0},
                {"timestamp_ms": 0, "joint_name": "left_knee", "angle_value": 90.5},
                {"timestamp_ms": 100, "joint_name": "left_knee", "angle_value": 85.2},
            ]
        },
        headers=auth_header(patient_token["access_token"]),
    )

    resp = client.get(
        f"/api/v1/sessions/{session_id}/angles",
        headers=auth_header(patient_token["access_token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
    # ต้องเรียงตาม timestamp
    timestamps = [d["timestamp_ms"] for d in data]
    assert timestamps == sorted(timestamps)
    assert timestamps == [0, 100, 200]


def test_patient_completes_session(client: TestClient, patient_token: dict):
    """ผู้ป่วยปิดเซสชัน status=completed แล้ว ended_at ต้องถูกตั้ง"""
    sess_resp = client.post(
        "/api/v1/sessions",
        json={"plan_id": None},
        headers=auth_header(patient_token["access_token"]),
    )
    session_id = sess_resp.json()["id"]

    resp = client.patch(
        f"/api/v1/sessions/{session_id}",
        json={"status": "completed", "total_reps": 10, "accuracy_score_avg": 85.5},
        headers=auth_header(patient_token["access_token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "completed"
    assert data["total_reps"] == 10
    assert float(data["accuracy_score_avg"]) == 85.5
    assert data["ended_at"] is not None  # ตั้งอัตโนมัติเมื่อ completed


def test_get_nonexistent_session_angles_returns_404(client: TestClient, patient_token: dict):
    """ดึง angles ของ session ที่ไม่มี ต้องได้ 404"""
    resp = client.get(
        "/api/v1/sessions/99999/angles",
        headers=auth_header(patient_token["access_token"]),
    )
    assert resp.status_code == 404


def test_patient_lists_own_sessions(client: TestClient, patient_token: dict):
    """ผู้ป่วยดูประวัติเซสชันของตัวเอง (/sessions/mine)"""
    client.post(
        "/api/v1/sessions",
        json={"plan_id": None},
        headers=auth_header(patient_token["access_token"]),
    )
    client.post(
        "/api/v1/sessions",
        json={"plan_id": None},
        headers=auth_header(patient_token["access_token"]),
    )

    resp = client.get(
        "/api/v1/sessions/mine",
        headers=auth_header(patient_token["access_token"]),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 2
    # เรียงจากใหม่ไปเก่า
    started_ats = [s["started_at"] for s in data]
    assert started_ats == sorted(started_ats, reverse=True)


def test_full_session_lifecycle(client: TestClient, patient_token: dict, exercise_id: int):
    """E2E: เริ่ม session → บันทึก angles → บันทึก reps → ปิด session"""
    # 1. เริ่ม session
    sess_resp = client.post(
        "/api/v1/sessions",
        json={"plan_id": None},
        headers=auth_header(patient_token["access_token"]),
    )
    session_id = sess_resp.json()["id"]

    # 2. บันทึก angles ระหว่างฝึก
    client.post(
        f"/api/v1/sessions/{session_id}/angles",
        json={
            "angles": [
                {"timestamp_ms": i * 500, "joint_name": "left_knee", "angle_value": 90 - i * 5}
                for i in range(5)
            ]
        },
        headers=auth_header(patient_token["access_token"]),
    )

    # 3. บันทึก reps 3 ครั้ง
    for rep_num in range(1, 4):
        client.post(
            f"/api/v1/sessions/{session_id}/reps",
            json={
                "exercise_id": exercise_id,
                "rep_number": rep_num,
                "accuracy_score": 80 + rep_num,
                "quality": "good",
            },
            headers=auth_header(patient_token["access_token"]),
        )

    # 4. ปิด session
    end_resp = client.patch(
        f"/api/v1/sessions/{session_id}",
        json={"status": "completed", "accuracy_score_avg": 85.0},
        headers=auth_header(patient_token["access_token"]),
    )
    assert end_resp.status_code == 200
    assert end_resp.json()["status"] == "completed"
    assert end_resp.json()["total_reps"] == 3

    # 5. ตรวจ angles ทั้งหมด
    angles_resp = client.get(
        f"/api/v1/sessions/{session_id}/angles",
        headers=auth_header(patient_token["access_token"]),
    )
    assert len(angles_resp.json()) == 5
