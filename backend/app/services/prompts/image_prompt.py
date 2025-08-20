
from typing import Optional, List, Tuple, Dict

# Much stronger cartoon/animation instructions
# DALLE_INSTRUCTIONS = """
# 🚫 ABSOLUTELY NO TEXT, LETTERS, WORDS, NUMBERS, OR WRITING anywhere in the image 🚫

# MANDATORY STYLE: 2D CARTOON ANIMATION ONLY - NOT REALISTIC
# - Flat cartoon children's book illustration style
# - Animated/cartoon characters ONLY (like Disney/Pixar style)
# - Thick black outlines around all elements
# - Solid pastel colors with flat fills (no realistic shading)
# - Simple vector-like illustration with soft rounded shapes
# - Child-friendly animated art style
# - Minimal clean background
# - NO photorealistic elements
# - NO realistic human features
# - Think: children's animated TV show or picture book illustration

# 🚫 FORBIDDEN: Any written text, signs, labels, books with text, typography, realistic photos, realistic people
# ✅ REQUIRED: Pure 2D cartoon animation style, visual storytelling through expressions and poses only

# Character consistency: If this is a follow-up image, maintain the exact same ANIMATED character appearance as previous images.
# """

# def build_image_prompt(description: str, character_info: dict = None) -> str:
#     """Enhanced version with strong cartoon/animation enforcement"""
#     desc = description.strip().capitalize()
    
#     # Remove text-inducing words
#     desc = desc.replace("reading", "looking at pictures in")
#     desc = desc.replace("book", "picture book with blank pages")
#     desc = desc.replace("sign", "simple symbol")
#     desc = desc.replace("text", "image")
#     desc = desc.replace("realistic", "cartoon")
#     desc = desc.replace("photo", "illustration")
    
#     # Force cartoon style in description
#     if "cartoon" not in desc.lower() and "animated" not in desc.lower():
#         desc = f"Cartoon animated {desc.lower()}"
    
#     # Add character consistency if provided
#     character_desc = ""
#     if character_info:
#         # Make sure character description emphasizes cartoon style
#         char_base = character_info.get('description', 'friendly animated character')
#         if "cartoon" not in char_base.lower() and "animated" not in char_base.lower():
#             char_base = f"cartoon animated {char_base}"
            
#         character_desc = f"\nCharacter: {char_base}"
#         if character_info.get('is_returning', False):
#             features = character_info.get('features', 'same animated style')
#             character_desc += f" (same cartoon appearance as previous: {features})"
    
#     # Build final prompt with multiple cartoon reinforcements
#     full_prompt = f"""2D CARTOON ANIMATION STYLE ONLY:
#         Scene: {desc}{character_desc} {DALLE_INSTRUCTIONS}"""
    
#     return full_prompt[:1000]




# from typing import Optional, List, Tuple, Dict

# # Ultra-strong character consistency instructions
# DALLE_INSTRUCTIONS = """
# 🚫 ABSOLUTELY NO TEXT, LETTERS, WORDS, NUMBERS, OR WRITING anywhere in the image 🚫

# MANDATORY: 2D CARTOON ANIMATION STYLE ONLY 
# - Flat cartoon children's book illustration
# - Thick black outlines, solid pastel colors
# - Simple vector-like illustration, soft rounded shapes
# - Child-friendly animated art style (like PBS Kids or Disney Junior)
# - NO realistic people or photography

# CRITICAL CHARACTER CONSISTENCY:
# - If character details are specified, follow them EXACTLY
# - Same hair color, hair style, clothing, facial features, body proportions
# - DO NOT change character appearance between images
# - Maintain identical visual characteristics throughout session

# 🚫 NO TEXT/WORDS/LETTERS in image ✅ ONLY cartoon animation style
# """

# def build_image_prompt(desc: str, character_info: str) -> str:
#     """Ultra-strong character consistency enforcement with persistent character details"""
#     # desc = description.strip().capitalize()

#     # # Clean up text-inducing words
#     # desc = desc.replace("reading", "looking at pictures in")
#     # desc = desc.replace("book", "picture book with blank pages")
#     # desc = desc.replace("sign", "simple symbol")
#     # desc = desc.replace("text", "image")

