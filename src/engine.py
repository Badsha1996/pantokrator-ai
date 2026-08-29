from __future__ import annotations

import asyncio
import re
from collections.abc import AsyncIterator
from typing import Protocol, runtime_checkable

GREETINGS = {"hi", "hey", "hello", "yo", "pantokrator", "sup"}


@runtime_checkable
class Engine(Protocol):
    name: str
    def stream(self, prompt: str) -> AsyncIterator[str]: ...


class EchoEngine:
    name = "echo"
    def __init__(self, delay: float = 0.014) -> None: self.delay = delay

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        for fragment in _fragments(_reply_to(prompt)):
            await asyncio.sleep(self.delay)
            yield fragment


def _reply_to(prompt: str) -> str:
    words = re.findall(r"[a-z']+", prompt.lower())

    if words and words[0] in GREETINGS and len(words) <= 3: return "Hello sir."

    return f'Heard you: *"{prompt.strip()}"*\n\n'


def _fragments(text: str) -> list[str]: return re.findall(r"\S+\s*", text) or [text]
