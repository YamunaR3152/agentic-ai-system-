import asyncio
from app.agents.retriever import RetrieverAgent
from app.agents.analyzer import AnalyzerAgent

async def main():
    task = {
        "user_query": "What is agentic AI?"
    }

    retriever = RetrieverAgent()
    analyzer = AnalyzerAgent()

    task = await retriever.run(task)
    task = await analyzer.run(task)

    print("\n✅ FINAL TASK OUTPUT:")
    print(task)

if __name__ == "__main__":
    asyncio.run(main())
