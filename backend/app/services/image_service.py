# import openai, requests, base64
# from app.core.config import settings
# from openai import AsyncOpenAI
# from app.services.prompts.image_prompt import build_image_prompt,CharacterConsistencyManager

# class ImageService:
#     def __init__(self):
#         self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

#     async def generate_image(self, user_id: str, autism_level: str, scene_desc: str, character_info: dict, n: int = 1, size: str = "1024x1024") -> str:
#         """Generate image with consistent character features"""
#         # Always reuse stored character description
#         character_specs = CharacterConsistencyManager.get_character_description_string(character_info)

#         prompt = build_image_prompt(scene_desc,character_specs)

#         resp = await self.openai_client.images.generate(prompt=prompt, n=n, size=size)

#         first_image = resp.data[0]
#         url = first_image.url

#         r = requests.get(url)
#         r.raise_for_status()
#         img_bytes = r.content
#         b64 = base64.b64encode(img_bytes).decode("utf-8")

#         return b64


# import openai, requests, base64
# from app.core.config import settings
# from openai import AsyncOpenAI
# from app.services.prompts.image_prompt import build_image_prompt, CharacterConsistencyManager

# class ImageService:
#     def __init__(self):
#         self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

#     async def generate_image(self, user_id: str, autism_level: str, scene_desc: str, character_info: dict, n: int = 1, size: str = "1024x1024") -> str:
#         """Generate image with consistent character features"""
        
#         # Debug logging
#         print(f"ImageService.generate_image called with:")
#         print(f"  user_id: {user_id}")
#         print(f"  autism_level: {autism_level}")
#         print(f"  scene_desc: {scene_desc}")
#         print(f"  character_info type: {type(character_info)}")
#         print(f"  character_info: {character_info}")
        
#         # Ensure character_info is a dict, not a string
#         if isinstance(character_info, str):
#             print("ERROR: character_info is a string, not a dict!")
#             # If it's already a string description, use it directly
#             character_specs = character_info
#         elif isinstance(character_info, dict):
#             # Convert character dict to description string
#             character_specs = CharacterConsistencyManager.get_character_description_string(character_info)
#         else:
#             print(f"ERROR: Unexpected character_info type: {type(character_info)}")
#             character_specs = "friendly animated child character"
        
#         print(f"  Final character_specs: {character_specs}")
        
#         # Build the image prompt
#         prompt = build_image_prompt(scene_desc, character_specs)
#         print(f"  Generated prompt length: {len(prompt)}")
#         print(f"  Generated prompt preview: {prompt[:200]}...")

#         try:
#             # Generate image with DALL-E
#             resp = await self.openai_client.images.generate(prompt=prompt, n=n, size=size)
            
#             first_image = resp.data[0]
#             url = first_image.url
            
#             # Download and convert to base64
#             r = requests.get(url)
#             r.raise_for_status()
#             img_bytes = r.content
#             b64 = base64.b64encode(img_bytes).decode("utf-8")
            
#             print(f"  Successfully generated image, base64 length: {len(b64)}")
#             return b64
            
#         except Exception as e:
#             print(f"  ERROR generating image: {str(e)}")
#             print(f"  Prompt that caused error: {prompt}")
#             raise


# import openai, requests, base64
# from app.core.config import settings
# from openai import AsyncOpenAI
# from app.services.prompts.image_prompt import build_image_prompt, CharacterConsistencyManager
# from typing import Optional, Dict, List

# class ImageService:
#     def __init__(self):
#         self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

#     async def enhance_prompt_with_gpt4_vision(self, scene_desc: str, character_specs: str, previous_images: List[str] = None) -> str:
#         """Use GPT-4 Vision to analyze previous images and enhance consistency"""
        
#         if not previous_images:
#             # First image - just enhance the basic prompt
#             messages = [
#                 {
#                     "role": "user",
#                     "content": f"""Create a detailed DALL-E prompt for a 2D cartoon animated children's book illustration.

# Character: {character_specs}
# Scene: {scene_desc}

