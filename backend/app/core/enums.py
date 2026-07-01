"""ค่าคงที่และ enum ที่ใช้ทั่วระบบ"""
from enum import Enum


class UserRole(str, Enum):
    """บทบาทผู้ใช้ — ผู้ป่วย / แพทย์ / ผู้ดูแลระบบ"""

    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class PlanStatus(str, Enum):
    """สถานะแผนกายภาพ — แพทย์เป็นผู้ควบคุม (Human-in-the-loop)"""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SessionStatus(str, Enum):
    """สถานะเซสชันฝึก"""

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class RepQuality(str, Enum):
    """คุณภาพของแต่ละ rep (จาก Form/ROM check)"""

    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
