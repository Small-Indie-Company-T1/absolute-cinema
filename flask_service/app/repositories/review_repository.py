from ..models import Review
from ..extensions import db


def create_review(movie_id: int, user_id: int, rating: int, text: str) -> Review:
    """Создаёт и сохраняет новый отзыв в БД"""
    review = Review(movie_id=movie_id, user_id=user_id, rating=rating, text=text) # type: ignore
    db.session.add(review)
    db.session.commit()
    return review


def get_reviews_by_movie(movie_id: int) -> list[Review]:
    """Возвращает все отзывы для фильма"""
    return db.session.query(Review).filter(Review.movie_id == movie_id).all()


def update_review_status(review_id: int, status: str) -> Review | None:
    """Обновляет статус отзыва"""
    db.session.query(Review).filter(Review.id == review_id).update({"status": status})
    db.session.commit()
    return db.session.query(Review).filter(Review.id == review_id).first()


def get_review_by_id(review_id: int) -> Review:
    """Возвращает отзыв по его id"""
    return db.session.query(Review).filter(Review.id == review_id).first()
