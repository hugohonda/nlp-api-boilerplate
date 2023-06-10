QA_INDEX_NAME = "qa-index"

QA_INDEX_SYNONYMS = []

QA_INDEX_SETTINGS = {
    "analysis": {
        "analyzer": {},
        "filter": {},
    },
}

QA_INDEX_MAPPINGS = {
    "properties": {
        "question": {"type": "text"},
        "answer": {"type": "text"},
        "annotations": {"type": "text"},
        "metadata": {"type": "object"}
    }
}
