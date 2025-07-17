import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    OPENAI_API_KEY:str = os.getenv("OPENAI_API_KEY")

settings = Settings()