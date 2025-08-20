import tempfile
from typing import List, Optional, Dict, Any
from app.db.repository.convo_repo import ConversationRepository
from app.services.stt_service import STTService
from app.services.tts_service import TTSService
from app.services.image_service import ImageService
from app.services.user_service import UserService
from app.services.llm.factories import LLMFactory
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.moderation_service import ModerationService
from app.core.config import settings
from app.db.models.user import User
from app.db.repository.embedding_repo import EmbeddingRepository
from starlette.concurrency import run_in_threadpool
import asyncio
import uuid
import time

# class ChatService:
#     def __init__(self, db, index, user:User):
#         self.repo = ConversationRepository(db)
#         self.stt = STTService()
#         self.tts = TTSService()
#         self.img = ImageService()
#         self.llm = LLMFactory.get_llm(provider=settings.PROVIDER)
#         self.embed_repo = EmbeddingRepository(index)
#         self.moderation = ModerationService()
#         self.autism_level = user.autism_level
#         self.user_id = user.id

#     def _matches_to_history(self, matches) -> List[Dict[str, str]]:
#         if not matches:
#             return []

#         def sort_key(m):
#             meta = getattr(m, "metadata", {}) or {}
#             ts = meta.get("ts")
#             return (0, ts) if ts is not None else (1, getattr(m, "score", 0.0))

#         ordered = sorted(matches, key=sort_key)

#         hist: List[Dict[str, str]] = []
#         for m in ordered:
#             meta = getattr(m, "metadata", {}) or {}
#             text = meta.get("text")
#             role = (meta.get("role") or "user").lower()
#             if not text:
#                 continue
#             role_norm = "assistant" if role.startswith("assist") else "user"
#             hist.append({"role": role_norm, "content": text})
#         return hist

#     async def send_message(self, req: ChatRequest) -> ChatResponse:
#         text=req.text
#         user_id_str=str(self.user_id)
#         turn_id = str(uuid.uuid4())

#         await self.moderation.check(text=text)
#         embed = await self.llm.get_embedding(text)
#         # sims = self.embed_repo.query(vector=embed, top_k=3, include_metadata=True, metadata_filter={"user_id": self.user_id} )
#         matches = self.embed_repo.query(
#             vector=embed,
#             top_k=5,
#             include_metadata=True,
#             metadata_filter={"user_id": user_id_str},
#         )
#         history = self._matches_to_history(matches)
#         print(history)
        
#         # context = [m.metadata["text"] for m in sims]
#         reply = await self.llm.generate(text, autism_level=self.autism_level, history=history)
        
#         self.embed_repo.upsert(id=f"{user_id_str}:{uuid.uuid4()}", vector=embed,metadata={"user_id": user_id_str,"role": "user","turn_id":turn_id,"text":text,"ts":int(time.time())})
#         emb2 = await  self.llm.get_embedding(reply)
#         self.embed_repo.upsert(id=f"{user_id_str}:{uuid.uuid4()}", vector=emb2, metadata={"user_id": user_id_str,"role": "assistant","turn_id":turn_id,"text": reply,"ts":int(time.time())})
        
#         tts_task = run_in_threadpool(self.tts.speech, reply)
#         refined = await self.llm.generate(f"Turn this into a visual scene description with less than 10 words for an image API:\n\n\"{reply}\"", autism_level=self.autism_level)
    
#         img_task = (self.img.generate_image(refined) if req.generate_image else  asyncio.sleep(0, result=None))
#         audio_b64, image_url = await asyncio.gather(tts_task, img_task)

#         return ChatResponse(text=reply, audio_base64=audio_b64, image_url=image_url)


# class ConversationSession:
#     """Simple in-memory or Redis-backed conversation session"""
    
#     def __init__(self, user_id: str, max_history: int = 20):
#         self.user_id = user_id
#         self.messages = []
#         self.max_history = max_history
#         self.session_id = str(uuid.uuid4())
#         self.created_at = time.time()
#         self.updated_at = time.time()
    
#     def add_message(self, role: str, content: str):
#         """Add a message to the conversation history"""
#         self.messages.append({
#             "role": role,
#             "content": content,
#             "timestamp": time.time()
#         })
        
#         # Trim history if it gets too long
#         if len(self.messages) > self.max_history:
#             self.messages = self.messages[-self.max_history:]
        
