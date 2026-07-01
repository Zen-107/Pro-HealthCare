"""Sync routes — Offline Mode: รับเซสชันที่ค้างในมือถือมาประมวลผลเป็นชุด"""
from datetime import timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession, get_current_patient_profile
from app.models.joint_angle import JointAngleRecord
from app.models.session import TherapySession, SessionRep
from app.schemas.sync import SyncBatchRequest, SyncBatchResult, SyncSessionResult

router = APIRouter()


def _idempotency_key(client_session_id: str, patient_id: int) -> str:
    """สร้าง device_info เพื่อ dedupe: ถ้าเคย sync client_session_id นี้แล้วจะข้าม"""
    return f"client:{patient_id}:{client_session_id}"


@router.post("/batch", response_model=SyncBatchResult)
def sync_batch(payload: SyncBatchRequest, user: CurrentUser, db: DbSession):
    """รับกลุ่มเซสชันจาก offline queue แล้วบันทึกทีเดียว"""
    patient = get_current_patient_profile(user, db)
    results: list[SyncSessionResult] = []
    created = skipped = errors = 0

    for s in payload.sessions:
        key = _idempotency_key(s.client_session_id, patient.id)
        # dedupe: ถ้ามีเซสชันที่มี device_info == key อยู่แล้ว ให้ข้าม
        existing = db.scalar(select(TherapySession).where(TherapySession.device_info == key))
        if existing:
            results.append(SyncSessionResult(
                client_session_id=s.client_session_id,
                server_session_id=existing.id,
                status="skipped",
                message="เคย sync แล้ว",
            ))
            skipped += 1
            continue

        try:
            started = s.started_at
            if started.tzinfo is None:
                started = started.replace(tzinfo=timezone.utc)
            session = TherapySession(
                patient_id=patient.id,
                plan_id=s.plan_id,
                started_at=started,
                ended_at=s.ended_at,
                status=s.status,
                total_reps=s.total_reps,
                accuracy_score_avg=s.accuracy_score_avg,
                device_info=key,
            )
            db.add(session)
            db.flush()

            for r in s.reps:
                db.add(SessionRep(session_id=session.id, **r.model_dump()))
            for a in s.angles:
                db.add(JointAngleRecord(session_id=session.id, **a.model_dump()))

            db.commit()
            db.refresh(session)
            results.append(SyncSessionResult(
                client_session_id=s.client_session_id,
                server_session_id=session.id,
                status="created",
            ))
            created += 1
        except Exception as e:  # noqa: BLE001 — rollback แล้วทำเซสชันถัดไป
            db.rollback()
            results.append(SyncSessionResult(
                client_session_id=s.client_session_id,
                server_session_id=None,
                status="error",
                message=str(e),
            ))
            errors += 1

    return SyncBatchResult(
        total=len(payload.sessions),
        created=created,
        skipped=skipped,
        errors=errors,
        results=results,
    )
