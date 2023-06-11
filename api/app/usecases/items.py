from typing import List
from pydantic import BaseModel


class TextResult(BaseModel):
    id: str
    searchfield: str


class TextSearch:
    def __init__(self, es):
        self.es = es
        self.index_name = "search-index"

    def search(self, search_query: str, size: int = 10) -> List[TextResult]:
        search_body = {
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fields": [
                        "searchfield"
                    ]
                }
            },
            "size": size
        }

        response = self.es.search(index=self.index_name, body=search_body)

        results = [TextResult(
            id=hit['_id'],
            searchfield=hit['_source']['searchfield']
        ) for hit in response['hits']['hits']]

        return results
