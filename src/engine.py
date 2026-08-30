from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Protocol, runtime_checkable

from .helpers.engine import _fragments, _reply_to

# Interfaces which should have the original shape
# btw i was thinking of separting this as we can have interfaces/
# BUT THIS IS A NOTE FOR Future Badsha 
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
