from flask import Flask, jsonify
from werkzeug .exceptions import HTTPException


def register_error_handlers(app: Flask):
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'not_found',
                'message': 'Not found'
            }
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'method_not_allowed',
                'message': 'Method not allowed'
            }
        }), 405
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            'status': 'error',
            'error': {
                'code': error.name.lower().replace(' ', '_'),
                'message': error.description
            }
        }), error.code
    
    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'internal_server_error',
                'message': 'Unexpected error occured'
            }
        }), 500
