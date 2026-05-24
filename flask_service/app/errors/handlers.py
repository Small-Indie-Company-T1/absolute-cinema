from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError
import logging

from ..schemas.review import ErrorResponse

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask):
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify(
            ErrorResponse.build(
                code='not_found',
                message='The requested resource was not found'
            )
        ), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify(
            ErrorResponse.build(
                code='method_not_allowed',
                message='HTTP method not allowed for this endpoint'
            )
        ), 405

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify(
            ErrorResponse.build(
                code='bad_request',
                message='Invalid request format'
            )
        ), 400

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation(error):
        """Обработчик ошибок валидации Pydantic"""
        return jsonify(
            ErrorResponse.build(
                code='validation_error',
                message='Invalid data provided',
                details=error.errors()
            )
        ), 422

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Обработчик всех HTTP исключений"""
        return jsonify(
            ErrorResponse.build(
                code=error.name.lower().replace(' ', '_'),
                message=error.description
            )
        ), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        """Обработчик всех непредвиденных ошибок"""
        logger.error(f"Unexpected error: {error}", exc_info=True)
        return jsonify(
            ErrorResponse.build(
                code='internal_server_error',
                message='An unexpected error occured'
            )
        ), 500
