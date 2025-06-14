from fastapi import APIRouter
from api.v1.handlers.user_handler import router


api_router = APIRouter()
api_router.include_router(router, prefix="/users", tags=["users"])

