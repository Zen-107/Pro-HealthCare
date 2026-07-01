"""Seed script — สร้างข้อมูลตัวอย่าง 10 ท่ากายภาพบำบัด (Ground Truth)

รันด้วย:
    uv run python -m app.seeds.seed_exercises

สคริปต์นี้ idempotent — ถ้า exercise ชื่อเดียวกันอยู่แล้วจะข้าม
"""
from __future__ import annotations

import sys
from pathlib import Path

# ทำให้ backend root อยู่ใน sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.exercise import Exercise

# -------------------------------------------------------------------
# ข้อมูลตัวอย่าง 10 ท่ากายภาพบำบัด
# ideal_angles: { joint_name: { min, max, target } } หน่วย degrees
# min/max = ช่วงที่ยอมรับได้, target = มุมมาตรฐาน (Ground Truth)
# -------------------------------------------------------------------

SEED_EXERCISES: list[dict] = [
    {
        "name": "Knee Extension",
        "name_th": "เเข้งขาตรง",
        "category": "knee",
        "difficulty": "easy",
        "target_joints": ["left_knee", "right_knee"],
        "ideal_angles": {
            "left_knee": {"min": 0, "max": 15, "target": 5},
            "right_knee": {"min": 0, "max": 15, "target": 5},
        },
        "instructions": "นั่งบนเก้าอี้ ยกขาขึ้นจนตรง ค้าง 3-5 วินาที ค่อยๆ ลง",
    },
    {
        "name": "Straight Leg Raise",
        "name_th": "ยกขาตรงขึ้น",
        "category": "knee",
        "difficulty": "easy",
        "target_joints": ["left_hip", "right_hip"],
        "ideal_angles": {
            "left_hip": {"min": 30, "max": 70, "target": 45},
            "right_hip": {"min": 30, "max": 70, "target": 45},
        },
        "instructions": "นอนหงาย ยกขาขึ้นตรงเหนือพื้น 30-45 องศา ค้าง 3 วินาที",
    },
    {
        "name": "Shoulder Flexion",
        "name_th": "ยกแขนขึ้นด้านหน้า",
        "category": "shoulder",
        "difficulty": "easy",
        "target_joints": ["left_shoulder", "right_shoulder"],
        "ideal_angles": {
            "left_shoulder": {"min": 150, "max": 180, "target": 170},
            "right_shoulder": {"min": 150, "max": 180, "target": 170},
        },
        "instructions": "ยกแขนขึ้นด้านหน้าให้สูงสุด ค้าง 3 วินาที ค่อยลง",
    },
    {
        "name": "Shoulder Abduction",
        "name_th": "กางแขนข้าง",
        "category": "shoulder",
        "difficulty": "medium",
        "target_joints": ["left_shoulder", "right_shoulder"],
        "ideal_angles": {
            "left_shoulder": {"min": 140, "max": 180, "target": 160},
            "right_shoulder": {"min": 140, "max": 180, "target": 160},
        },
        "instructions": "ยกแขนออกข้างให้สูงสุด ค้าง 3 วินาที ค่อยลง",
    },
    {
        "name": "Hip Abduction",
        "name_th": "กางขาข้าง",
        "category": "hip",
        "difficulty": "easy",
        "target_joints": ["left_hip", "right_hip"],
        "ideal_angles": {
            "left_hip": {"min": 25, "max": 45, "target": 35},
            "right_hip": {"min": 25, "max": 45, "target": 35},
        },
        "instructions": "นอนข้าง ยกขาขึ้นข้างบน 30-40 องศา ค้าง 3 วินาที",
    },
    {
        "name": "Ankle Dorsiflexion",
        "name_th": "งอเท้าขึ้น",
        "category": "ankle",
        "difficulty": "easy",
        "target_joints": ["left_ankle", "right_ankle"],
        "ideal_angles": {
            "left_ankle": {"min": 10, "max": 20, "target": 15},
            "right_ankle": {"min": 10, "max": 20, "target": 15},
        },
        "instructions": "นั่งพับขา ดึงปลายเท้าเข้าหาตัวให้มากที่สุด ค้าง 5 วินาที",
    },
    {
        "name": "Wall Push-up",
        "name_th": "กดพื้นกำแพง",
        "category": "shoulder",
        "difficulty": "easy",
        "target_joints": ["left_elbow", "right_elbow"],
        "ideal_angles": {
            "left_elbow": {"min": 60, "max": 90, "target": 75},
            "right_elbow": {"min": 60, "max": 90, "target": 75},
        },
        "instructions": "ยืนห่างกำแพง กดลงจนแขนเอียง 70-80 องศา ดันกลับ",
    },
    {
        "name": "Bridge Exercise",
        "name_th": "ยกสะโพก",
        "category": "hip",
        "difficulty": "medium",
        "target_joints": ["left_hip", "right_hip"],
        "ideal_angles": {
            "left_hip": {"min": 0, "max": 30, "target": 15},
            "right_hip": {"min": 0, "max": 30, "target": 15},
        },
        "instructions": "นอนหงาย เกร็งกล้ามเนื้อสะโพกยกขึ้น ค้าง 5 วินาที ค่อยลง",
    },
    {
        "name": "Neck Rotation",
        "name_th": "หมุนคอ",
        "category": "neck",
        "difficulty": "easy",
        "target_joints": ["neck"],
        "ideal_angles": {
            "neck": {"min": 60, "max": 80, "target": 70},
        },
        "instructions": "หมุนคอไปทางซ้าย-ขวาช้าๆ จนรู้สึกยืด ค้าง 3 วินาที",
    },
    {
        "name": "Wrist Extension",
        "name_th": "งอข้อมือขึ้น",
        "category": "wrist",
        "difficulty": "easy",
        "target_joints": ["left_wrist", "right_wrist"],
        "ideal_angles": {
            "left_wrist": {"min": 40, "max": 60, "target": 50},
            "right_wrist": {"min": 40, "max": 60, "target": 50},
        },
        "instructions": "วางแขนบนโต๊ะ ยกมือขึ้นช้าๆ ค้าง 3 วินาที ค่อยลง",
    },
]


def seed() -> None:
    """สร้างข้อมูล exercise ตัวอย่าง — skip ถ้าชื่อซ้ำ"""
    with SessionLocal() as db:
        existing_names = {
            name
            for (name,) in db.execute(select(Exercise.name)).all()
        }

        created = skipped = 0
        for data in SEED_EXERCISES:
            if data["name"] in existing_names:
                skipped += 1
                continue

            db.add(Exercise(**data))
            created += 1

        db.commit()

        print(f"✅ Seed complete: {created} created, {skipped} skipped (already exist)")


if __name__ == "__main__":
    seed()
