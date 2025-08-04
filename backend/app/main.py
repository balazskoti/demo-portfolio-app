from fastapi import FastAPI

from .api.routes import router
from .config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(router, prefix="/api")

    if settings.customer == "ironhold":
        from .customer.ironhold.bootstrap import install as install_ironhold

        install_ironhold(app)

    return app


app = create_app()
