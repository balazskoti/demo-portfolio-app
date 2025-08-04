"""Wiring for the Ironhold deployment.

Called from the application factory when ``settings.customer == "ironhold"``.
Registers Ironhold-only routers, dependencies and scheduled jobs.
"""

from fastapi import FastAPI


def install(app: FastAPI) -> None:
    # Subsequent commits on this branch register routers/services here.
    return None
