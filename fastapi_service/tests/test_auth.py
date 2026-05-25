from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str

def create_test_client():
    app = FastAPI()

    @app.post("/auth/login")
    def login(payload: LoginSchema):
        if payload.password == "wrong":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized"
            )
        return {"access_token": "token"}

    return TestClient(app)

def test_login_invalid_password():
    client = create_test_client()
    payload = {'email': 'test@test.com', 'password': 'wrong'}
    response = client.post('/auth/login', json=payload)
    assert response.status_code == 401