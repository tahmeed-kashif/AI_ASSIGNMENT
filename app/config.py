import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    whatsapp_token: str
    whatsapp_phone_number_id: str
    verify_token: str
    db_path: str
    timezone: str
    app_base_url: str | None


def load_settings() -> Settings:
    return Settings(
        whatsapp_token=os.getenv("WHATSAPP_TOKEN", ""),
        whatsapp_phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID", ""),
        verify_token=os.getenv("VERIFY_TOKEN", ""),
        db_path=os.getenv("DB_PATH", "/workspace/data/bot.db"),
        timezone=os.getenv("TIMEZONE", "UTC"),
        app_base_url=os.getenv("APP_BASE_URL") or None,
    )

