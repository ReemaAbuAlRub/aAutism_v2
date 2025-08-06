from typing import Optional


DALLE_INSTRUCTIONS = """
Cartoon style: flat, children’s book style vector illustration:  black outlines, solid pastel fills, minimal background
"""
def build_image_prompt(description: str) -> str:
    desc = description.strip().capitalize()
    # Merge and truncate
    full = f"Scene description: {description}\n\n{DALLE_INSTRUCTIONS}"
    return full[:1000]