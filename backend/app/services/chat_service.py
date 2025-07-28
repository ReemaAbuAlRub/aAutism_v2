import tempfile
from typing import Optional
from app.db.repository.convo_repo import ConversationRepository
from app.services.stt_service import STTService
from app.services.tts_service import TTSService
from app.services.image_service import ImageService
from app.services.llm.strategies import GPT4Strategy
from app.schemas.chat import ChatRequest, ChatResponse

class ChatService:
    def __init__(self, db):
        self.repo = ConversationRepository(db)
        self.stt = STTService()
        self.tts = TTSService()
        self.img = ImageService()
        self.llm = GPT4Strategy()


    async def send_message(self, req: ChatRequest) -> ChatResponse:
        
        self.repo.add_user_message(req)
        reply = await self.llm.generate(req)
        self.repo.add_assistant_message(reply)
        audio_b64 = self.tts.speech(reply)

        image = None
        if req.generate_image:
            image = await self.img.generate_image(prompt=reply)

        return ChatResponse(text=reply, audio_base64=audio_b64, image_url=image)


