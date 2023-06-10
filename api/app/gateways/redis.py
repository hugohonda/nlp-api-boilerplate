import redis
import os
from dotenv import load_dotenv
load_dotenv()

redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = os.environ.get('REDIS_PORT', '6379')
redis_pass = os.environ.get('REDIS_PASSWORD')

redis_client = redis.Redis(
    host=redis_host, port=redis_port, password=redis_pass)
