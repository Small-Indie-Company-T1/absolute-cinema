from app.core.exceptions.app_exceptions import AppException


class MovieError(AppException):
    ...

class MovieNotFound(MovieError):
    status_code = 404