#         self.updated_at = time.time()
    
#     def get_history(self) -> List[Dict[str, str]]:
#         """Get conversation history in the format expected by LLM"""
#         return [{"role": msg["role"], "content": msg["content"]} for msg in self.messages]
    
#     def is_expired(self, timeout_hours: int = 24) -> bool:
#         """Check if session is expired"""
#         return (time.time() - self.updated_at) > (timeout_hours * 3600)
        
# class ChatService:
#     def __init__(self, db, index, user: User):
#         self.repo = ConversationRepository(db)
#         self.stt = STTService()
#         self.tts = TTSService()
#         self.img = ImageService()
#         self.llm = LLMFactory.get_llm(provider=settings.PROVIDER)
#         self.embed_repo = EmbeddingRepository(index)
#         self.moderation = ModerationService()
#         self.autism_level = user.autism_level
#         self.user_id = user.id
        
#         # Session storage (use Redis in production)
#         self.sessions = {}  # user_id -> ConversationSession
    
#     def get_or_create_session(self, user_id: str) -> ConversationSession:
#         """Get existing session or create a new one"""
#         if user_id not in self.sessions:
#             self.sessions[user_id] = ConversationSession(user_id)
#         elif self.sessions[user_id].is_expired():
#             # Create new session if expired
#             self.sessions[user_id] = ConversationSession(user_id)
        
#         return self.sessions[user_id]
    
#     async def send_message(self, req: ChatRequest) -> ChatResponse:
#         text = req.text
#         user_id_str = str(self.user_id)
#         turn_id = str(uuid.uuid4())

#         await self.moderation.check(text=text)
        
#         # Get current session
#         session = self.get_or_create_session(user_id_str)
        
#         # Get recent conversation history from session
#         history = session.get_history()

#         # Optionally enhance with semantic search for longer-term context
#         if len(history) < 4:  # If session is new/short, get contextual history
#             embed = await self.llm.get_embedding(text)
#             contextual_matches = self.embed_repo.query(
#                 vector=embed,
#                 top_k=6,
#                 include_metadata=True,
#                 metadata_filter={"user_id": user_id_str},
#             )
            
#             # Add relevant past context
#             for match in contextual_matches:
#                 meta = match.metadata or {}
#                 if meta.get("text") and len(history) < 10:
#                     role = "assistant" if meta.get("role", "").startswith("assist") else "user"
#                     history.insert(0, {"role": role, "content": meta["text"]})
        
#         print(f"Session history ({len(history)} messages):", history)

#         # Generate reply
#         reply = await self.llm.generate(text, autism_level=self.autism_level, history=history)
        
#         # Add to session
#         session.add_message("user", text)
#         session.add_message("assistant", reply)

#         # Store in vector database for long-term memory
#         embed = await self.llm.get_embedding(text)
#         current_ts = int(time.time())
        
#         self.embed_repo.upsert(
#             id=f"{user_id_str}:{turn_id}:user",
#             vector=embed,
#             metadata={
#                 "user_id": user_id_str,
#                 "role": "user",
#                 "turn_id": turn_id,
#                 "text": text,
#                 "ts": current_ts,
#                 "session_id": session.session_id
#             }
#         )
        
#         reply_embed = await self.llm.get_embedding(reply)
#         self.embed_repo.upsert(
#             id=f"{user_id_str}:{turn_id}:assistant",
#             vector=reply_embed,
#             metadata={
#                 "user_id": user_id_str,
#                 "role": "assistant", 
#                 "turn_id": turn_id,
#                 "text": reply,
#                 "ts": current_ts + 1,
#                 "session_id": session.session_id
#             }
#         )

#         # Generate TTS and image
#         tts_task = run_in_threadpool(self.tts.speech, reply)
#         refined = await self.llm.generate(
#             f"Turn this into a visual scene description with less than 10 words for an image API:\n\n\"{reply}\"",
#             autism_level=self.autism_level
#         )

#         img_task = (
#             self.img.generate_image(refined) 
#             if req.generate_image 
#             else asyncio.sleep(0, result=None)
#         )
        
#         audio_b64, image_url = await asyncio.gather(tts_task, img_task)

#         return ChatResponse(text=reply, audio_base64=audio_b64, image_url=image_url)


