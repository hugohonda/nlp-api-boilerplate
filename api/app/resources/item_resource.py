from fastapi import HTTPException
from fastapi import APIRouter
from typing import List
from app.usecases.items import Item, ItemBase
from app.gateways.elastic import es_client
from app.usecases.logging import logging

router = APIRouter()
items_base = ItemBase(es_client)


@router.get("/items/{consulta}")
async def busca_items(consulta: str, size: int = 10) -> List[Item]:
    """
    Retorna uma lista de produtos correspondentes à busca.

    Parâmetros:
    - consulta: string de busca
    - size: número máximo de resultados (padrão 10)
    """
    try:
        items = items_base.busca_items(consulta, size)
        if not items:
            error_msg = "No item found"
            logging.info(error_msg)
            raise HTTPException(
                status_code=404, detail=error_msg)
        return items

    except HTTPException as error:
        raise error
    except Exception as error:
        error_msg = f"Internal server error: {str(error)}"
        logging.error(error_msg)
        raise HTTPException(
            status_code=500, detail=error_msg)
