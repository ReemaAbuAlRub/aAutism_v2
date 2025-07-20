from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    text: Optional[str]
    generate_image: bool=False

class ChatResponse(BaseModel): 
    text:str
    audio_base64: str
    image_url: Optional[str] = None
    
