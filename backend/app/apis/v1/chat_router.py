from openai import OpenAI
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import tempfile
from app.schemas.chat import ChatResponse, ChatRequest
from app.services.chat_service import ChatService
from app.db.session import get_db
from app.db.vectorstore import get_vector_index
from app.db.redis_client import get_redis
from ...core.config import settings


router=APIRouter()

@router.post("/",response_model=ChatResponse)
async def chat( req: ChatRequest,db: Session = Depends(get_db) ):
    svc = ChatService(db)
    try:
        return await svc.send_message(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/moderation")
async def moderation():
    pass 