# import asyncio
# import uuid
# import time
# from starlette.concurrency import run_in_threadpool
# from typing import List, Dict
# from app.schemas.chat import ChatRequest, ChatResponse
# # ... keep your imports

# class ChatService:
#     user_sessions = {}

#     def __init__(self, db, index, user: User):
#         self.repo = ConversationRepository(db)
#         self.tts = TTSService()
#         self.img = ImageService()
#         self.llm = LLMFactory.get_llm(provider=settings.PROVIDER)
#         self.embed_repo = EmbeddingRepository(index)
#         self.moderation = ModerationService()
#         self.autism_level = user.autism_level
#         self.user_id = user.id

#     def get_conversation_history(self, user_id_str: str) -> List[Dict[str, str]]:
#         if user_id_str not in ChatService.user_sessions:
#             ChatService.user_sessions[user_id_str] = []
#         return ChatService.user_sessions[user_id_str].copy()

#     def add_message_to_history(self, user_id_str: str, role: str, content: str):
#         ChatService.user_sessions.setdefault(user_id_str, []).append({"role": role, "content": content})
#         if len(ChatService.user_sessions[user_id_str]) > 20:
#             ChatService.user_sessions[user_id_str] = ChatService.user_sessions[user_id_str][-20:]

#     async def _upsert_async(self, *args, **kwargs):
#         # Offload synchronous vectorstore upsert to a thread so we don’t block the loop
#         return await run_in_threadpool(self.embed_repo.upsert, *args, **kwargs)

#     async def send_message(self, req: ChatRequest) -> ChatResponse:
#         text = req.text
#         user_id_str = str(self.user_id)
#         turn_id = str(uuid.uuid4())
#         now_ts = int(time.time())

#         # 1) Moderation (must pass before anything else)
#         await self.moderation.check(text=text)

#         # 2) Get history (fast, in-mem)
#         history = self.get_conversation_history(user_id_str)

#         # 3) Kick off user text embedding ASAP (doesn’t depend on reply)
#         user_embed_task = asyncio.create_task(self.llm.get_embedding(text))

#         # 4) Main reply from LLM (critical path)
#         reply = await self.llm.generate(text, autism_level=self.autism_level, history=history)

#         # 5) Update in-memory history immediately (so next turn has it)
#         self.add_message_to_history(user_id_str, "user", text)
#         self.add_message_to_history(user_id_str, "assistant", reply)

#         # 6) After we have reply, start everything else **in parallel**
#         #    - reply embedding
#         #    - TTS (thread)
#         #    - refine prompt for image (LLM)
#         reply_embed_task = asyncio.create_task(self.llm.get_embedding(reply))
#         tts_task = asyncio.create_task(run_in_threadpool(self.tts.speech, reply))
#         refine_task = asyncio.create_task(
#             self.llm.generate(
#                 f'Turn this into a visual scene description with less than 10 words for an image API:\n\n"{reply}"',
#                 autism_level=self.autism_level,
#             )
#         )

#         # 7) While those run, upsert the user message as soon as its embedding is ready
#         try:
#             user_embed = await asyncio.wait_for(user_embed_task, timeout=6.0)
#             _ = asyncio.create_task(self._upsert_async(
#                 id=f"{user_id_str}:{turn_id}:user",
#                 vector=user_embed,
#                 metadata={
#                     "user_id": user_id_str, "role": "user",
#                     "turn_id": turn_id, "text": text, "timestamp": now_ts
#                 }
#             ))
#         except asyncio.TimeoutError:
#             # skip if too slow; don’t block user
#             user_embed = None

#         # 8) Prepare image gen (depends on refine)
#         image_task = None
#         image_url = None
#         if req.generate_image:
#             try:
#                 refined = await asyncio.wait_for(refine_task, timeout=4.0)
#                 image_task = asyncio.create_task(self.img.generate_image(refined))
#             except asyncio.TimeoutError:
#                 refined = None  # skip image if refine is slow

#         # 9) Wait for TTS + reply embedding + (maybe) image, but with timeouts so we don’t stall
#         audio_b64 = None
#         try:
#             audio_b64 = await asyncio.wait_for(tts_task, timeout=6.0)
#         except asyncio.TimeoutError:
#             audio_b64 = None  # return text without audio if slow