# Requirements:
# - 2D cartoon animation style only (like Disney Junior/PBS Kids)
# - Thick black outlines, flat pastel colors
# - NO text, letters, words, or writing anywhere
# - Child-friendly and warm
# - Consistent character appearance

# Generate an enhanced DALL-E prompt (max 1000 characters):"""
#                 }
#             ]
#         else:
#             # Analyze previous images for consistency
#             content = [
#                 {
#                     "type": "text",
#                     "text": f"""Analyze these previous images of the same character and create a DALL-E prompt that maintains perfect visual consistency.

# Character should be: {character_specs}
# New scene: {scene_desc}

# Look at the previous images and note:
# - Exact hair color, style, and length
# - Clothing details and colors  
# - Facial features and proportions
# - Skin tone
# - Overall art style

# Create a DALL-E prompt that will generate the SAME character in the new scene. Focus on maintaining identical visual appearance.

# Requirements:
# - 2D cartoon animation style
# - NO text/letters/words
# - Same character as shown in previous images
# - Max 1000 characters

# Enhanced DALL-E prompt:"""
#                 }
#             ]
            
#             # Add previous images for analysis
#             for img_b64 in previous_images[-2:]:  # Analyze last 2 images
#                 content.append({
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/png;base64,{img_b64}",
#                         "detail": "high"
#                     }
#                 })
            
#             messages = [{"role": "user", "content": content}]

#         try:
#             response = await self.openai_client.chat.completions.create(
#                 model="gpt-4o",  # GPT-4 with vision
#                 messages=messages,
#                 max_tokens=500,
#                 temperature=0.3
#             )
            
#             enhanced_prompt = response.choices[0].message.content.strip()
#             print(f"GPT-4 Vision enhanced prompt: {enhanced_prompt}")
#             return enhanced_prompt
            
#         except Exception as e:
#             print(f"GPT-4 Vision enhancement failed: {e}")
#             # Fallback to original method
#             return build_image_prompt(scene_desc, character_specs)

#     async def generate_image(self, user_id: str, autism_level: str, scene_desc: str, character_info: dict, 
#                            previous_images: List[str] = None, n: int = 1, size: str = "1024x1024") -> str:
#         """Generate image with GPT-4 Vision enhanced consistency"""
        
#         print(f"ImageService.generate_image called with:")
#         print(f"  user_id: {user_id}")
#         print(f"  autism_level: {autism_level}")
#         print(f"  scene_desc: {scene_desc}")
#         print(f"  character_info type: {type(character_info)}")
#         print(f"  previous_images count: {len(previous_images) if previous_images else 0}")
        
#         # Convert character info to description string
#         if isinstance(character_info, str):
#             character_specs = character_info
#         elif isinstance(character_info, dict):
#             character_specs = CharacterConsistencyManager.get_character_description_string(character_info)
#         else:
#             print(f"ERROR: Unexpected character_info type: {type(character_info)}")
#             character_specs = "friendly animated child character"
        
#         # Use GPT-4 Vision to enhance the prompt for consistency
#         enhanced_prompt = await self.enhance_prompt_with_gpt4_vision(
#             scene_desc, character_specs, previous_images
#         )

#         try:
#             # Generate image with DALL-E using enhanced prompt
#             resp = await self.openai_client.images.generate(
#                 prompt=enhanced_prompt, 
#                 model="dall-e-3",  # Use DALL-E 3 for best quality
#                 n=n, 
#                 size=size,
#                 quality="standard"
#             )
            
#             first_image = resp.data[0]
#             url = first_image.url
            
#             # Download and convert to base64
#             r = requests.get(url)
#             r.raise_for_status()
#             img_bytes = r.content
#             b64 = base64.b64encode(img_bytes).decode("utf-8")
            
#             print(f"Successfully generated image, base64 length: {len(b64)}")
#             return b64
            
#         except Exception as e:
#             print(f"ERROR generating image: {str(e)}")
#             print(f"Prompt that caused error: {enhanced_prompt}")
#             raise

