from fastapi import APIRouter

from app.api.routes import chattts

api_router = APIRouter()
api_router.include_router(chattts.router, prefix="/chattts", tags=["chattts"])