#         try:
#             reply_embed = await asyncio.wait_for(reply_embed_task, timeout=6.0)
#             _ = asyncio.create_task(self._upsert_async(
#                 id=f"{user_id_str}:{turn_id}:assistant",
#                 vector=reply_embed,
#                 metadata={
#                     "user_id": user_id_str, "role": "assistant",
#                     "turn_id": turn_id, "text": reply, "timestamp": now_ts + 1
#                 }
#             ))
#         except asyncio.TimeoutError:
#             reply_embed = None

#         if image_task is not None:
#             try:
#                 image_url = await asyncio.wait_for(image_task, timeout=20)
#             except asyncio.TimeoutError:
#                 image_url = None

#         # 10) Return immediately with whatever we have (text always; audio/image best-effort)
#         return ChatResponse(text=reply, audio_base64=audio_b64 or "" ,image_url=image_url)




# import asyncio
# import uuid
# import time
# from starlette.concurrency import run_in_threadpool
# from typing import List, Dict
# from app.schemas.chat import ChatRequest, ChatResponse
# from app.services.prompts.image_prompt import build_image_prompt,CharacterConsistencyManager

# class ChatService:
#     user_sessions = {}
#     user_characters = {}  # NEW: Store character info per user

#     def __init__(self, db, index, user: User):
#         self.repo = ConversationRepository(db)
#         self.tts = TTSService()
#         self.img = ImageService()
#         self.llm = LLMFactory.get_llm(provider=settings.PROVIDER)
#         self.embed_repo = EmbeddingRepository(index)
#         self.moderation = ModerationService()
#         self.autism_level = user.autism_level
#         self.user_id = user.id

#     def get_conversation_history(self, user_id_str: str) -> List[Dict[str, str]]:
#         if user_id_str not in ChatService.user_sessions:
#             ChatService.user_sessions[user_id_str] = []
#         return ChatService.user_sessions[user_id_str].copy()

#     def add_message_to_history(self, user_id_str: str, role: str, content: str):
#         ChatService.user_sessions.setdefault(user_id_str, []).append({"role": role, "content": content})
#         if len(ChatService.user_sessions[user_id_str]) > 20:
#             ChatService.user_sessions[user_id_str] = ChatService.user_sessions[user_id_str][-20:]

#     def get_or_create_character(self, user_id_str: str) -> dict:
#         """Get or create consistent character for user"""
#         if user_id_str not in ChatService.user_characters:
#             # Create default character based on autism level
#             if self.autism_level == "LVL1":
#                 char_desc = "friendly child with curious eyes, colorful casual clothes, approachable smile"
#             elif self.autism_level == "LVL2":
#                 char_desc = "gentle child with kind expression, simple comfortable clothing, calm demeanor"
#             else:  # LVL3
#                 char_desc = "peaceful child with soft features, plain comfortable clothes, serene expression"
            
#             ChatService.user_characters[user_id_str] = {
#                 'description': char_desc,
#                 'features': 'consistent appearance',
#                 'image_count': 0,
#                 'is_returning': False
#             }
        
#         char_info = ChatService.user_characters[user_id_str]
#         char_info['image_count'] += 1
#         char_info['is_returning'] = char_info['image_count'] > 1
        
#         return char_info

#     def get_or_create_character(self, user_id_str: str) -> dict:
#         """Get or create persistent character profile for user"""
#         if user_id_str not in ChatService.user_characters:
#             ChatService.user_characters[user_id_str] = CharacterConsistencyManager.create_detailed_character(
#                 user_id_str, self.autism_level
#             )

#         char_info = ChatService.user_characters[user_id_str]
#         char_info['image_count'] += 1
#         char_info['is_returning'] = char_info['image_count'] > 1
#         return char_info

#     def update_character_features(self, user_id_str: str, new_features: str):
#         """Update character features based on generated image"""
#         if user_id_str in ChatService.user_characters:
#             ChatService.user_characters[user_id_str]['features'] = new_features

#     async def _upsert_async(self, *args, **kwargs):
#         return await run_in_threadpool(self.embed_repo.upsert, *args, **kwargs)

#     async def send_message(self, req: ChatRequest) -> ChatResponse:
#         text = req.text
#         user_id_str = str(self.user_id)
#         turn_id = str(uuid.uuid4())
#         now_ts = int(time.time())

#         # 1) Moderation
#         await self.moderation.check(text=text)

