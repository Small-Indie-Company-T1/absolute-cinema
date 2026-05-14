import os


class Settings:
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

settings = Settings()
