
# app/workers/queue.py
import redis
from rq import Queue
from app.config import settings

redis_conn = redis.from_url(settings.REDIS_URL or "redis://localhost:6379/0")
q = Queue("default", connection=redis_conn)
