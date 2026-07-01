"""ชุดรวม API routers"""
from fastapi import APIRouter

from app.api.routes import auth, users, exercises, plans, sessions, sync, reports

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
api_router.include_router(plans.router, prefix="/plans", tags=["Plans"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(sync.router, prefix="/sync", tags=["Sync (Offline)"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])

__all__ = ["api_router"]
