from fastapi import Header, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from starlette import status

from config import Settings
from api.dependencies.stubs import get_config


API_TOKEN_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_TOKEN_NAME, auto_error=False)


async def verify_token(
    authorization: str = Security(api_key_header),
    config: Settings = Depends(get_config),
):
    expected = f"Bearer {config.api_token}"
    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
        )
