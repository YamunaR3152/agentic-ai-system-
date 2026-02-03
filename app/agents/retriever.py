import asyncio
import re
from app.preprocessing.text_loader import load_texts
from app.preprocessing.wiki_loader import fetch_wikipedia
from app.core.task_queue import (
    TASK_QUEUE,
    RETRIEVER_QUEUE,
    STATUS_QUEUE,
    pop_task,
    push_task
)

# 🔹 Smart cleaning for Wikipedia titles
def clean_query(q: str) -> str:
    q_lower = q.lower().strip()

    # 🔥 Handle special AI question patterns FIRST
    if "types of ai" in q_lower or "types of artificial intelligence" in q_lower:
        return "Types of artificial intelligence"

    if q_lower in ["ai", "artificial intelligence"]:
        return "Artificial intelligence"

    # Remove common question phrases
    q_lower = re.sub(r"what is|what are|define|explain|tell me about", "", q_lower)

    # Remove extra spaces
    q_lower = re.sub(r"\s+", " ", q_lower).strip()

    return q_lower.title()


class RetrieverAgent:
    async def run(self):
        print("🚀 Retriever Agent started")

        while True:
            task = pop_task(TASK_QUEUE)

            if not task:
                await asyncio.sleep(0.5)
                continue

            task_id = task.get("task_id")
            full_query = task.get("query", "")

            questions = [q.strip() for q in full_query.split("?") if q.strip()]

            push_task(STATUS_QUEUE, {
                "task_id": task_id,
                "type": "status",
                "message": "📚 Retrieving relevant knowledge..."
            })

            all_texts = []

            # 🔹 Load local docs
            local_docs = load_texts()
            all_texts.extend([doc["text"] for doc in local_docs])

            # 🔹 Fetch Wikipedia per question
            for q in questions:
                search_term = clean_query(q)

                print(f"🌍 Searching Wikipedia for: {search_term}")
                wiki_doc = fetch_wikipedia(search_term)

                # 🔁 Fallback if page fails
                if not wiki_doc and "Types Of Artificial Intelligence" in search_term:
                    wiki_doc = fetch_wikipedia("Artificial intelligence")

                if wiki_doc and wiki_doc.get("text"):
                    all_texts.append(wiki_doc["text"])

            task["retrieved_text"] = "\n".join(all_texts) if all_texts else "❌ No data retrieved"

            push_task(RETRIEVER_QUEUE, task)
