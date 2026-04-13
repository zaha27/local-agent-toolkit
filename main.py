# main.py
import asyncio
from agent.core import LocalAgent
from llm.client import OllamaConfig

async def main():
    config = OllamaConfig(
        model="llama3.1:8b",
        temperature=0.3,
        num_ctx=8192,
        keep_alive="30m"
    )

    agent = LocalAgent(config)
    print("sudo. ctrl+c for exit...\n")

    try:
        while True:
            user_input = input("Tu: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                break

            response = await agent.run(user_input)
            print(f"\nAgent: {response}\n")
    except KeyboardInterrupt:
        print("\nLa revedere!")
    finally:
        await agent.close()

if __name__ == "__main__":
    asyncio.run(main()) 