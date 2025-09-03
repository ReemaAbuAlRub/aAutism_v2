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
import asyncio
import uuid
import time
from starlette.concurrency import run_in_threadpool
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
                
    def get_current_character(self, user_id_str: str = None) -> dict:
        """Get current character info for debugging"""
        target_user = user_id_str or str(self.user_id)
        return ChatService.user_characters.get(target_user, None)