#         # 2) Get history
#         history = self.get_conversation_history(user_id_str)

#         # 3) Kick off user text embedding
#         user_embed_task = asyncio.create_task(self.llm.get_embedding(text))

#         # 4) Main reply from LLM
#         reply = await self.llm.generate(text, autism_level=self.autism_level, history=history)

#         # 5) Update in-memory history
#         self.add_message_to_history(user_id_str, "user", text)
#         self.add_message_to_history(user_id_str, "assistant", reply)

#         # 6) Start parallel tasks
#         reply_embed_task = asyncio.create_task(self.llm.get_embedding(reply))
#         tts_task = asyncio.create_task(run_in_threadpool(self.tts.speech, reply))
        
#         # Enhanced refine task for better image prompts
#         refine_task = asyncio.create_task(
#             self.llm.generate(
#                 f'Turn this into a simple visual scene description (max 8 words, no text/books/signs): "{reply}"',
#                 autism_level=self.autism_level,
#             )
#         )

#         # 7) Upsert user message
#         try:
#             user_embed = await asyncio.wait_for(user_embed_task, timeout=6.0)
#             _ = asyncio.create_task(self._upsert_async(
#                 id=f"{user_id_str}:{turn_id}:user",
#                 vector=user_embed,
#                 metadata={
#                     "user_id": user_id_str, "role": "user",
#                     "turn_id": turn_id, "text": text, "timestamp": now_ts
#                 }
#             ))
#         except asyncio.TimeoutError:
#             user_embed = None

#         # 8) Prepare image generation with character consistency
#         image_task = None
#         image_url = None

#         if req.generate_image:
#             try:
#                 refined = await asyncio.wait_for(refine_task, timeout=20.0)
#                 character_info = self.get_or_create_character(user_id_str)  # persistent profile
#                 image_task = asyncio.create_task(
#                     self.img.generate_image(user_id_str, self.autism_level, refined, character_info)
#                 )
#             except asyncio.TimeoutError:
#                 refined = None
                
#         # 9) Wait for results
#         audio_b64 = None
#         try:
#             audio_b64 = await asyncio.wait_for(tts_task, timeout=6.0)
#         except asyncio.TimeoutError:
#             audio_b64 = None

#         try:
#             reply_embed = await asyncio.wait_for(reply_embed_task, timeout=6.0)
#             _ = asyncio.create_task(self._upsert_async(
#                 id=f"{user_id_str}:{turn_id}:assistant",
#                 vector=reply_embed,
#                 metadata={
#                     "user_id": user_id_str, "role": "assistant",
#                     "turn_id": turn_id, "text": reply, "timestamp": now_ts + 1
#                 }
#             ))
#         except asyncio.TimeoutError:
#             reply_embed = None

#         if image_task is not None:
#             try:
#                 image_url = await asyncio.wait_for(image_task, timeout=20)
                
#                 # Optional: Update character features based on successful generation
#                 if image_url and user_id_str in ChatService.user_characters:
#                     self.update_character_features(user_id_str, "established visual appearance")
                    
#             except asyncio.TimeoutError:
#                 image_url = None

#         return ChatResponse(text=reply, audio_base64=audio_b64 or "", image_url=image_url)


import asyncio
import uuid
import time
from starlette.concurrency import run_in_threadpool
from typing import List, Dict
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.prompts.image_prompt import build_image_prompt, CharacterConsistencyManager

# class ChatService:
#     user_sessions = {}
#     user_characters = {}  # Store character info per user

#     def __init__(self, db, index, user: User):
#         self.repo = ConversationRepository(db)
#         self.tts = TTSService()
#         self.img = ImageService()
#         self.llm = LLMFactory.get_llm(provider=settings.PROVIDER)
#         self.embed_repo = EmbeddingRepository(index)
#         self.moderation = ModerationService()
#         self.autism_level = user.autism_level
#         self.user_id = user.id

#     def get_conversation_history(self, user_id_str: str) -> List[Dict[str, str]]:
#         if user_id_str not in ChatService.user_sessions:
#             ChatService.user_sessions[user_id_str] = []
#         return ChatService.user_sessions[user_id_str].copy()

