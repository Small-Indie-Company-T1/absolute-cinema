from fastapi import APIRouter, HTTPException, status
import httpx

from ...core.auth import create_access_token
from ...schemas.auth import Token, UserIn
from ...core.config import settings

import logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/auth")

@router.post("/login", response_model=Token)
async def login(user_data: UserIn):
    url = f'{settings.django_api_url}/users/login/'

    async with httpx.AsyncClient(timeout=5.0) as ac:
        response = await ac.post(
            url, json={
                'email': user_data.email,
                'password': user_data.password
            }
        )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    data = response.json()

    logger.info(f"User logged in: {user_data.email}")
    access_token = create_access_token(data={"sub": str(user_data.get('id'))})
    return Token(access_token=access_token, token_type="bearer")
