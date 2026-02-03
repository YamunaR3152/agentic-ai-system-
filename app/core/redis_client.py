import redis

def get_redis_client():
    """
    Creates and returns a Redis client.
    Used as a message queue between agents.
    """
    return redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )
