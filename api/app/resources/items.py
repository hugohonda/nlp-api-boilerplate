from fastapi import HTTPException
from fastapi import APIRouter
from typing import List
from app.usecases.items import TextResult, TextSearch
from app.gateways.elastic import es_client
from app.utils.logging import logger

router = APIRouter()
textsearch = TextSearch(es_client)


@router.get("/{search}")
async def textual_search(search: str, size: int = 10) -> List[TextResult]:
    """
    Returns a list of products matching the textual search query.

    Parameters:
    - query: search query string
    - size: maximum number of results (default 10)
    """
    try:
        results = textsearch.search(search, size)
        if not results:
            error_msg = "No result found"
            logger.info(error_msg)
            raise HTTPException(
                status_code=404, detail=error_msg)
        return results

    except HTTPException as error:
        raise error
    except Exception as error:
        error_msg = f"Internal server error: {str(error)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500, detail=error_msg)
