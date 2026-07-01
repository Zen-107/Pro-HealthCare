"""FastAPI Dependencies — DB session และผู้ใช้ปัจจุบัน (จาก JWT)"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.enums import UserRole
from app.core.security import JWTError, decode_access_token
from app.models.user import User

# tokenUrl ใช้สำหรับ Swagger "Authorize" — ชี้ไป endpoint login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

DbSession = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(token: TokenDep, db: DbSession) -> User:
    """ถอด JWT แล้วดึง user จาก DB"""
    cred_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="ไม่สามารถยืนยันตัวตนได้ — token ไม่ถูกต้องหรือหมดอายุ",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise cred_error
        user_id = int(user_id)
    except (JWTError, ValueError):
        raise cred_error

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise cred_error
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_role(*allowed: UserRole):
    """Factory สร้าง dependency จำกัดบทบาท เช่น Depends(require_role(UserRole.DOCTOR))"""

    def _checker(user: CurrentUser) -> User:
        if UserRole(user.role) not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"สำหรับ {', '.join(r.value for r in allowed)} เท่านั้น",
            )
        return user

    return _checker


def get_current_patient_profile(user: CurrentUser, db: DbSession):
    """ดึง profile patient ของ user คนปัจจุบัน (import แบบ lazy เพื่อหลีก circular)"""
    from app.models.patient import Patient

    patient = db.scalar(select(Patient).where(Patient.user_id == user.id))
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ไม่พบข้อมูลผู้ป่วย — บัญชีนี้ยังไม่ได้ลงทะเบียนเป็นผู้ป่วย",
        )
    return patient
