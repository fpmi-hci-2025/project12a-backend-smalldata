from fastapi import Header, HTTPException, status

from config import config


async def authorize(authorization: str = Header(...)) -> None:

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
        )

    token = authorization.removeprefix("Bearer ").strip()
    if token != config.auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
