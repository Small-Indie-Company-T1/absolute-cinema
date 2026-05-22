import logging
from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from ..schemas.review import ErrorResponse
from ..services.django_client import check_movie_exists
from ..schemas.review import ReviewCreate

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
    movie_id = request.args.get("movie_id")

    if movie_id is None:
        return jsonify(
            ErrorResponse(
                error="missing_parameter",
                detail="Query parameter 'movie_id' is required",
                status_code=400,
            ).model_dump()
        ), 400

    # TODO: get_reviews_by_movie
    reviews = []

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
            ErrorResponse(
                error="invalid_json",
                detail="Request body must be a valid json",
                status_code=400,
            ).model_dump()
        ), 400

    try:
        validated = ReviewCreate(**payload)  # type: ignore
    except ValidationError as e:
        logger.warning(f"Validation error while creating review: {e.errors()}")
        return jsonify(
            ErrorResponse(
                error="validation_error", detail="Invalid review data", status_code=422
            ).model_dump()
        ), 422

    movie_exists = check_movie_exists(validated.movie_id)
    if not movie_exists:
        logger.warning(f"Movie {validated.movie_id} not found in Django")
        return jsonify(
            ErrorResponse(
                error="movie_not_found",
                detail=f"Movie with id {validated.movie_id} does not exist",
                status_code=404,
            ).model_dump()
        ), 404

    # TODO: вызвать create_review

    logger.info(
        f"Review created: movie_id={validated.movie_id}, user_id={validated.user_id}"
    )

    return jsonify(
        {
            "status": "success",
            "data": {
                "id": 1,
                "movie_id": validated.movie_id,
                "user_id": validated.user_id,
                "rating": validated.rating,
                "text": validated.text,
                "status": "pending",
                "created_at": "2024-01-01T12:00:00Z",
            },
        }
    ), 201


@api_bp.patch("/reviews/<int:review_id>/status")
def update_review_status(review_id: int):
    """
    Обновить статус отзыва (модерация).
    Ожидает JSON: {status: "active" | "hidden"}
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify(
            ErrorResponse(
                error="invalid_json",
                detail="Request body must be a valid json",
                status_code=400,
            ).model_dump()
        ), 400

    new_status = payload.get("status")  # type: ignore
    if new_status not in ("active", "hidden"):
        return jsonify(
            ErrorResponse(
                error="invalid_status",
                detail="Status must be 'active' or 'hidden'",
                status_code=422,
            ).model_dump()
        ), 422

    # TODO: update_review_status

    logger.info(f"Review {review_id} status updated to {new_status}")

    return jsonify(
        {
            "status": "success",
            "data": {"id": review_id, "new_status": new_status},
        }
    ), 200
