ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'src.core.exceptions.custom_exception_handler',
}