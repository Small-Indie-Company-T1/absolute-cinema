import os
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))

    DJANGO_API_URL = os.getenv("DJANGO_API_URL", "http://127.0.0.1:8000/api")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join(base_dir, "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() == "true"
    )
