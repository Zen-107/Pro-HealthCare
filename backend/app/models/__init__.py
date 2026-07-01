"""ชุดรวมของ ORM models — import ทุก model เพื่อให้ Alembic/Base.metadata เห็นครบ"""
from app.models.user import User
from app.models.patient import Patient
from app.models.exercise import Exercise
from app.models.exercise_plan import ExercisePlan, PlanItem
from app.models.session import Session, SessionRep
from app.models.joint_angle import JointAngleRecord
from app.models.clinical_report import ClinicalReport

__all__ = [
    "User",
    "Patient",
    "Exercise",
    "ExercisePlan",
    "PlanItem",
    "Session",
    "SessionRep",
    "JointAngleRecord",
    "ClinicalReport",
]
