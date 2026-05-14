from fastapi import FastAPI

from app.api.v1.search import router as search_router


app = FastAPI()

@app.get("/")
def main():
    return {"message": "Hello World"}

@app.get('/health')
def health_check():
    return {'status': 'ok'}

app.include_router(search_router, tags=['search'])
