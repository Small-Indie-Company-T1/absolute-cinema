from models.review import Review


def create_review(movie_id: int, user_id: int, rating: int, text: str) -> Review:
    """Создаёт и сохраняет новый отзыв в БД"""
    ...


def get_reviews_by_movie(movie_id: int) -> list[Review]:
    """Возвращает все отзывы для фильма"""
    ...


def update_review_status(review_id: int, status: str) -> Review | None:
    """Обновляет статус отзыва"""
    ...
