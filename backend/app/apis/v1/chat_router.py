from fastapi import  APIRouter
from openai import OpenAI
from core.config import settings


router=APIRouter()

@route.post("/chat")
async def chat():
    client=OpenAI(api_key=settings.OPENAI_API_KEY)
    completion= client.chat.completions.create(
        
    )

@router.post("/moderation")
async def moderation():
    pass 
