from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
load_dotenv()

es_client = Elasticsearch(
    [{
        'scheme': 'http',
        'host': os.getenv('ELASTIC_HOST', 'elasticsearch'),
        'port': int(os.getenv('ELASTIC_PORT', 9200)),
    }],
    basic_auth=(os.getenv('ELASTIC_USER', 'elastic'),
                os.getenv('ELASTIC_PASSWORD', 'changeme'))
)
