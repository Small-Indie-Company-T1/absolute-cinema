import logging
from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from ..schemas.review import ErrorResponse, ReviewStatusUpdate, ReviewCreate
from ..services.django_client import (
    DjangoConnectionError,
    DjangoIntegrationError,
    DjangoTimeoutError,
    MovieNotFoundError,
    check_movie_exists,
)
from ..repositories import review_repository

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def healthcheck():
    return jsonify(
        {
            "status": "success",
            "data": {
                "service": "reviews_service",
                "message": "Reviews service is running",
            },
        }
    ), 200


@api_bp.get("/reviews")
def list_reviews():
    """
    Получить список отзывов по фильму.
    Query param: movie_id (обязательный)
    """
    movie_id_str = request.args.get("movie_id")

    if movie_id_str is None:
        return jsonify(
            ErrorResponse.build(
                code="missing_parameter",
                message='Query parameter "movie_id" is required',
            )
        ), 400

    try:
        movie_id = int(movie_id_str)
    except ValueError:
        return jsonify(
            ErrorResponse.build(
                code="invalid_parameter",
                message='Query parameter "movid_id" must be an integer',
            )
        ), 400

    reviews = review_repository.get_reviews_by_movie(movie_id)

    return jsonify(
        {
            "status": "success",
            "data": {"items": reviews, "filters": {"movie_id": movie_id}},
        }
    ), 200


@api_bp.post("/reviews")
def create_review():
    """
    Создать новый отзыв.
    Ожидает JSON: {movie_id, user_id, rating, text}
    """
    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify(
            ErrorResponse.build(
                code="invalid_json", message="Request body must be a valid json"
            )
        ), 400

    try:
        validated = ReviewCreate(**payload)  # type: ignore
    except ValidationError as e:
        logger.warning(f"Validation error while creating review: {e.errors()}")
        return jsonify(
            ErrorResponse.build(
                code="validation_error",
                message="Invalid review data",
                details=e.errors(),
            )
        ), 422

    try:
        check_movie_exists(validated.movie_id)
    except MovieNotFoundError:
        return jsonify(
            ErrorResponse.build(
                code="movie_not_found",
                message=f"Movie with id {validated.movie_id} does not exist",
            )
        ), 404
    except DjangoTimeoutError:
        logger.error(
            f"Django API timeout while checking movie with id {validated.movie_id}"
        )
        return jsonify(
            ErrorResponse.build(
                code="integration_timeout", message="Django service is not responding"
            )
        ), 503
    except DjangoConnectionError:
        logger.error("Cannot connect to Django")
        return jsonify(
            ErrorResponse.build(
                code="integration_unavailable", message="Django service is unavailable"
            )
        ), 503
    except DjangoIntegrationError as e:
        logger.error(f"Django integration error: {e}")
        return jsonify(
            ErrorResponse.build(
                code="integration_error",
                message="Error communcation with Django service",
            )
        ), 503

    review = review_repository.create_review(
        movie_id=validated.movie_id,
        user_id=validated.user_id,
        rating=validated.rating,
        text=validated.text,
    )

    logger.info(
        f"Review created: movie_id={validated.movie_id}, user_id={validated.user_id}"
    )

    return jsonify({"status": "success", "data": review.to_dict()}), 201


@api_bp.patch("/reviews/<int:review_id>/status")
def update_review_status(review_id: int):
    """
    Обновить статус отзыва (модерация).
    Ожидает JSON: {status: "active" | "hidden"}
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify(
            ErrorResponse.build(
                code="invalid_json", message="Request body must be a valid json"
            )
        ), 400

    try:
        validated = ReviewStatusUpdate(**payload) # type: ignore
    except ValidationError as e:
        logger.warning(f"Validation error while updating review status: {e.errors()}")
        return jsonify(
            ErrorResponse.build(
                code="validation_error",
                message="Invalid status data",
                details=e.errors(),
            )
        ), 422

    review = review_repository.update_review_status(review_id, status=validated.status)
    if review is None:
        return jsonify(
            ErrorResponse.build(
                code="review_not_found", message=f"Review with id {review_id} not found"
            )
        ), 404

    logger.info(f"Review {review_id} status updated to {validated.status}")

    return jsonify(
        {
            "status": "success",
            "data": review.to_dict(),
        }
    ), 200


@api_bp.get("/reviews/<int:review_id>")
def get_review(review_id: int):
    review = review_repository.get_review_by_id(review_id)
    if review is None:
        return jsonify(
            ErrorResponse.build(
                code="review_not_found", message=f"Review with id {review_id} not found"
            )
        ), 404

    return jsonify({"status": "success", "data": review.to_dict()}), 200
