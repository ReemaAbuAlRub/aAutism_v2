import tempfile
from typing import Optional
from app.db.repository.convo_repo import ConversationRepository
from app.services.stt_service import STTService
from app.services.tts_service import TTSService
from app.services.image_service import ImageService
from app.services.user_service import UserService
from app.services.llm.factories import LLMFactory
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.moderation_service import ModerationService
from app.core.config import settings
from app.db.models.user import User
from app.db.repository.embedding_repo import EmbeddingRepository
from starlette.concurrency import run_in_threadpool
import asyncio
import uuid

class ChatService:
    def __init__(self, db, index, user:User):
        self.repo = ConversationRepository(db)
        self.stt = STTService()
        self.tts = TTSService()
        self.img = ImageService()
        self.llm = LLMFactory.get_llm(provider=settings.PROVIDER)
        self.embed_repo = EmbeddingRepository(index)
        self.moderation = ModerationService()
        self.autism_level = user.autism_level
        self.user_id = user.id


    async def send_message(self, req: ChatRequest) -> ChatResponse:
        text=req.text
        user_id_str=str(self.user_id)
        turn_id = str(uuid.uuid4())

        await self.moderation.check(text=text)
        embed = await self.llm.get_embedding(text)
        self.embed_repo.upsert(id=f"{user_id_str}:{uuid.uuid4()}", vector=embed,metadata={"user_id": user_id_str,"role": "user","turn_id":turn_id,"text":text})
        
        sims = self.embed_repo.query(vector=embed, top_k=3)
        context = [m.metadata["text"] for m in sims]
        reply = await self.llm.generate(text, autism_level=self.autism_level, history=context)
        emb2 = await  self.llm.get_embedding(reply)
        self.embed_repo.upsert(id=f"{user_id_str}:{uuid.uuid4()}", vector=emb2, metadata={"user_id": user_id_str,"role": "assistant","turn_id":turn_id,"text": reply})
        
        tts_task = run_in_threadpool(self.tts.speech, reply)
        refined = await self.llm.generate(f"Turn this into a visual scene description with less that 10 words for an image API:\n\n\"{reply}\"", autism_level=self.autism_level)
        
        img_task = (self.img.generate_image(reply) if req.generate_image else  asyncio.sleep(0, result=None))
        audio_b64, image_url = await asyncio.gather(tts_task, img_task)

        return ChatResponse(text=reply, audio_base64=audio_b64, image_url=image_url)



