from fastapi import APIRouter
from api.v1 import chat_router

api_router=APIRouter()

# api_router.include_router(chat_router.router,  prefix="/chat", tags=["chat"])