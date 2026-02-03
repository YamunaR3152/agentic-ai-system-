import asyncio
from app.agents.retriever import RetrieverAgent

async def main():
    print("🚀 Retriever Agent started...")
    agent = RetrieverAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
