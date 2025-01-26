import jwt
from typing import Dict, Optional, Union
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from db.db_models import UserModel
from db.db_repository import get_user
from logger.logger import logger
from settings import settings


async def get_token_from_cookie_ws(cookies: Dict[bytes, bytes]) -> str:
    """
    Extract the token from the cookies passed in the WebSocket connection.

    Args:
        cookies (Dict[bytes, bytes]): The cookies in the WebSocket connection.

    Returns:
        str: The extracted token if valid.

    Raises:
        HTTPException: If the cookie is missing or the token format is invalid.
    """
    cookie_header: Optional[bytes] = cookies.get(b"cookie")
    if cookie_header:
        cookie_value = cookie_header.decode()
        token: Optional[str] = cookie_value.split("=")[1].replace('"', "")
        if token.startswith("Bearer "):
            return token[len("Bearer "):]

        logger.error("Invalid token format")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token format"
        )
    logger.error("Token not found")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token not found"
    )


def validation_token_from_cookie(token: Optional[str]) -> Union[str, RedirectResponse]:
    """
    Validate the token and extract the username if valid.

    Args:
        token (Optional[str]): The token to validate.

    Returns:
        Union[str, RedirectResponse]: The username if token is valid, otherwise a redirect response.
    """
    if not token:
        return RedirectResponse(url="/signin?error=Token+is+missing")
    try:
        payload: dict = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM],
        )
        username: Optional[str] = payload.get("sub")
        if not username:
            return RedirectResponse(url="/signin?error=Invalid+credentials")
        return username
    except jwt.PyJWTError:
        return RedirectResponse(url="/signin?error=Invalid+token")


async def get_current_user(token: str) -> UserModel:
    """
    Retrieve the current user based on the provided token.

    Args:
        token (str): The token to validate and extract the username.

    Returns:
        UserModel: The user associated with the valid token.

    Raises:
        HTTPException: If the token is invalid or expired, or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM],
        )
        username: Optional[str] = payload.get("sub")
        if not username:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.PyJWTError:
        raise credentials_exception

    user: Optional[UserModel] = await get_user(username=username)
    if not user:
        raise credentials_exception
    return user

