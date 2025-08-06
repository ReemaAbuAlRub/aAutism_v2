from openai import OpenAI
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import tempfile
from app.schemas.chat import ChatResponse, ChatRequest
from app.services.chat_service import ChatService
from app.services.moderation_service import ModerationService
from app.db.session import get_db
from ...dependencies.auth import get_current_user
from app.db.vectorstore import get_vector_index
from app.db.models.user import User
from ...core.config import settings
from pinecone import Pinecone
import pinecone


router=APIRouter()

@router.post("/",response_model=ChatResponse)
async def chat( req: ChatRequest ,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    index=get_vector_index()
    svc = ChatService(db,index,current_user)
    try:
        print(req)
        return await svc.send_message(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/moderation")
async def moderation(text: str, moderation_service:ModerationService = Depends(ModerationService)):
    await moderation_service.check(text)
    return {"detail": "OK"} 
