from fastapi import FastAPI
from fastapi.testclient import TestClient

def create_test_client():
    app = FastAPI()

    @app.get("/")
    def root():
        return {"message": "Welcome to Absolute Cinema FastAPI"}

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return TestClient(app)

def test_root():
    client = create_test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert 'message' in response.json()

def test_health():
    client = create_test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'