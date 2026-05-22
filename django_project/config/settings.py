from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# Application definition
FASTAPI_SERVICE_URL = "http://localhost:8001"

load_dotenv(BASE_DIR / ".env")

include(
    "components/apps.py",
    "components/base_settings.py",
    "components/cors.py",
    "components/databases.py",
    "components/internationalization.py",
    "components/middlewares.py",
    "components/security.py",
    "components/static.py",
    "components/templates.py",
    "components/validators.py",
)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
