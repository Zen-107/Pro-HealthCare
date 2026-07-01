"""User schemas"""
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import UserRole


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    phone: str | None = None
    is_active: bool


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
