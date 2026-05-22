class MovieNotFound(Exception):
    """Исключение, возникающее при попытке добавить фильм, которого не существует."""
    ...
class RecommendationServiceError(Exception):
    """Ошибка при обращении к сервису рекомендаций FastAPI"""
    pass