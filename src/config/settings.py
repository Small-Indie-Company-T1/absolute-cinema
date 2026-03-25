from pathlib import Path
from split_settings.tools import include

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# Application definition

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