#     # Force cartoon style wording
#     if "cartoon" not in desc.lower() and "animated" not in desc.lower():
#         desc = f"2D cartoon animated scene: {desc.lower()}"

#     # Get clean character description string
#     # char_desc = CharacterConsistencyManager.get_character_description_string(character_info)

#     # Build final prompt
#     full_prompt = f"""
#     {DALLE_INSTRUCTIONS}

#     EXACT CHARACTER (must match previous images exactly):
#     {character_info}

#     SCENE:
#     {desc}

#     REMINDER: This is the SAME character from previous images. Keep the SAME hair, clothing, facial features, skin tone, and proportions. 
#     DO NOT change appearance between images.
#     """

#     return full_prompt.strip()[:1000]

# # Enhanced character management system
# class CharacterConsistencyManager:
#     """Manages detailed character profiles for ultra-consistency"""

#     @staticmethod
#     def create_detailed_character(user_id: str, autism_level: str) -> dict:
#         """Create detailed character profile based on autism level"""
#         if autism_level == "LVL1":
#             return {
#                 'name': 'main_character',
#                 'hair_color': 'dark brown',
#                 'hair_style': 'short neat',
#                 'clothing': 'bright blue t-shirt and dark blue pants',
#                 'age_group': 'child around 8 years old',
#                 'skin_tone': 'medium',
#                 'gender': 'Female',
#                 'facial_features': 'round friendly face, big expressive eyes, gentle smile',
#                 'body_type': 'normal child proportions',
#                 'is_returning': False,
#                 'image_count': 0
#             }
#         elif autism_level == "LVL2":
#             return {
#                 'name': 'main_character',
#                 'hair_color': 'light brown',
#                 'hair_style': 'medium length wavy',
#                 'clothing': 'soft green sweater and comfortable brown pants',
#                 'age_group': 'child around 7 years old',
#                 'skin_tone': 'light',
#                 'gender': 'Female',
#                 'facial_features': 'gentle round face, kind eyes, calm expression',
#                 'body_type': 'slight child proportions',
#                 'is_returning': False,
#                 'image_count': 0
#             }
#         else:  # LVL3
#             return {
#                 'name': 'main_character',
#                 'hair_color': 'blonde',
#                 'hair_style': 'short straight',
#                 'clothing': 'simple white shirt and blue jeans',
#                 'age_group': 'child around 6 years old',
#                 'skin_tone': 'fair',
#                 'gender': 'Female',
#                 'facial_features': 'soft features, peaceful expression, gentle eyes',
#                 'body_type': 'small child proportions',
#                 'is_returning': False,
#                 'image_count': 0
#             }

#     @staticmethod
#     def get_character_description_string(char_info: dict) -> str:
#         """Convert character dict to detailed description string"""
#         return (
#             f"A {char_info['gender']} {char_info['age_group']} with {char_info['hair_color']} {char_info['hair_style']} hair, "
#             f"wearing {char_info['clothing']}, {char_info['facial_features']}, "
#             f"{char_info['skin_tone']} skin, {char_info['body_type']}"
#         )





from typing import Optional, List, Tuple, Dict, Union

# Ultra-strong character consistency instructions
DALLE_INSTRUCTIONS = """
🚫 ABSOLUTELY NO TEXT, LETTERS, WORDS, NUMBERS, OR WRITING anywhere in the image 🚫

MANDATORY: 2D CARTOON ANIMATION STYLE ONLY 
- Flat cartoon children's book illustration
- Thick black outlines, solid pastel colors
- Simple vector-like illustration, soft rounded shapes
- Child-friendly animated art style (like PBS Kids or Disney Junior)
- NO realistic people or photography

CRITICAL CHARACTER CONSISTENCY:
- Follow character details EXACTLY as specified
- Same hair color, hair style, clothing, facial features, body proportions
- DO NOT change character appearance between images
- Maintain identical visual characteristics throughout session
- This character appears in multiple images - keep them looking identical

🚫 NO TEXT/WORDS/LETTERS in image ✅ ONLY cartoon animation style
"""

# def build_image_prompt(desc: str, character_info: Union[str, dict]) -> str:
#     """Ultra-strong character consistency enforcement with persistent character details"""
    
