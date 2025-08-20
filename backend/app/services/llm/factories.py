from abc import ABC, abstractmethod
from openai import AsyncOpenAI
from app.core.config import settings
from app.services.prompts.chat_prompt import build_messages

class BaseLlmFactory(ABC):
    @abstractmethod
    async def generate(self, message: str, autism_level :str, history: list[dict] = None) -> str:
        pass

    @abstractmethod
    async def get_embedding( self, text: str) -> list[float]:
        pass


class OPenAIFactory(BaseLlmFactory):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.GPT_MODEL
        self.temperature = 0.3

    async def generate(self, message: str, autism_level : str, history: list[dict] = None) -> str:
        messages=build_messages(
            user=message,
            history=history,
            level=autism_level
        )
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        return response.choices[0].message.content

    async def get_embedding( self, text: str) -> list[float]:
        resp = await self.client.embeddings.create( model=settings.EMBEDDING_MODEL, input=text )
        return resp.data[0].embedding

# class GPT4Factory(BaseLlmFactory):
#     def __init__(self):
#         self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
#         self.model = "gpt-4.1"
#         self.temperature = 0.2

#     async def generate(self, message: str, autism_level :str, history: list[dict] = None) -> str:
#         messages=build_messages(
#             user=message,
#             history=history,
#             level=autism_level
#         )
#         response = await self.client.chat.completions.create(
#             model=self.model,
#             messages=messages,
#             temperature=self.temperature,
#         )
#         return response.choices[0].message.content

#     async def get_embedding( self, text: str) -> list[float]:
#         resp = await self.client.embeddings.create( model=settings.EMBEDDING_MODEL, input=text )
#         return resp.data[0].embedding

class GoogleFactory(BaseLlmFactory):
    def __init__(self):
        pass

    async def generate(self, message: str, autism_level :str, history: list[dict] = None) -> str:
        pass

    async def get_embedding( self, text: str) -> list[float]:
        pass


class LLMFactory:
    @staticmethod
    def get_llm(provider: str) -> BaseLlmFactory:
        if provider == "OpenAI":
            return OPenAIFactory()
        elif provider == "google":
            return GoogleFactory()
        else:
            raise ValueError(f"Unknown LLM: {provider}")