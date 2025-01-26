from datetime import datetime, timedelta, timezone
from typing import Union, Optional
import jwt
from passlib.context import CryptContext
from db.db_models import UserModel
from db.db_repository import get_user
from settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the provided plain text password matches the hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if passwords match, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hashed password from a plain text password.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> Optional[UserModel]:
    """
    Authenticate a user by verifying the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The plain text password of the user.

    Returns:
        Optional[UserModel]: The authenticated user object if credentials are valid, otherwise None.
    """
    user: Optional[UserModel] = await get_user(username=username)
    if user and verify_password(plain_password=password, hashed_password=user.hashed_password):
        return user
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with an expiration time.

    Args:
        data (dict): The data to include in the token.
        expires_delta (Optional[timedelta]): The expiration time for the token.
                                             Defaults to the configured expiration time.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)
    return encoded_jwt
