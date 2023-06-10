from fastapi import HTTPException
from fastapi import APIRouter
from typing import List
from app.items import Item, ItemBase
from app.gateways.elastic import es_client

router = APIRouter()

# Criação da instância da classe
items_base = ItemBase(es_client)

# Definição da rota de busca
@router.get("/items/{consulta}")
async def busca_items(consulta: str, size: int = 10) -> List[Item]:
    """
    Retorna uma lista de produtos correspondentes à busca.

    Parâmetros:
    - consulta: string de busca
    - size: número máximo de resultados (padrão 10)
    """
    items = items_base.busca_items(consulta, size)
    if not items:
        raise HTTPException(status_code=404, detail="Nenhum item encontrado.")
    return items