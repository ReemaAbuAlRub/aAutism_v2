import openai, requests, base64
from app.core.config import settings

class ImageService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def generate_image(self, prompt: str, n: int = 1, size: str = "512x512") -> str:
        resp = openai.Image.create(
            model= setttings.IMAGE_MODEL,
            prompt=prompt,
            n=n,
            size=size
        )
        
        url = resp["data"][0]["url"]
        r = requests.get(url)
        r.raise_for_status()
        img_bytes = r.content
        b64 = base64.b64encode(img_bytes).decode("utf-8")

        return b64