#     print(f"build_image_prompt called with:")
#     print(f"  desc: {desc}")
#     print(f"  character_info type: {type(character_info)}")
#     print(f"  character_info: {character_info}")
    
#     # Clean up scene description
#     desc = desc.strip()
    
#     # Clean up text-inducing words
#     desc = desc.replace("reading", "looking at pictures in")
#     desc = desc.replace("book", "picture book with blank pages")
#     desc = desc.replace("sign", "simple symbol")
#     desc = desc.replace("text", "image")
#     desc = desc.replace("letter", "picture")
#     desc = desc.replace("word", "image")

#     # Force cartoon style wording
#     if "cartoon" not in desc.lower() and "animated" not in desc.lower():
#         desc = f"2D cartoon animated scene: {desc.lower()}"

#     # Handle character_info properly - it should be a string at this point
#     if isinstance(character_info, dict):
#         # If somehow we get a dict, convert it
#         char_desc = CharacterConsistencyManager.get_character_description_string(character_info)
#         consistency_note = ""
#         if character_info.get('is_returning', False):
#             consistency_note = f"\n⚠️ SAME CHARACTER AS PREVIOUS {character_info.get('image_count', 1)} IMAGES - DO NOT CHANGE APPEARANCE ⚠️"
#     elif isinstance(character_info, str):
#         # This is what we expect - a string description
#         char_desc = character_info
#         consistency_note = "\n⚠️ MAINTAIN SAME CHARACTER APPEARANCE AS PREVIOUS IMAGES ⚠️"
#     else:
#         print(f"ERROR: Unexpected character_info type in build_image_prompt: {type(character_info)}")
#         char_desc = "friendly animated child character"
#         consistency_note = ""

#     # Build final prompt with maximum consistency emphasis
#     full_prompt = f"""
# {DALLE_INSTRUCTIONS}

# EXACT CHARACTER (must match previous images exactly):
# {char_desc}
# {consistency_note}

# SCENE: {desc}

# CRITICAL: This is the SAME character from previous images. Keep the EXACT SAME hair color, hair style, clothing, facial features, skin tone, body proportions, and overall appearance. DO NOT change anything about the character's visual design.
# """

#     final_prompt = full_prompt.strip()[:1000]  # Increased limit for more detail
#     print(f"Final prompt length: {len(final_prompt)}")
#     return final_prompt

# class CharacterConsistencyManager:
#     """Manages detailed character profiles for ultra-consistency"""

#     @staticmethod
#     def create_detailed_character(user_id: str, autism_level: str) -> dict:
#         """Create detailed character profile based on autism level"""
#         base_profiles = {
#             "LVL1": {
#                 'name': 'main_character',
#                 'hair_color': 'dark brown',
#                 'hair_style': 'short neat bob cut',
#                 'clothing': 'bright blue t-shirt with small star design and dark blue pants',
#                 'age_group': 'child around 8 years old',
#                 'skin_tone': 'medium tan',
#                 'gender': 'girl',
#                 'facial_features': 'round friendly face with big brown eyes, small nose, gentle smile with dimples',
#                 'body_type': 'normal child proportions, medium height',
#                 'accessories': 'small red backpack',
#                 'is_returning': False,
#                 'image_count': 0
#             },
#             "LVL2": {
#                 'name': 'main_character',
#                 'hair_color': 'light brown',
#                 'hair_style': 'medium length wavy hair with side part',
#                 'clothing': 'soft green long-sleeve sweater and comfortable brown corduroy pants',
#                 'age_group': 'child around 7 years old',
#                 'skin_tone': 'light olive',
#                 'gender': 'girl',
#                 'facial_features': 'gentle oval face with hazel eyes, button nose, calm peaceful expression',
#                 'body_type': 'slight child proportions, average height',
#                 'accessories': 'small purple bracelet',
#                 'is_returning': False,
#                 'image_count': 0
#             },
#             "LVL3": {
#                 'name': 'main_character',
#                 'hair_color': 'blonde',
#                 'hair_style': 'short straight hair with bangs',
#                 'clothing': 'simple white cotton shirt and blue denim jeans',
#                 'age_group': 'child around 6 years old',
#                 'skin_tone': 'fair',
#                 'gender': 'girl',
#                 'facial_features': 'soft round face with blue eyes, small features, serene gentle expression',
#                 'body_type': 'petite child proportions, shorter height',
#                 'accessories': 'simple white sneakers',
#                 'is_returning': False,
#                 'image_count': 0
#             }
#         }
        
