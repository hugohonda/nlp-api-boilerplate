from elasticsearch import Elasticsearch
from app.utils.logging import logger
import os
from dotenv import load_dotenv
load_dotenv()


class ElasticsearchClient:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = Elasticsearch(
                [{
                    'scheme': 'http',
                    'host': self.host,
                    'port': self.port,
                }],
                basic_auth=(self.user, self.password)
            )
            logger.info("Connected to Elasticsearch")
        except Exception as error:
            logger.info(f"Error while connecting to Elasticsearch: {error}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from Elasticsearch.")


client = ElasticsearchClient(
    host=os.getenv('ELASTIC_HOST', 'elasticsearch'),
    port=int(os.getenv('ELASTIC_PORT', 9200)),
    user=os.getenv('ELASTIC_USER', 'elastic'),
    password=os.getenv('ELASTIC_PASSWORD', 'changeme')
)

client.connect()

es_client = client.connection
