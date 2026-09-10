import os
from redis import Redis
from rq import Queue
from app.config import settings
q=Queue('fooddash',connection=Redis.from_url(settings.REDIS_URL))
def enqueue_notification(user_id,title,body,role='customer'):
    return q.enqueue('app.jobs.tasks.send_notification',user_id,title,body,role)
