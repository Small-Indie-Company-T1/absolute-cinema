import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.v1.auth import router as auth_router
from app.api.v1.search import router as search_router
from app.api.v1.recommendations import router as recommendations_router
from app.core.config import settings
from app.schemas.other import ErrorResponse
from app.core.exceptions.client_exceptions import CatalogClientError, WatchlistClientError
from app.core.exceptions.movie_exceptions import MovieNotFound

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Recommendation Service is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth_router, tags=["authentication"])
app.include_router(search_router, tags=["search"])
app.include_router(recommendations_router, tags=["recommendations"])


@app.exception_handler(MovieNotFound)
async def movie_not_found_handler(request: Request, exc: MovieNotFound):
    logger.error(f'Movie not found: {exc.message}', exc_info=True)
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error='Movie not found',
            detail = str(exc),
            status_code=404
        ).model_dump()
    )

@app.exception_handler(CatalogClientError)
async def movie_not_found_handler(request: Request, exc: CatalogClientError):
    logger.error(f'Catalog service error: {exc.message}', exc_info=True)
    return JSONResponse(
        status_code=502,
        content=ErrorResponse(
            error='Catalog service unavailable',
            detail = str(exc),
            status_code=502
        ).model_dump()
    )

@app.exception_handler(WatchlistClientError)
async def movie_not_found_handler(request: Request, exc: WatchlistClientError):
    logger.error(f'Watchlist service unavailable: {exc.message}', exc_info=True)
    return JSONResponse(
        status_code=502,
        content=ErrorResponse(
            error='Watchlist service unavailable',
            detail = str(exc),
            status_code=502
        ).model_dump()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=f"Internal server error",
            detail=str(exc) if settings.debug else "Something went wrong",
            status_code=500
        ).model_dump()
    )
