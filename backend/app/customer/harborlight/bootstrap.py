"""Wiring for the Harborlight deployment."""

from fastapi import FastAPI

from . import esg  # noqa: F401  (pre-trade screening hook is imported on boot)


def install(app: FastAPI) -> None:
    # Subsequent commits register routers/services here.
    return None