#     def add_message_to_history(self, user_id_str: str, role: str, content: str):
#         ChatService.user_sessions.setdefault(user_id_str, []).append({"role": role, "content": content})
#         if len(ChatService.user_sessions[user_id_str]) > 20:
#             ChatService.user_sessions[user_id_str] = ChatService.user_sessions[user_id_str][-20:]

#     def get_or_create_character(self, user_id_str: str) -> dict:
#         """Get or create persistent character profile for user"""
#         if user_id_str not in ChatService.user_characters:
#             # Create detailed character profile based on autism level
#             ChatService.user_characters[user_id_str] = CharacterConsistencyManager.create_detailed_character(
#                 user_id_str, self.autism_level
#             )
#             print(f"Created new character for user {user_id_str}: {ChatService.user_characters[user_id_str]}")

#         char_info = ChatService.user_characters[user_id_str]
#         char_info['image_count'] = char_info.get('image_count', 0) + 1
#         char_info['is_returning'] = char_info['image_count'] > 1
        
#         print(f"Using character (image #{char_info['image_count']}): {char_info}")
#         return char_info

#     async def _upsert_async(self, *args, **kwargs):
#         return await run_in_threadpool(self.embed_repo.upsert, *args, **kwargs)

#     async def send_message(self, req: ChatRequest) -> ChatResponse:
#         text = req.text
#         user_id_str = str(self.user_id)
#         turn_id = str(uuid.uuid4())
#         now_ts = int(time.time())

#         # 1) Moderation
#         await self.moderation.check(text=text)

#         # 2) Get history
#         history = self.get_conversation_history(user_id_str)

#         # 3) Kick off user text embedding
#         user_embed_task = asyncio.create_task(self.llm.get_embedding(text))

#         # 4) Main reply from LLM
#         reply = await self.llm.generate(text, autism_level=self.autism_level, history=history)

#         # 5) Update in-memory history
#         self.add_message_to_history(user_id_str, "user", text)
#         self.add_message_to_history(user_id_str, "assistant", reply)

#         # 6) Start parallel tasks
#         reply_embed_task = asyncio.create_task(self.llm.get_embedding(reply))
#         tts_task = asyncio.create_task(run_in_threadpool(self.tts.speech, reply))
        
#         # Enhanced refine task for better image prompts
#         refine_task = asyncio.create_task(
#             self.llm.generate(
#                 f'Turn this into a simple visual scene description (max 8 words, no text/books/signs): "{reply}"',
#                 autism_level=self.autism_level,
#             )
#         )

#         # 7) Upsert user message
#         try:
#             user_embed = await asyncio.wait_for(user_embed_task, timeout=6.0)
#             _ = asyncio.create_task(self._upsert_async(
#                 id=f"{user_id_str}:{turn_id}:user",
#                 vector=user_embed,
#                 metadata={
#                     "user_id": user_id_str, "role": "user",
#                     "turn_id": turn_id, "text": text, "timestamp": now_ts
#                 }
#             ))
#         except asyncio.TimeoutError:
#             user_embed = None

#         # 8) Prepare image generation with character consistency
#         image_task = None
#         image_url = None

#         if req.generate_image:
#             try:
#                 refined = await asyncio.wait_for(refine_task,timeout=60)
                
#                 # Get persistent character profile
#                 character_info = self.get_or_create_character(user_id_str)
                
#                 # Create image with consistent character
#                 image_task  = asyncio.create_task(
#                 self.img.generate_image(
#                     user_id=user_id_str,
#                     autism_level=self.autism_level, 
#                     scene_desc=refined_scene,  # Use the refined scene
#                     character_info=character_info,  # Pass the character info
#                     previous_images=None,
#                     n=1,
#                     size="1024x1024"
#                 )
#             )
#             except asyncio.TimeoutError:
#                 refined = None
                
#         # 9) Wait for results
#         audio_b64 = None
#         try:
#             audio_b64 = await asyncio.wait_for(tts_task, timeout=6.0)
#         except asyncio.TimeoutError:
#             audio_b64 = None

#         try:
#             reply_embed = await asyncio.wait_for(reply_embed_task, timeout=6.0)
#             _ = asyncio.create_task(self._upsert_async(
#                 id=f"{user_id_str}:{turn_id}:assistant",
#                 vector=reply_embed,
#                 metadata={
#                     "user_id": user_id_str, "role": "assistant",
#                     "turn_id": turn_id, "text": reply, "timestamp": now_ts + 1
#                 }
#             ))
#         except asyncio.TimeoutError:
#             reply_embed = None

