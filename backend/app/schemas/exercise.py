"""Exercise schemas"""
from pydantic import BaseModel, ConfigDict, Field


class ExerciseCreate(BaseModel):
    name: str = Field(max_length=200)
    name_th: str | None = Field(default=None, max_length=200)
    category: str | None = Field(default=None, max_length=100)
    difficulty: str = Field(default="easy", max_length=20)
    target_joints: list[str] | None = None
    ideal_angles: dict | None = None
    instructions: str | None = None
    video_url: str | None = Field(default=None, max_length=500)


class ExerciseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    name_th: str | None = None
    category: str | None = None
    difficulty: str
    target_joints: list[str] | None = None
    ideal_angles: dict | None = None
    instructions: str | None = None
    video_url: str | None = None
