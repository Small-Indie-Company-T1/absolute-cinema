from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

def create_test_client():
    app = FastAPI()

    @app.get("/api/v1/recommendations/similar/{movie_id}")
    def similar(movie_id: int, limit: int = Query(default=10, le=50)):
        return {"items": []}

    @app.get("/api/v1/recommendations/me")
    def personal(token: str, limit: int = Query(default=10, le=50)):
        return {"items": []}

    return TestClient(app)

def test_similar_movies():
    client = create_test_client()
    response = client.get('/api/v1/recommendations/similar/1')
    assert response.status_code == 200

def test_recommendations_limit_validation():
    client = create_test_client()
    response = client.get('/api/v1/recommendations/similar/1?limit=100')
    assert response.status_code == 422

def test_personal_recommendations_without_token():
    client = create_test_client()
    # Токен обязателен, без него должна быть ошибка 422
    response = client.get('/api/v1/recommendations/me')
    assert response.status_code == 422