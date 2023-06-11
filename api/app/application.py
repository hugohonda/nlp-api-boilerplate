from app.resources import items
from app.resources import auth
from fastapi import FastAPI, APIRouter, Request

api_router = APIRouter()

def create_app():
    app = FastAPI(
        title="API Items",
        description="Textual Search - Elasticsearch",
        version="0.0.1",
        openapi_url="/openapi.json",
        docs_url="/",
        redoc_url="/redoc"
    )

    app.include_router(
        auth.router,
        prefix="/auth",
        tags=["Authentication"]
        # dependencies=PROTECTED
    )

    app.include_router(
        items.router,
        prefix="/items",
        tags=["Items"]
        # dependencies=PROTECTED
    )

    # app.on_event("startup")
    # async def startup_event():
        
    # app.on_event("shutdown")
    # def shutdown_event():

    return app