#         profile = base_profiles.get(autism_level, base_profiles["LVL1"]).copy()
#         print(f"Created character profile for {autism_level}: {profile}")
#         return profile

#     @staticmethod
#     def get_character_description_string(char_info: dict) -> str:
#         """Convert character dict to ultra-detailed description string"""
#         if not isinstance(char_info, dict):
#             print(f"ERROR in get_character_description_string: Expected dict, got {type(char_info)}: {char_info}")
#             return "friendly animated child character"
            
#         try:
#             description = (
#                 f"A {char_info.get('gender', 'child')} {char_info.get('age_group', 'young child')} with "
#                 f"{char_info.get('hair_color', 'brown')} {char_info.get('hair_style', 'neat hair')}, "
#                 f"wearing {char_info.get('clothing', 'colorful clothes')}, "
#                 f"{char_info.get('facial_features', 'friendly face')}, "
#                 f"{char_info.get('skin_tone', 'medium')} skin, "
#                 f"{char_info.get('body_type', 'normal child proportions')}, "
#                 f"with {char_info.get('accessories', 'no accessories')}"
#             )
#             print(f"Generated character description: {description}")
#             return description
#         except Exception as e:
#             print(f"ERROR generating character description: {e}")
#             print(f"char_info contents: {char_info}")
#             return "friendly animated child character"



from typing import Optional, List, Tuple, Dict, Union

# def build_image_prompt(desc: str, character_info: Union[str, dict]) -> str:
#     """Simplified, working image prompt builder"""
    
#     print(f"build_image_prompt called with:")
#     print(f"  desc: {desc}")
#     print(f"  character_info type: {type(character_info)}")
    
#     # Clean up scene description - remove Arabic text and emojis
#     desc = desc.strip()
#     # Remove emojis and Arabic text that might cause issues
#     desc = desc.replace("🌟", "").replace("طهي وجبة خفيفة أو رئيسية؟", "cooking food")
#     desc = desc.replace("بدي اكل", "wanting to eat")
    
#     # If description is empty or still has Arabic, use English fallback
#     if not desc or any(ord(c) > 127 for c in desc):
#         desc = "child cooking or eating food"
    
#     # Clean up text-inducing words
#     desc = desc.replace("reading", "looking at pictures")
#     desc = desc.replace("book", "picture book")
#     desc = desc.replace("sign", "picture")
#     desc = desc.replace("text", "image")
#     desc = desc.replace("letter", "drawing")
#     desc = desc.replace("word", "picture")

#     # Handle character_info properly
#     if isinstance(character_info, dict):
#         char_desc = CharacterConsistencyManager.get_character_description_string(character_info)
#     elif isinstance(character_info, str):
#         char_desc = character_info
#     else:
#         print(f"ERROR: Unexpected character_info type: {type(character_info)}")
#         char_desc = "friendly child character"

#     # Create a simple, clean prompt - NO emojis, NO complex formatting
#     prompt = f"2D cartoon animated children's book illustration: {char_desc} {desc}. Flat cartoon style with thick black outlines, pastel colors, child-friendly, no text or writing anywhere in the image."
    
#     # Ensure reasonable length (DALL-E 3 works better with shorter prompts)
#     if len(prompt) > 400:
#         # Shorten the character description if needed
#         char_desc = char_desc[:150] + "..." if len(char_desc) > 150 else char_desc
#         prompt = f"2D cartoon illustration: {char_desc} {desc}. Child-friendly style, no text."
    
#     final_prompt = prompt.strip()
#     print(f"Final prompt length: {len(final_prompt)}")
#     print(f"Final prompt: {final_prompt}")
#     return final_prompt

# class CharacterConsistencyManager:
#     """Simplified character manager"""

