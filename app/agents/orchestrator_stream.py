from app.core.task_queue import push_task, TASK_QUEUE

class OrchestratorStream:
    """
    Submits a single task per user query.
    Agents will process it sequentially via queues.
    """
    async def execute(self, user_query: str):
        task = {
            "user_query": user_query,
            "retrieved_text": None,
            "analysis": None,
            "final_answer": None
        }

        # Push to TASK_QUEUE for Retriever
        push_task(TASK_QUEUE, task)

        yield f"status: Submitted task to Redis queue ✅\n"
        yield f"status: Agents will process and results will stream below...\n"
