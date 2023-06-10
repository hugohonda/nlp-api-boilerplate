"""Script to load category data to ES index."""
import argparse
import sys
from app.gateways.elastic import es_client
from elasticsearch import helpers
import csv

from api.app.utils.index_config_search import (
    SEARCH_INDEX_NAME,
    SEARCH_INDEX_SETTINGS,
    SEARCH_INDEX_MAPPINGS,
)

SEARCH_DATA_PATH = 'data.csv'


def load_data_to_index():
    """Load item documents to the Elasticsearch index."""
    with open(SEARCH_DATA_PATH) as f:
        reader = csv.DictReader(f)
        helpers.bulk(es_client, reader, index=SEARCH_INDEX_NAME)


def create_index():
    """Create the ES index."""
    es_client.indices.create(
        index=SEARCH_INDEX_NAME,
        settings=SEARCH_INDEX_SETTINGS,
        mappings=SEARCH_INDEX_MAPPINGS,
    )


if __name__ == "__main__":

    if (es_client.indices.exists(index=SEARCH_INDEX_NAME)):
        es_client.options(ignore_status=404).indices.delete(
            index=SEARCH_INDEX_NAME)

    try:
        create_index()
        load_data_to_index()
    except Exception as exc:
        sys.exit(1)
    finally:
        es_client.close()
