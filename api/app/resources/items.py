from fastapi import HTTPException
from fastapi import APIRouter
from typing import List
from app.usecases.items import Item, ItemBase
from app.gateways.elastic import es_client
from app.utils.logging import logger

router = APIRouter()
items_base = ItemBase(es_client)


@router.get("/items/{consulta}")
async def get_items(query: str, size: int = 10) -> List[Item]:
    """
    Returns a list of products matching the search query.

    Parameters:
    - query: search query string
    - size: maximum number of results (default 10)
    """
    try:
        items = items_base.get_items(query, size)
        if not items:
            error_msg = "No item found"
            logger.info(error_msg)
            raise HTTPException(
                status_code=404, detail=error_msg)
        return items

    except HTTPException as error:
        raise error
    except Exception as error:
        error_msg = f"Internal server error: {str(error)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500, detail=error_msg)