#     async def analyze_image_consistency(self, current_image: str, reference_image: str, character_specs: str) -> Dict:
#         """Use GPT-4 Vision to analyze how consistent two images are"""
        
#         messages = [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": f"""Compare these two images of the same character and rate their visual consistency.

# Expected character: {character_specs}

# Rate consistency (1-10) for:
# - Hair color and style
# - Clothing
# - Facial features  
# - Body proportions
# - Art style
# - Overall character identity

# Provide a JSON response with scores and suggestions for improvement."""
#                     },
#                     {
#                         "type": "image_url", 
#                         "image_url": {
#                             "url": f"data:image/png;base64,{reference_image}",
#                             "detail": "high"
#                         }
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/png;base64,{current_image}", 
#                             "detail": "high"
#                         }
#                     }
#                 ]
#             }
#         ]

#         try:
#             response = await self.openai_client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=messages,
#                 max_tokens=300,
#                 temperature=0.1
#             )
            
#             analysis = response.choices[0].message.content
#             print(f"Consistency analysis: {analysis}")
#             return {"analysis": analysis}
            
#         except Exception as e:
#             print(f"Image consistency analysis failed: {e}")
#             return {"error": str(e)}



import openai, requests, base64, json
from app.core.config import settings
from openai import AsyncOpenAI
from app.services.prompts.image_prompt import build_image_prompt, CharacterConsistencyManager, SceneTranslator
from typing import Optional, Dict, List

