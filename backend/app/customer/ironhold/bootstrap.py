"""Wiring for the Ironhold deployment."""

from fastapi import FastAPI

from . import risk  # noqa: F401  (ensures risk module is importable at boot)


def install(app: FastAPI) -> None:
    # Register Ironhold routers & services here.
    return None
