import tempfile
from typing import Optional
from app.db.repositories.convo_repo import ConversationRepository
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

    async def send_message(self, text: Optional[str], audio_file_path: Optional[str], generate_image: bool) -> ChatResponse:
        if audio_file_path:
            text = await self.stt.transcribe(audio_file_path)

        self.repo.add_user_message(text)
        reply = await self.llm.generate(text)
        self.repo.add_assistant_message(reply)
        audio_b64 = self.tts.speech(reply)

        image_url = None
        if generate_image:
            image_url = await self.img.generate(prompt=text)

        return ChatResponse(text=reply, audio_base64=audio_b64, image_url=image_url)


