from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str = "secret-key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 2

    django_api_url: str = "http://localhost:8000/api"

    cors_origins: list = ["http://localhost:8000", "http://127.0.0.1:8000"]

    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
