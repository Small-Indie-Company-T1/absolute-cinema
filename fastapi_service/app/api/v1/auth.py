from fastapi import APIRouter, HTTPException, status

from ...core.auth import create_access_token
from ...schemas.auth import Token, UserIn

import logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/auth")

@router.post("/login", response_model=Token)
async def login(user_data: UserIn):
    # TODO: Integrate django for validation
    if user_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = 1  # Placeholder for user ID by email from Django

    logger.info(f"User logged in: {user_data.email}")
    access_token = create_access_token(data={"sub": str(user_id)})
    return Token(access_token=access_token, token_type="bearer")
