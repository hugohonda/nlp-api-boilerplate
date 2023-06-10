from app.resources import item_resource
from app.resources import auth_resource
from fastapi import FastAPI, APIRouter

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
        auth_resource.router,
        tags=["Authentication"]
        # dependencies=PROTECTED
    )

    app.include_router(
        item_resource.router,
        tags=["Items"]
        # dependencies=PROTECTED
    )

    return app
