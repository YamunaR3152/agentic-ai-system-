import asyncio
from app.core.task_queue import (
    TASK_QUEUE,
    RETRIEVER_QUEUE,
    ANALYZER_QUEUE,
    STATUS_QUEUE,
    pop_task,
    push_task
)

class AgentWorker:
    async def start(self):
        print("🤖 Agent Worker started...")

        while True:
            # STEP 1 — Wait for retriever output
            task = pop_task(RETRIEVER_QUEUE)

            if not task:
                await asyncio.sleep(0.5)
                continue

            task_id = task.get("task_id")
            query = task.get("query") or task.get("user_query", "")
            retrieved_text = task.get("retrieved_text", "")

            # -------------------------------
            # STEP 2 — Status: Analyzing
            # -------------------------------
            push_task(STATUS_QUEUE, {
                "task_id": task_id,
                "type": "status",
                "message": "🧠 Analyzing retrieved knowledge..."
            })

            await asyncio.sleep(1)

            # -------------------------------
            # STEP 3 — Generate answer FROM TEXT
            # -------------------------------
            push_task(STATUS_QUEUE, {
                "task_id": task_id,
                "type": "status",
                "message": "✍️ Generating answer from documents..."
            })

            await asyncio.sleep(1)

            if not retrieved_text or "❌" in retrieved_text:
                final_answer = "I couldn’t find relevant information in the knowledge sources."
            else:
                # SIMPLE CONTEXT-BASED ANSWER GENERATION
                # (You can replace with LLM later)
                snippets = retrieved_text.split("\n")[:5]  # Take top few chunks
                context = " ".join(snippets)

                final_answer = (
                    f"Based on the retrieved knowledge:\n\n{context[:1200]}"
                )

            # -------------------------------
            # STEP 4 — Send Final Answer
            # -------------------------------
            push_task(STATUS_QUEUE, {
                "task_id": task_id,
                "type": "final",
                "message": final_answer
            })