#     @staticmethod
#     def create_detailed_character(user_id: str, autism_level: str) -> dict:
#         """Create simplified character profile"""
#         base_profiles = {
#             "LVL1": {
#                 'name': 'main_character',
#                 'description': 'A friendly 8-year-old girl with dark brown bob haircut, wearing a bright blue t-shirt and dark blue pants',
#                 'is_returning': False,
#                 'image_count': 0
#             },
#             "LVL2": {
#                 'name': 'main_character', 
#                 'description': 'A gentle 7-year-old girl with light brown wavy hair, wearing a soft green sweater and brown pants',
#                 'is_returning': False,
#                 'image_count': 0
#             },
#             "LVL3": {
#                 'name': 'main_character',
#                 'description': 'A calm 6-year-old girl with blonde hair and bangs, wearing a white shirt and blue jeans',
#                 'is_returning': False,
#                 'image_count': 0
#             }
#         }
        
#         profile = base_profiles.get(autism_level, base_profiles["LVL1"]).copy()
#         print(f"Created character profile for {autism_level}: {profile}")
#         return profile

#     @staticmethod
#     def get_character_description_string(char_info: dict) -> str:
#         """Convert character dict to simple description string"""
#         if not isinstance(char_info, dict):
#             print(f"ERROR: Expected dict, got {type(char_info)}")
#             return "friendly child character"
            
#         try:
#             # Use simplified description if available, otherwise build one
#             if 'description' in char_info:
#                 return char_info['description']
            
#             # Fallback to building description from components
#             description = f"A friendly child character with {char_info.get('hair_color', 'brown')} hair, wearing {char_info.get('clothing', 'casual clothes')}"
#             print(f"Generated character description: {description}")
#             return description
#         except Exception as e:
#             print(f"ERROR generating character description: {e}")
#             return "friendly child character"

