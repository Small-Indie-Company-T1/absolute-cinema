from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

def create_test_client():
    app = FastAPI()

    @app.get("/api/v1/search")
    def search(q: str = None, limit: int = Query(default=10, le=50)):
        if limit > 50:
            return {"detail": "Limit too high"}, 422
        return {"results": []}

    return TestClient(app)

def test_search_movies():
    client = create_test_client()
    response = client.get('/api/v1/search?q=batman')
    assert response.status_code == 200

def test_search_invalid_limit():
    client = create_test_client()
    response = client.get('/api/v1/search?limit=1000')
    # FastAPI на Query(le=50) автоматически выкидывает 422
    assert response.status_code == 422