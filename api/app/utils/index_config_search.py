SEARCH_INDEX_NAME = "search-index"

SEARCH_INDEX_SYNONYMS = []

SEARCH_INDEX_SETTINGS = {
    "analysis": {
        "analyzer": {
            "index_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "autocomplete_filter",
                ],
            },
            "search_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "synonym_filter",
                    "asciifolding"
                ],
            },
        },
        "filter": {
            "synonym_filter": {
                "type": "synonym_graph",
                "expand": True,
                "lenient": True,
                "synonyms": SEARCH_INDEX_SYNONYMS,
            },
            "autocomplete_filter": {
                "type": "edge_ngram",
                "min_gram": 1,
                "max_gram": 20,
            },
        },
    },
}

SEARCH_INDEX_MAPPINGS = {
    "properties": {
        "searchfield": {
            "type": "text",
            "search_analyzer": "search_analyzer",
            "fields": {
                "ngrams": {
                    "type": "text",
                    "analyzer": "index_analyzer",
                    "search_analyzer": "search_analyzer",
                },
            }
        }
    }
}
