"""Wiring for the Ironhold deployment."""

from fastapi import FastAPI

from . import risk  # noqa: F401
from .trading import router as trading_router


def install(app: FastAPI) -> None:
    app.include_router(trading_router, prefix="/api")
