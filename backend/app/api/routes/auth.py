"""Auth routes — register / login (OAuth2 password flow) / me"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, DbSession
from app.core.security import create_access_token, hash_password, verify_password
from app.models.patient import Patient
from app.models.user import User
from app.schemas.auth import RegisterRequest, Token
from app.schemas.user import UserOut

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: DbSession):
    """สมัครบัญชี — ถ้าเป็น patient จะสร้าง profile patient ให้อัตโนมัติ"""
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="อีเมลนี้ถูกใช้งานแล้ว",
        )

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role.value,
        phone=payload.phone,
    )
    db.add(user)
    db.flush()  # ได้ user.id

    # ผู้ป่วยอัตโนมัติมี profile patient
    if payload.role.value == "patient":
        db.add(Patient(user_id=user.id))

    db.commit()
    db.refresh(user)

    token = create_access_token(user.id, {"role": user.role})
    return Token(access_token=token, role=user.role, user_id=user.id)


@router.post("/login", response_model=Token)
def login(
    db: DbSession,
    form: OAuth2PasswordRequestForm = Depends(),
):
    """Login ด้วย OAuth2 password flow — Swagger ใช้ปุ่ม Authorize ได้"""
    user = db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="อีเมลหรือรหัสผ่านไม่ถูกต้อง",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="บัญชีถูกระงับการใช้งาน",
        )

    token = create_access_token(user.id, {"role": user.role})
    return Token(access_token=token, role=user.role, user_id=user.id)


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user
