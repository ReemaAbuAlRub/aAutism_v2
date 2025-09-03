# from abc import ABC, abstractmethod
# from openai import AsyncOpenAI
# from app.core.config import settings
# from app.services.prompts.chat_prompt import build_messages

# class BaseLlmStrategy(ABC):
#     @abstractmethod
#     async def generate(self, message: str, history: list[dict] = None) -> str:
#         pass

# class GPT35TurboStrategy(BaseLlmStrategy):
#     def __init__(self):
#         self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
#         self.model = "gpt-3.5 turbo"
#         self.temperature = 0.2

#     async def generate(self, message: str, history: list[dict] = None) -> str:
#         messages=build_messages(
#             user=message,
#             history=history
#         )
#         response = await self.client.chat.completions.create(
#             model=self.model,
#             messages=messages,
#             temperature=self.temperature,
#         )
#         return response.choices[0].message.content

# class GPT4Strategy(BaseLlmStrategy):
#     def __init__(self):
#         self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
#         self.model = "gpt-4.1"
#         self.temperature = 0.2

#     async def generate(self, message: str, history: list[dict] = None) -> str:
#         messages=build_messages(
#             user=message,
#             history=history
#         )
#         response = await self.client.chat.completions.create(
#             model=self.model,
#             messages=messages,
#             temperature=self.temperature,
#         )
#         return response.choices[0].message.content