from typing import List
from pydantic import BaseModel

# Definição do modelo de dados de medicamentos
class Item(BaseModel):
    id: str
    nome: str


# Definição da classe
class ItemBase:
    def __init__(self, es):
        self.es = es
        self.index_name = "items_index"

    # Método de busca de produtos
    def busca_items(self, search_query: str, size: int = 10) -> List[Item]:
        # Configuração do filtro de busca
        search_body = {
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fields": [
                        "nome"
                    ]
                }
            },
            "size": size
        }

        # Busca no Elasticsearch
        response = self.es.search(index=self.index_name, body=search_body)

        # Transforma os resultados em objetos Medicamento
        items = [Item(
            id=hit['_id'],
            nome=hit['_source']['nome']
        ) for hit in response['hits']['hits']]

        return items