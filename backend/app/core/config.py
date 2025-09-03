import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

class Settings:
    OPENAI_API_KEY:str = os.getenv("OPENAI_API_KEY")
    IMAGE_MODEL: str = "gpt-4.1"
    POSTGRES_USER : str = os.getenv("POSTGRES_USER","reema")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : int = 5432
    POSTGRES_DB : str = os.getenv("POSTGRES_DB","chatbot")
    DATABASE_URL: str = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    REDIS_HOST: str = os.getenv("REDIS_HOST","localhost")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV: str = os.getenv("PINECONE_ENV")
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(60)
    MODERATION: str = os.getenv("MODERATION")
    PROVIDER: str = os.getenv("PROVIDER")
    EMBEDDING_MODEL:str = os.getenv("EMBEDDING_MODEL")
    GPT_MODEL: str = os.getenv("GPT_MODEL")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")


settings = Settings()

