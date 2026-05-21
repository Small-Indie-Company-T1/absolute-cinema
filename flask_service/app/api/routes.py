from flask import Blueprint, jsonify, request


api_bp = Blueprint("api", __name__)

@api_bp.get('/health')
def healthcheck():
    return jsonify({
        'status': 'success',
        'data': {
            'service': 'reviews_service',
            'message': 'Reviews service is running'
        }
    }), 200

@api_bp.get('/reviews')
def list_reviews():
    movie_id = request.args.get('movie_id')
    return jsonify({
        'status': 'success',
        'data': {
            'items': [],
            'filters': {
                'movie_id': movie_id
            }
        }
    }), 200

@api_bp.post('/reviews')
def create_review():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'invalid_json',
                'message': 'Request body must be a valid json'
            }
        }), 400
    return jsonify({
        'status': 'success',
        'data': {
            'message': 'Review accepted',
            'payload': payload
        }
    }), 201

@api_bp.patch('/reviews/<int:review_id>/status')
def update_review_status(review_id: int):
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'invalid_json',
                'message': 'Request body must be a valid json'
            }
        }), 400
    
    return jsonify({
        'status': 'success',
        'data': {
            'id': review_id,
            'new_status': payload.get('status')
        }
    }), 200
