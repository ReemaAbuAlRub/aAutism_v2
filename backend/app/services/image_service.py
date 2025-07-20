import openai
from app.core.config import settings

class ImageService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def generate(self, prompt: str, n: int = 1, size: str = "512x512") -> str:
        resp = openai.Image.create(
            prompt=prompt,
            n=n,
            size=size
        )
        return resp['data'][0]['url']