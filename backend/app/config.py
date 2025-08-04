from dataclasses import dataclass
import os


@dataclass
class Settings:
    app_name: str = "Meridian Portfolio"
    environment: str = os.getenv("MERIDIAN_ENV", "dev")
    base_currency: str = os.getenv("BASE_CCY", "USD")
    session_secret: str = os.getenv("SESSION_SECRET", "change-me")
    # Non-empty on customer deployment branches only. Drives optional
    # imports from backend.app.customer.<customer>.
    customer: str = os.getenv("MERIDIAN_CUSTOMER", "")


settings = Settings()