class ImageService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.scene_translator = SceneTranslator(self.openai_client)


    async def debug_gpt4_vision_call(self, scene_desc: str, character_specs: str) -> Dict:
        """Debug version that logs everything about the GPT-4 Vision call"""
        
        # Simple test message first
        test_messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant for creating children's book illustrations."
            },
            {
                "role": "user", 
                "content": f"""Create a DALL-E prompt for: {scene_desc}

                Character: {character_specs}

                Make it child-friendly, 2D cartoon style, no text."""
                            }
                        ]
                        
        print("=== DEBUG GPT-4 Vision Call ===")
        print(f"Scene description: {scene_desc}")
        print(f"Character specs: {character_specs}")
        print(f"Messages being sent: {json.dumps(test_messages, indent=2, ensure_ascii=False)}")
        
        try:
            print("Making API call to GPT-4o...")
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=test_messages,
                max_tokens=300,
                temperature=0.2
            )
            
            result = response.choices[0].message.content.strip()
            print(f"GPT-4o Response: {result}")
            
            # Log the full response object for debugging
            print(f"Full response object: {response}")
            print(f"Finish reason: {response.choices[0].finish_reason}")
            
            return {
                "success": True,
                "response": result,
                "full_response": response.model_dump(),
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            print(f"GPT-4o API Error: {str(e)}")
            print(f"Error type: {type(e)}")
            
            # Log the specific error details
            if hasattr(e, 'response'):
                print(f"Error response: {e.response}")
            if hasattr(e, 'body'):
                print(f"Error body: {e.body}")
                
            return {
                "success": False,
                "error": str(e),
                "error_type": str(type(e))
            }

    async def test_direct_dalle_call(self, prompt: str) -> Dict:
        """Test DALL-E directly with a simple prompt"""
        
        print("=== DEBUG Direct DALL-E Call ===")
        print(f"Prompt: {prompt}")
        
        try:
            response = await self.openai_client.images.generate(
                prompt=prompt,
                model="dall-e-3",
                n=1,
                size="1024x1024",
                quality="standard"
            )
            
            print(f"DALL-E Response: {response}")
            return {"success": True, "response": response}
            
        except Exception as e:
            print(f"DALL-E Error: {str(e)}")
            print(f"Error type: {type(e)}")
            
            # Parse the error for more details
            error_details = {}
            if hasattr(e, 'response') and e.response:
                try:
                    error_body = e.response.json()
                    error_details = error_body.get('error', {})
                    print(f"Detailed error: {error_details}")
                except:
                    pass
            
            return {
                "success": False,
                "error": str(e),
                "error_type": str(type(e)),
                "error_details": error_details
            }

    async def test_simple_arabic_processing(self, arabic_text: str) -> Dict:
        """Test how GPT-4 handles simple Arabic text"""
        
        print("=== DEBUG Arabic Text Processing ===")
        print(f"Arabic text: {arabic_text}")
        
        # Test 1: Simple translation
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": f"Translate to English: {arabic_text}"}
                ],
                max_tokens=100
            )
            
            translation = response.choices[0].message.content
            print(f"Translation: {translation}")
            
            return {"success": True, "translation": translation}
            
        except Exception as e:
            print(f"Arabic processing error: {str(e)}")
            return {"success": False, "error": str(e)}

    # async def comprehensive_debug(self, user_id: str, scene_desc: str, character_info: dict) -> Dict:
    #     """Run comprehensive debugging for the image generation issue"""
        
    #     results = {}
        
    #     # Convert character info
    #     if isinstance(character_info, dict):
    #         character_specs = CharacterConsistencyManager.get_character_description_string(character_info)
    #     else:
    #         character_specs = str(character_info)
        
    #     print(f"\n=== COMPREHENSIVE DEBUG for user {user_id} ===")
    #     print(f"Scene: {scene_desc}")
    #     print(f"Character: {character_specs}")
        
    #     # Test 1: Arabic text processing
    #     results["arabic_test"] = await self.test_simple_arabic_processing(scene_desc)
        
    #     # Test 2: GPT-4 Vision call
    #     results["gpt4_vision"] = await self.debug_gpt4_vision_call(scene_desc, character_specs)
        
    #     # Test 3: Direct DALL-E with basic prompt
    #     basic_prompt = f"Child-friendly 2D cartoon illustration of a child wanting to eat food, no text"
    #     results["dalle_basic"] = await self.test_direct_dalle_call(basic_prompt)
        
    #     # Test 4: DALL-E with fallback prompt
    #     fallback_prompt = build_image_prompt(scene_desc, character_specs)
    #     results["dalle_fallback"] = await self.test_direct_dalle_call(fallback_prompt)
        
    #     # Test 5: DALL-E with English-only prompt
    #     english_prompt = "Child-friendly 2D cartoon of a happy child in kitchen wanting food, animated style, no text"
    #     results["dalle_english"] = await self.test_direct_dalle_call(english_prompt)
        
    #     print(f"\n=== DEBUG RESULTS SUMMARY ===")
    #     for test_name, result in results.items():
    #         status = "SUCCESS" if result.get("success") else "FAILED"
    #         print(f"{test_name}: {status}")
    #         if not result.get("success"):
    #             print(f"  Error: {result.get('error', 'Unknown')}")
        
    #     return results

    #  async def download_image_async(self, url: str, timeout: int = 30) -> str:
    #     """Async image download with proper error handling"""
    #     print(f"Downloading image from: {url}")
        
    #     try:
    #         # Try async download first
    #         async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
    #             async with session.get(url) as response:
    #                 if response.status == 200:
    #                     img_bytes = await response.read()
    #                     b64 = base64.b64encode(img_bytes).decode("utf-8")
    #                     print(f"Successfully downloaded image async, base64 length: {len(b64)}")
    #                     return b64
    #                 else:
    #                     print(f"HTTP error {response.status} during async download")
    #                     raise Exception(f"HTTP {response.status}")
                        
    #     except Exception as async_error:
    #         print(f"Async download failed: {async_error}")
            
    #         # Fallback to synchronous download
    #         try:
    #             print("Trying synchronous download...")
    #             response = requests.get(url, timeout=timeout)
    #             response.raise_for_status()
    #             img_bytes = response.content
    #             b64 = base64.b64encode(img_bytes).decode("utf-8")
    #             print(f"Successfully downloaded image sync, base64 length: {len(b64)}")
    #             return b64
                
    #         except Exception as sync_error:
    #             print(f"Sync download also failed: {sync_error}")
    #             raise Exception(f"Both download methods failed. Async: {async_error}, Sync: {sync_error}")

    async def comprehensive_debug(self, user_id: str, scene_desc: str, character_info: dict) -> Dict:
        """Test the new system"""
        print(f"\n=== TESTING NEW SYSTEM ===")
        
        # Test character consistency
        char1 = CharacterConsistencyManager.get_or_create_character(user_id, "LVL1")
        char2 = CharacterConsistencyManager.get_or_create_character(user_id, "LVL1")
        
        print(f"Character consistency test: {char1 == char2}")
        
        # Test translation
        translated = await self.scene_translator.translate_and_enhance_scene(scene_desc)
        print(f"Translation test: '{scene_desc}' -> '{translated}'")
        
        # Test full generation
        try:
            result = await self.generate_image(user_id, "LVL1", scene_desc, char1)
            return {"success": True, "character": char1, "translated_scene": translated}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def download_image_async(self, url: str, timeout: int = 30) -> str:
        """Async image download with proper error handling"""
        print(f"Downloading image from: {url}")
        
        try:
            # Try async download first
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        img_bytes = await response.read()
                        b64 = base64.b64encode(img_bytes).decode("utf-8")
                        print(f"Successfully downloaded image async, base64 length: {len(b64)}")
                        return b64
                    else:
                        print(f"HTTP error {response.status} during async download")
                        raise Exception(f"HTTP {response.status}")
                        
        except Exception as async_error:
            print(f"Async download failed: {async_error}")
            
            # Fallback to synchronous download
            try:
                print("Trying synchronous download...")
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                img_bytes = response.content
                b64 = base64.b64encode(img_bytes).decode("utf-8")
                print(f"Successfully downloaded image sync, base64 length: {len(b64)}")
                return b64
                
            except Exception as sync_error:
                print(f"Sync download also failed: {sync_error}")
                raise Exception(f"Both download methods failed. Async: {async_error}, Sync: {sync_error}")

    # Keep the original methods but add more logging
    # async def generate_image(self, user_id: str, autism_level: str, scene_desc: str, character_info: dict, 
    #                     previous_images: List[str] = None, n: int = 1, size: str = "1024x1024") -> str:

    #     """Generate image with comprehensive debugging - SIMPLIFIED"""
        
    #     print(f"\n=== IMAGE GENERATION START ===")
    #     print(f"User: {user_id}, Scene: {scene_desc}")
        
    #     # Skip the complex debug - just use what works
    #     try:
    #         # Use the working approach directly
    #         print("Using direct working approach...")
            
    #         prompt = scene_desc
            
    #         resp = await self.openai_client.images.generate(
    #             prompt=prompt,
    #             model="dall-e-3", 
    #             n=1,
    #             size=size,
    #             quality="standard"
    #         )
            
    #         url = resp.data[0].url
    #         print(f"DALL-E SUCCESS: {url}")
            
    #         # Download with better error handling
    #         b64_result = await self.download_image_async(url, timeout=120)  # 2 minute timeout
            
    #         print(f"DOWNLOAD SUCCESS: {len(b64_result)} characters")
    #         return b64_result
            
    #     except Exception as e:
    #         print(f"Image generation failed: {e}")
    #         raise Exception(f"Image generation failed: {str(e)}")
    async def generate_image(self, user_id: str, autism_level: str, scene_desc: str, character_info: dict = None, 
                        previous_images: List[str] = None, n: int = 1, size: str = "1024x1024") -> str:
        """Generate image with consistent character and proper scene handling"""
        
        print(f"\n=== IMAGE GENERATION START ===")
        print(f"User: {user_id}")
        print(f"Autism Level: {autism_level}")
        print(f"Scene Description: {scene_desc}")
        
        try:
            # Step 1: Get or create consistent character
            if character_info is None:
                character_info = CharacterConsistencyManager.get_or_create_character(user_id, autism_level)
            
            # Step 2: Translate and enhance scene description
            enhanced_scene = await self.scene_translator.translate_and_enhance_scene(scene_desc)
            print(f"Enhanced scene: {enhanced_scene}")
            
            # Step 3: Build prompt with character consistency
            prompt = build_image_prompt(scene_desc, character_info, enhanced_scene)
            
            # Step 4: Generate image
            print(f"Generating with DALL-E 3...")
            response = await self.openai_client.images.generate(
                prompt=prompt,
                model="dall-e-3",
                n=1,
                size=size,
                quality="standard"
            )
            
            url = response.data[0].url
            print(f"DALL-E SUCCESS: {url}")
            
            # Step 5: Download image
            b64_result = await self.download_image_async(url, timeout=120)
            
            # Step 6: Update character usage count
            CharacterConsistencyManager.increment_image_count(user_id, autism_level)
            
            print(f"GENERATION COMPLETE: {len(b64_result)} characters")
            return b64_result
            
        except Exception as e:
            print(f"Image generation failed: {e}")
            
            # Fallback to simple English prompt
            try:
                print("Attempting fallback generation...")
                fallback_prompt = f"2D cartoon child-friendly illustration: {CharacterConsistencyManager.get_character_description_string(character_info)} in a happy scene, no text"
                
                response = await self.openai_client.images.generate(
                    prompt=fallback_prompt,
                    model="dall-e-3",
                    n=1,
                    size=size,
                    quality="standard"
                )
                
                url = response.data[0].url
                b64_result = await self.download_image_async(url, timeout=60)
                return b64_result
                
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
                raise Exception(f"Image generation failed: {str(e)}")

    async def _generate_with_english_prompt(self, scene_desc: str, character_info: dict, size: str) -> str:
        """Generate using English-only prompt with better error handling"""
        
        print("=== _generate_with_english_prompt START ===")
        
        prompt = "Child-friendly 2D cartoon of a happy child in kitchen cooking pasta, animated style, thick outlines, pastel colors, no text or writing"
        
        print(f"Using prompt: {prompt}")
        
        try:
            # Step 1: Generate image
            print("Step 1: Calling DALL-E API...")
            resp = await self.openai_client.images.generate(
                prompt=prompt,
                model="dall-e-3",
                n=1,
                size=size,
                quality="standard"
            )
            
            url = resp.data[0].url
            print(f"Step 1 SUCCESS: Got URL: {url}")
            
            # Step 2: Download image with better error handling
            print("Step 2: Downloading image...")
            b64_result = await self.download_image_async(url, timeout=60)  # Increased timeout
            
            print(f"Step 2 SUCCESS: Image downloaded, length: {len(b64_result)}")
            return b64_result
            
        except Exception as e:
            print(f"ERROR in _generate_with_english_prompt: {str(e)}")
            print(f"Error type: {type(e)}")
            raise

    async def _generate_with_basic_prompt(self, scene_desc: str, character_info: dict, size: str) -> str:
        """Generate using basic prompt without GPT-4 processing"""
        prompt = f"Child-friendly 2D cartoon illustration of a child wanting to eat food, no text"
        
        resp = await self.openai_client.images.generate(
            prompt=prompt,
            model="dall-e-3", 
            n=1,
            size=size,
            quality="standard"
        )
        
        url = resp.data[0].url
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        return base64.b64encode(r.content).decode("utf-8")

    async def _generate_with_fallback(self, scene_desc: str, character_info: dict, size: str) -> str:
        """Generate using fallback method"""
        if isinstance(character_info, dict):
            character_specs = CharacterConsistencyManager.get_character_description_string(character_info)
        else:
            character_specs = str(character_info)
            
        prompt = build_image_prompt(scene_desc, character_specs)
        
        resp = await self.openai_client.images.generate(
            prompt=prompt,
            model="dall-e-3",
            n=1, 
            size=size,
            quality="standard"
        )
        
        url = resp.data[0].url
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        return base64.b64encode(r.content).decode("utf-8")