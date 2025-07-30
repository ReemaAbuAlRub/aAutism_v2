from typing import List, Dict, Optional

SYSTEM_PROMPT = (
    "You are a friendly, clear, and concise assistant tailored for autistic users"
    "Provide straightforward, concrete answers with optional visual supports when helpful."
)

def build_messages(user: str, history: Optional[List[Dict]] = None) -> List[Dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user})

    return messages