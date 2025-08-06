from fastapi import FastAPI

from .api.routes import router
from .config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(router, prefix="/api")

    if settings.customer == "harborlight":
        from .customer.harborlight.bootstrap import install as install_harborlight

        install_harborlight(app)

    return app


app = create_app()
