from gtts import gTTS
import io
import base64

class TTSService:
    def __init__(self, lang: str = "ar"):
        self.lang = lang
    
    def speech(self, text:str) -> str:
        tts = gTTS(text=text, lang=self.lang)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        data = buf.read()
        return base64.b64encode(data).decode()