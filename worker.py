from redis import Redis
from rq import Worker, Queue
from app.config import settings
if __name__=='__main__':
    Worker([Queue('fooddash',connection=Redis.from_url(settings.REDIS_URL))],connection=Redis.from_url(settings.REDIS_URL)).work()
