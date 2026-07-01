"""📷 Agent 1: Vision Tracker (The Eyes) — STUB

หน้าที่ (เมื่อ implement ใน Step 2):
- รับเฟรมจากกล้อง รัน MediaPipe Pose ดึงพิกัด (x, y, z) ของข้อต่อ
- คำนวณมุมข้อต่อ (Kinematics) จาก Vector 3 จุด
- ส่งค่า Coordinates/Angles แบบ Real-time

หมายเหตุ PDPA: ประมวลผล On-device (MediaPipe JS ใน WebView) ส่งขึ้น server เฉพาะ JSON
"""
from dataclasses import dataclass, field


@dataclass
class Landmark:
    """พิกัดข้อต่อหนึ่งจุด (ตรงกับ MediaPipe PoseLandmark)"""
    name: str
    x: float
    y: float
    z: float = 0.0
    visibility: float = 1.0


@dataclass
class AngleResult:
    """ผลลัพธ์การคำนวณมุมข้อต่อหนึ่งจุด"""
    joint_name: str
    angle: float
    target: float | None = None
    deviation: float | None = None


class VisionTracker:
    """STUB — จะเชื่อม MediaPipe ใน Step 2"""

    def __init__(self) -> None:
        self.is_running = False

    def process_frame(self, frame):  # noqa: ANN001
        """รับเฟรมภาพ -> คืน list[Landmark]

        Step 2: รัน MediaPipe Pose แล้วแปลงผลเป็น Landmark
        """
        raise NotImplementedError("VisionTracker ยังไม่ implement — อยู่ใน Step 2")

    @staticmethod
    def calculate_angle(a: Landmark, b: Landmark, c: Landmark) -> float:
        """คำนวณมุมที่จุด b จาก Vector 3 จุด (a-b-c) หน่วยเป็นองศา

        Step 2: เขียนด้วย numpy — atan2 ของ cross/dot product
        """
        raise NotImplementedError("calculate_angle ยังไม่ implement — อยู่ใน Step 2")

    def start(self) -> None:
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False
