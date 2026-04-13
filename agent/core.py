# agent/core.py
import json
from llm.client import OllamaClient, OllamaConfig
from agent.context import ContextManager, MsgPriority
from tools.registry import registry

SYSTEM_PROMPT = """You are a local AI agent running on Arch Linux.
You have access to tools to interact with the system.
Think step by step before executing commands.
If unsure, ask for clarification. Prioritize safety."""

class LocalAgent:
    def __init__(self, config: OllamaConfig = None):
        self.llm = OllamaClient(config or OllamaConfig())
        self.ctx = ContextManager(max_tokens=7000)
        self.tools = registry.to_ollama_tools()
        self.max_tool_iterations = 5

        self.ctx.add("system", SYSTEM_PROMPT, MsgPriority.SYSTEM)

    async def run(self, user_input: str) -> str:
        self.ctx.add("user", user_input)
        iterations = 0

        while iterations < self.max_tool_iterations:
            iterations += 1
            response = await self.llm.chat(
                messages=self.ctx.to_ollama_format(),
                tools=self.tools
            )

            message = response.get("message", {})
            tool_calls = message.get("tool_calls", [])

            if not tool_calls:
                final = message.get("content", "")
                self.ctx.add("assistant", final, MsgPriority.ASSISTANT)
                return final

            self.ctx.add("assistant", json.dumps(tool_calls), MsgPriority.ASSISTANT)

            for tc in tool_calls:
                fn = tc.get("function", {})
                tool_name = fn.get("name")
                tool_args = fn.get("arguments", {})

                print(f"[TOOL] {tool_name}({tool_args})")
                result = await registry.dispatch(tool_name, tool_args)
                print(f"[RESULT] {result[:200]}")

                self.ctx.add("tool", str(result), MsgPriority.TOOL_RESULT)

        return "Max iterations reached."

    async def close(self):
        await self.llm.close()