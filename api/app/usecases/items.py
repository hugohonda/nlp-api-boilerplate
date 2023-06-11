from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    searchfield: str

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "items": [
    #                 {
    #                     "id": 1,
    #                     "searchfield": "My text 1"
    #                 },
    #                 {
    #                     "id": 2,
    #                     "searchfield": "My text 2"
    #                 }
    #             ]
    #         }
    #     }


class ItemBase:
    def __init__(self, es):
        self.es = es
        self.index_name = "items_index"

    def get_items(self, search_query: str, size: int = 10) -> List[Item]:
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

        items = [Item(
            id=hit['_id'],
            searchfield=hit['_source']['searchfield']
        ) for hit in response['hits']['hits']]

        return items
