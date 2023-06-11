import redis
from app.utils.logging import logger
import os
from dotenv import load_dotenv
load_dotenv()


class RedisClient:
    def __init__(self, host, port, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password
            )
            logger.info("Connected to Redis!")
        except Exception as error:
            logger.error(f"Error while connecting to Redis: {error}")

    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected from Redis.")


client = RedisClient(
    host=os.environ.get('REDIS_HOST', 'redis'),
    port=os.environ.get('REDIS_PORT', '6379'),
    password=os.environ.get('REDIS_PASSWORD')
)

client.connect()

redis_client = client.connection
