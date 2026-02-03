import asyncio
from app.agents.analyzer import AnalyzerAgent

async def main():
    print("🚀 Analyzer Agent started...")
    agent = AnalyzerAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
