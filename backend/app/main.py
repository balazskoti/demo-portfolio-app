from fastapi import FastAPI

from .api.routes import router
from .config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(router, prefix="/api")
    return app


app = create_app()
