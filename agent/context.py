# agent/context.py
from dataclasses import dataclass, field
from enum import Enum

class MsgPriority(Enum):
    SYSTEM = 0      
    TOOL_RESULT = 1 
    ASSISTANT = 2
    USER = 3        

@dataclass
class Message:
    role: str
    content: str
    priority: MsgPriority = MsgPriority.USER
    token_estimate: int = 0

    def __post_init__(self):
        self.token_estimate = len(self.content) // 4

class ContextManager:
    def __init__(self, max_tokens: int = 7000, reserve_tokens: int = 1000):
        self.max_tokens = max_tokens
        self.reserve = reserve_tokens
        self._messages: list[Message] = []

    def add(self, role: str, content: str, priority: MsgPriority = MsgPriority.USER):
        self._messages.append(Message(role, content, priority))
        self._trim_if_needed()

    def _trim_if_needed(self):
        budget = self.max_tokens - self.reserve

        while self._total_tokens() > budget:
            candidates = [
                (i, m) for i, m in enumerate(self._messages)
                if m.priority != MsgPriority.SYSTEM
            ]
            if not candidates:
                break
            idx = max(candidates, key=lambda x: x[1].priority.value)[0]
            self._messages.pop(idx)

    def _total_tokens(self) -> int:
        return sum(m.token_estimate for m in self._messages)

    def to_ollama_format(self) -> list[dict]:
        return [{"role": m.role, "content": m.content} for m in self._messages]