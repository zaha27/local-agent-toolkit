# llm/client.py
import asyncio
import json
import httpx
from dataclasses import dataclass, field
from typing import AsyncIterator, Optional

@dataclass
class OllamaConfig:
    base_url: str = "http://localhost:11434"
    model: str = "llama3.1:8b"
    temperature: float = 0.7
    keep_alive: str = "30m"
    num_ctx: int = 8192
    num_gpu: int = 99

class OllamaClient:
    def __init__(self, config: OllamaConfig = OllamaConfig()):
        self.config = config
        self._client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=httpx.Timeout(120.0, connect=5.0),
            limits=httpx.Limits(max_keepalive_connections=5)
        )

    async def chat_stream(
        self,
        messages: list[dict],
        tools: Optional[list[dict]] = None
    ) -> AsyncIterator[str]:
        payload = {
            "model": self.config.model,
            "messages": messages,
            "stream": True,
            "keep_alive": self.config.keep_alive,
            "options": {
                "temperature": self.config.temperature,
                "num_ctx": self.config.num_ctx,
                "num_gpu": self.config.num_gpu,
            }
        }
        if tools:
            payload["tools"] = tools

        async with self._client.stream("POST", "/api/chat", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                if chunk.get("done"):
                    break
                content = chunk.get("message", {}).get("content", "")
                if content:
                    yield content

    async def chat(self, messages: list[dict], tools: Optional[list[dict]] = None) -> dict:
        payload = {
            "model": self.config.model,
            "messages": messages,
            "stream": False,
            "keep_alive": self.config.keep_alive,
            "options": {
                "num_ctx": self.config.num_ctx,
                "num_gpu": self.config.num_gpu,
            }
        }
        if tools:
            payload["tools"] = tools

        resp = await self._client.post("/api/chat", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self._client.aclose()