from openai import AsyncOpenAI
import hashlib
class CharacterConsistencyManager:
    """Improved character manager with persistence"""
    
    # Store character profiles in memory (in production, use database)
    _character_cache = {}
    
    @staticmethod
    def get_or_create_character(user_id: str, autism_level: str) -> dict:
        """Get existing character or create new one"""
        cache_key = f"{user_id}_{autism_level}"
        
        if cache_key in CharacterConsistencyManager._character_cache:
            char = CharacterConsistencyManager._character_cache[cache_key]
            print(f"Using existing character for {user_id}: {char['name']}")
            return char
        
        # Create new character
        char = CharacterConsistencyManager._create_detailed_character(user_id, autism_level)
        CharacterConsistencyManager._character_cache[cache_key] = char
        print(f"Created new character for {user_id}: {char['name']}")
        return char
    
    @staticmethod
    def _create_detailed_character(user_id: str, autism_level: str) -> dict:
        """Create detailed, consistent character profile"""
        
        # Use user_id to generate consistent features
        seed = int(hashlib.md5(user_id.encode()).hexdigest()[:8], 16)
        
        # Hair options
        hair_colors = ["dark brown", "light brown", "blonde", "black", "auburn"]
        hair_styles = ["short bob", "shoulder-length wavy", "curly", "straight with bangs", "pigtails"]
        
        # Clothing options
        shirt_colors = ["bright blue", "soft green", "cheerful yellow", "warm pink", "light purple"]
        bottom_colors = ["dark blue jeans", "brown pants", "black leggings", "denim shorts", "gray pants"]
        
        # Generate consistent features based on user_id
        hair_color = hair_colors[seed % len(hair_colors)]
        hair_style = hair_styles[(seed // 5) % len(hair_styles)]
        shirt_color = shirt_colors[(seed // 25) % len(shirt_colors)]
        bottom_color = bottom_colors[(seed // 125) % len(bottom_colors)]
        
        # Age varies slightly by autism level for appropriateness
        ages = {"LVL1": 8, "LVL2": 7, "LVL3": 6}
        age = ages.get(autism_level, 7)
        
        character = {
            'name': f'character_{user_id}',
            'age': age,
            'hair_color': hair_color,
            'hair_style': hair_style,
            'shirt_color': shirt_color,
            'bottom_color': bottom_color,
            'description': f"A friendly {age}-year-old child with {hair_color} {hair_style} hair, wearing a {shirt_color} shirt and {bottom_color}",
            'autism_level': autism_level,
            'image_count': 0,
            'created_for_user': user_id
        }
        
        return character
    
    @staticmethod
    def get_character_description_string(char_info: dict) -> str:
        """Convert character dict to detailed description string"""
        if not isinstance(char_info, dict):
            return "a friendly child character"
        
        try:
            if 'description' in char_info:
                return char_info['description']
            
            # Build from components
            age = char_info.get('age', 7)
            hair = f"{char_info.get('hair_color', 'brown')} {char_info.get('hair_style', 'hair')}"
            clothing = f"{char_info.get('shirt_color', 'blue')} shirt and {char_info.get('bottom_color', 'pants')}"
            
            return f"A friendly {age}-year-old child with {hair}, wearing a {clothing}"
        
        except Exception as e:
            print(f"Error generating character description: {e}")
            return "a friendly child character"
    
    @staticmethod
    def increment_image_count(user_id: str, autism_level: str):
        """Track how many images generated for consistency"""
        cache_key = f"{user_id}_{autism_level}"
        if cache_key in CharacterConsistencyManager._character_cache:
            CharacterConsistencyManager._character_cache[cache_key]['image_count'] += 1


class SceneTranslator:
    """Handle Arabic text translation and scene understanding"""
    
    def __init__(self, openai_client: AsyncOpenAI):
        self.openai_client = openai_client
    
    async def translate_and_enhance_scene(self, scene_desc: str) -> str:
        """Translate Arabic and enhance scene description for image generation"""
        
        if not scene_desc or scene_desc.strip() == "":
            return "child in a happy scene"
        
        # Check if contains Arabic text
        has_arabic = any(ord(char) > 127 for char in scene_desc)
        
        if not has_arabic:
            return scene_desc.strip()
        
        try:
            print(f"Translating scene: {scene_desc}")
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a translator specializing in children's content. Translate Arabic text to English and enhance it for image generation. Keep it child-friendly and descriptive but concise."
                },
                {
                    "role": "user",
                    "content": f"Translate this to English and make it suitable for generating a children's book illustration: {scene_desc}"
                }
            ]
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=150,
                temperature=0.3
            )
            
            translated = response.choices[0].message.content.strip()
            print(f"Translated scene: {translated}")
            return translated
            
        except Exception as e:
            print(f"Translation failed: {e}")
            # Fallback translations for common Arabic phrases
            fallbacks = {
                "بدي اكل": "wanting to eat food",
                "طبخ": "cooking",
                "طعام": "food",
                "تفاحة": "apple",
                "موز": "banana",
                "خضار": "vegetables"
            }
            
            for arabic, english in fallbacks.items():
                if arabic in scene_desc:
                    return english
            
            return "child in a happy scene"


def build_image_prompt(scene_desc: str, character_info: dict, enhanced_scene: str = None) -> str:
    """Build comprehensive image prompt with character consistency"""
    
    print(f"Building prompt for scene: {scene_desc}")
    
    # Use enhanced scene if provided, otherwise use original
    scene_to_use = enhanced_scene or scene_desc
    
    # Get character description
    char_desc = CharacterConsistencyManager.get_character_description_string(character_info)
    
    # Clean problematic words that might trigger text generation
    scene_clean = scene_to_use.lower()
    text_triggers = ["reading", "book", "sign", "text", "letter", "word", "writing", "newspaper"]
    for trigger in text_triggers:
        scene_clean = scene_clean.replace(trigger, "picture")
    
    # Build the prompt with specific style instructions
    prompt_parts = [
        "2D cartoon children's book illustration:",
        char_desc,
        scene_clean,
        "Digital art style with thick black outlines,",
        "bright cheerful colors,",
        "simple clean background,", 
        "child-friendly,",
        "no text, no writing, no letters, no words anywhere in the image"
    ]
    
    final_prompt = " ".join(prompt_parts)
    
    # Ensure reasonable length for DALL-E 3
    if len(final_prompt) > 400:
        # Simplify if too long
        final_prompt = f"2D cartoon illustration: {char_desc} {scene_clean}. Child-friendly style, thick outlines, no text."
    
    print(f"Final prompt ({len(final_prompt)} chars): {final_prompt}")
    return final_prompt