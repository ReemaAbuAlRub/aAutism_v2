import openai, requests, base64
from app.core.config import settings
from openai import AsyncOpenAI
from app.services.prompts.image_prompt import build_image_prompt

class ImageService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_image(self, request: str, n: int = 1, size: str = "1024x1024") -> str:


        resp = await self.openai_client.images.generate(
            prompt= build_image_prompt(request),
            n=n,
            size=size
        )
        
        first_image = resp.data[0]        
        url = first_image.url   
        
        r = requests.get(url)
        r.raise_for_status()
        img_bytes = r.content
        b64 = base64.b64encode(img_bytes).decode("utf-8")

        return b64