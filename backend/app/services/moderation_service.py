from openai import AsyncOpenAI
from fastapi import HTTPException, status
from app.core.config import settings

class ModerationService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODERATION

    async def check(self, text: str) -> None:
        resp = await self.client.moderations.create(model=self.model, input=[text])
        result = resp.results[0]

        if result.flagged:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Content violates policy.")
        


         