#         if image_task is not None:
#             try:
#                 image_url = await asyncio.wait_for(image_task, timeout=60)
#                 print(f"Generated image URL: {image_url is not None}")
                    
#             except asyncio.TimeoutError:
#                 image_url = None
#                 print("Image generation timed out")

#         return ChatResponse(text=reply, audio_base64=audio_b64 or "", image_url=image_url)


import asyncio
import uuid
import time
from starlette.concurrency import run_in_threadpool
from typing import List, Dict
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.prompts.image_prompt import build_image_prompt, CharacterConsistencyManager

class ChatService:
    user_sessions = {}
    user_characters = {}  # Store character info per user

    def __init__(self, db, index, user: User):
        self.repo = ConversationRepository(db)
        self.tts = TTSService()
        self.img = ImageService()
        self.llm = LLMFactory.get_llm(provider=settings.PROVIDER)
        self.embed_repo = EmbeddingRepository(index)
        self.moderation = ModerationService()
        self.autism_level = user.autism_level
        self.user_id = user.id

    def get_conversation_history(self, user_id_str: str) -> List[Dict[str, str]]:
        if user_id_str not in ChatService.user_sessions:
            ChatService.user_sessions[user_id_str] = []
        return ChatService.user_sessions[user_id_str].copy()

    def add_message_to_history(self, user_id_str: str, role: str, content: str):
        ChatService.user_sessions.setdefault(user_id_str, []).append({"role": role, "content": content})
        if len(ChatService.user_sessions[user_id_str]) > 20:
            ChatService.user_sessions[user_id_str] = ChatService.user_sessions[user_id_str][-20:]

    def get_or_create_character(self, user_id_str: str) -> dict:
        """Get or create persistent character profile for user"""
        if user_id_str not in ChatService.user_characters:
            # Use the updated CharacterConsistencyManager method
            ChatService.user_characters[user_id_str] = CharacterConsistencyManager.get_or_create_character(
                user_id_str, self.autism_level
            )
            print(f"Created new character for user {user_id_str}: {ChatService.user_characters[user_id_str]}")

        char_info = ChatService.user_characters[user_id_str]
        
        # Update image count
        CharacterConsistencyManager.increment_image_count(user_id_str, self.autism_level)
        
        print(f"Using character (image #{char_info.get('image_count', 0)}): {char_info}")
        return char_info

    async def _upsert_async(self, *args, **kwargs):
        return await run_in_threadpool(self.embed_repo.upsert, *args, **kwargs)

    async def send_message(self, req: ChatRequest) -> ChatResponse:
        text = req.text
        user_id_str = str(self.user_id)
        turn_id = str(uuid.uuid4())
        now_ts = int(time.time())

        # 1) Moderation
        await self.moderation.check(text=text)

        # 2) Get history
        history = self.get_conversation_history(user_id_str)

        # 3) Kick off user text embedding
        user_embed_task = asyncio.create_task(self.llm.get_embedding(text))

        # 4) Main reply from LLM
        reply = await self.llm.generate(text, autism_level=self.autism_level, history=history)

        # 5) Update in-memory history
        self.add_message_to_history(user_id_str, "user", text)
        self.add_message_to_history(user_id_str, "assistant", reply)

        # 6) Start parallel tasks
        reply_embed_task = asyncio.create_task(self.llm.get_embedding(reply))
        tts_task = asyncio.create_task(run_in_threadpool(self.tts.speech, reply))
        
        # Enhanced refine task for better image prompts
        refine_task = asyncio.create_task(
            self.llm.generate(
                f'Extract the main visual scene from this response for a children\'s book illustration. '
                f'Return only a simple scene description (max 10 words): "{reply}"',
                autism_level=self.autism_level,
            )
        )

        # 7) Upsert user message
        try:
            user_embed = await asyncio.wait_for(user_embed_task, timeout=6.0)
            _ = asyncio.create_task(self._upsert_async(
                id=f"{user_id_str}:{turn_id}:user",
                vector=user_embed,
                metadata={
                    "user_id": user_id_str, "role": "user",
                    "turn_id": turn_id, "text": text, "timestamp": now_ts
                }
            ))
        except asyncio.TimeoutError:
            user_embed = None

        # 8) Prepare image generation with character consistency
        image_task = None
        image_url = None

        if req.generate_image:
            try:
                # Wait for refined scene description
                refined_scene = await asyncio.wait_for(refine_task, timeout=10.0)
                print(f"Refined scene for image: {refined_scene}")
                
                # Get persistent character profile
                character_info = self.get_or_create_character(user_id_str)
                
                # FIXED: Call generate_image with correct parameters
                image_task = asyncio.create_task(
                    self.img.generate_image(
                        user_id=user_id_str,
                        autism_level=self.autism_level, 
                        scene_desc=refined_scene,  # Use the refined scene
                        character_info=character_info,  # Pass the character info
                        previous_images=None,  # Optional: could track previous images
                        n=1,
                        size="1024x1024"
                    )
                )
                print(f"Started image generation task for scene: {refined_scene}")
                
            except asyncio.TimeoutError:
                print("Scene refinement timed out, using original user text")
                # Fallback to original user text if refinement fails
                character_info = self.get_or_create_character(user_id_str)
                image_task = asyncio.create_task(
                    self.img.generate_image(
                        user_id=user_id_str,
                        autism_level=self.autism_level,
                        scene_desc=text,  # Use original user text
                        character_info=character_info
                    )
                )
            except Exception as e:
                print(f"Error setting up image generation: {e}")
                image_task = None
                
        # 9) Wait for results
        audio_b64 = None
        try:
            audio_b64 = await asyncio.wait_for(tts_task, timeout=6.0)
        except asyncio.TimeoutError:
            audio_b64 = None

        try:
            reply_embed = await asyncio.wait_for(reply_embed_task, timeout=6.0)
            _ = asyncio.create_task(self._upsert_async(
                id=f"{user_id_str}:{turn_id}:assistant",
                vector=reply_embed,
                metadata={
                    "user_id": user_id_str, "role": "assistant",
                    "turn_id": turn_id, "text": reply, "timestamp": now_ts + 1
                }
            ))
        except asyncio.TimeoutError:
            reply_embed = None

        # Wait for image generation to complete
        if image_task is not None:
            try:
                image_url = await asyncio.wait_for(image_task, timeout=120)  # Increased timeout
                print(f"Image generation completed: {image_url is not None}")
                if image_url:
                    print(f"Generated image base64 length: {len(image_url)}")
                    
            except asyncio.TimeoutError:
                image_url = None
                print("Image generation timed out after 120 seconds")
            except Exception as e:
                image_url = None
                print(f"Image generation failed: {e}")

        return ChatResponse(text=reply, audio_base64=audio_b64 or "", image_url=image_url)

    # Optional: Add method to test image generation directly
    async def test_image_generation(self, scene_desc: str) -> str:
        """Test method for debugging image generation"""
        user_id_str = str(self.user_id)
        character_info = self.get_or_create_character(user_id_str)
        
        print(f"Testing image generation:")
        print(f"  Scene: {scene_desc}")
        print(f"  Character: {character_info}")
        
        try:
            result = await self.img.generate_image(
                user_id=user_id_str,
                autism_level=self.autism_level,
                scene_desc=scene_desc,
                character_info=character_info
            )
            print(f"Test generation successful: {len(result)} characters")
            return result
        except Exception as e:
            print(f"Test generation failed: {e}")
            raise

    # Optional: Add method to reset character for testing
    def reset_character(self, user_id_str: str = None):
        """Reset character for testing purposes"""
        target_user = user_id_str or str(self.user_id)
        if target_user in ChatService.user_characters:
            del ChatService.user_characters[target_user]
            print(f"Reset character for user {target_user}")
        
        # Also clear from CharacterConsistencyManager cache
        cache_key = f"{target_user}_{self.autism_level}"
        if hasattr(CharacterConsistencyManager, '_character_cache'):
            if cache_key in CharacterConsistencyManager._character_cache:
                del CharacterConsistencyManager._character_cache[cache_key]
                print(f"Cleared character cache for {cache_key}")

    # Optional: Add method to get character info for debugging
    def get_current_character(self, user_id_str: str = None) -> dict:
        """Get current character info for debugging"""
        target_user = user_id_str or str(self.user_id)
        return ChatService.user_characters.get(target_user, None)