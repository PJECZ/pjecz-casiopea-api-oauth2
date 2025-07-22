"""
Redis
"""

from typing import Annotated

import rq
from fastapi import Depends
from redis import ConnectionPool, Redis

from ..config.settings import Settings, get_settings

# Crear una conexión global a Redis
pool = None


def get_redis_pool(settings: Annotated[Settings, Depends(get_settings)]) -> ConnectionPool:
    """Get Redis connection pool"""
    global pool
    if pool is None:
        # Create a new connection pool if it doesn't exist
        pool = ConnectionPool.from_url(url=settings.REDIS_URL)
    return pool


def get_task_queue(settings: Annotated[Settings, Depends(get_settings)]) -> rq.Queue:
    """Get Redis task queue"""

    # Get the Redis connection pool
    pool = get_redis_pool(settings)

    # Create Redis connection
    redis_conn = Redis(connection_pool=pool)

    # Return task queue
    try:
        return rq.Queue(name=settings.TASK_QUEUE, connection=redis_conn, default_timeout=3600)
    except Exception as error:
        raise RuntimeError(f"Error creating task queue: {error}") from error
