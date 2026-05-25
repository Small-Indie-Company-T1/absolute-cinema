import logging
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    jwt_secret: str = Field(...)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15

    django_api_url: str = "http://localhost:8000/api"

    cors_origins: list[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]

    debug: bool = True

    model_config = SettingsConfigDict(
        env_file= ROOT / '.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

try:
    settings = Settings()
except Exception as e:
    logger.error(f'Configuration error (Forgot to create .env?): {e}')
    raise
