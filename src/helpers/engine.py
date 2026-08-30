import random
import re

GREETINGS = {"hi", "hey", "hello", "yo", "pantokrator", "sup"}
REPLY = ["Hello sir.", "Welcome back Sir.", "How are you sir?"]

def _reply_to(prompt: str) -> str:
    words = re.findall(r"[a-z']+", prompt.lower())

    if words and words[0] in GREETINGS and len(words) <= 3: return REPLY[random.randint(0, len(REPLY) - 1)]

    return f'Heard you: *"{prompt.strip()}"*\n\n'


def _fragments(text: str) -> list[str]: return re.findall(r"\S+\s*", text) or [text]
