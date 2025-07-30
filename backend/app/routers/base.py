from fastapi import APIRouter
from app.routers.v1 import chat_router
from app.routers.v1 import user_router

api_router=APIRouter()

api_router.include_router(chat_router.router,  prefix="/api/v1/chat", tags=["chat"])
api_router.include_router(user_router.router,  prefix="/api/v1/user", tags=["user"])