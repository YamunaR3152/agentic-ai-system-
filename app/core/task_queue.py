from collections import deque

# User submits tasks here
TASK_QUEUE = deque()

# Retriever → Analyzer
RETRIEVER_QUEUE = deque()

# Analyzer → Writer
ANALYZER_QUEUE = deque()

# Messages for frontend polling
STATUS_QUEUE = deque()


def push_task(queue, item):
    queue.append(item)


def pop_task(queue):
    if queue:
        return queue.popleft()
    return None
