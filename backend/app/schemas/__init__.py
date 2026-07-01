"""ชุดรวมของ Pydantic schemas"""
from app.schemas.auth import Token, TokenData, LoginRequest, RegisterRequest
from app.schemas.user import UserOut, UserUpdate
from app.schemas.patient import PatientOut, PatientUpdate, PatientWithUser
from app.schemas.exercise import ExerciseOut, ExerciseCreate
from app.schemas.plan import (
    PlanItemCreate,
    PlanItemOut,
    ExercisePlanCreate,
    ExercisePlanOut,
)
from app.schemas.session import (
    SessionCreate,
    SessionUpdate,
    SessionOut,
    SessionRepCreate,
    SessionRepOut,
    JointAngleCreate,
)
from app.schemas.sync import SyncBatchRequest, SyncBatchResult
from app.schemas.report import ClinicalReportOut

__all__ = [
    "Token", "TokenData", "LoginRequest", "RegisterRequest",
    "UserOut", "UserUpdate",
    "PatientOut", "PatientUpdate", "PatientWithUser",
    "ExerciseOut", "ExerciseCreate",
    "PlanItemCreate", "PlanItemOut", "ExercisePlanCreate", "ExercisePlanOut",
    "SessionCreate", "SessionUpdate", "SessionOut",
    "SessionRepCreate", "SessionRepOut", "JointAngleCreate",
    "SyncBatchRequest", "SyncBatchResult",
    "ClinicalReportOut",
]
