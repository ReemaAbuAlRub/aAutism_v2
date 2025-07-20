import openai
from app.core.config import settings

class STTService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def transcribe(self, audio_file_path:str ) -> str:
        with open(audio_file_path, "rb") as f:
                        resp = openai.Audio.transcribe("whisper-1", f)
        return resp.get("text", "")

    


