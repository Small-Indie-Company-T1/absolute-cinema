import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('flask_service/.env'))

class Config:
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', 'localhost')
    PORT = int(os.getenv('PORT', 5000))

    DJANGO_API_URL = os.getenv('DJANGO_API_URL', 'http://localhost:8000/api')