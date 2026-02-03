from app.core.task_queue import push_task, TASK_QUEUE

def decompose_task(user_query: str):
    """
    Converts a complex task into subtasks for different agents.
    """

    subtasks = [
        {
            "agent": "retriever",
            "user_query": user_query
        },
        {
            "agent": "analyzer",
            "user_query": f"Analyze retrieved research papers for: {user_query}"
        },
        {
            "agent": "writer",
            "user_query": f"Summarize findings for: {user_query}"
        }
    ]

    for task in subtasks:
        push_task(TASK_QUEUE, task)
