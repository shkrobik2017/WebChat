from fastapi import APIRouter, status, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from db.db_repository import get_user, create_user
from logger.logger import logger
from routers.user_router.services import authenticate_user, create_access_token, get_password_hash
from settings import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/signup", response_class=HTMLResponse)
async def get_signup_page(request: Request, error: str = None) -> HTMLResponse:
    """
    Serve the signup page with an optional error message.

    Args:
        request (Request): The request object.
        error (str, optional): An error message to display. Defaults to None.

    Returns:
        HTMLResponse: The rendered signup page with error message if any.
    """
    return templates.TemplateResponse("signup.html", {"request": request, "error": error})


@router.post("/signup", response_class=RedirectResponse)
async def signup(username: str = Form(...), password: str = Form(...)) -> RedirectResponse:
    """
    Handle the signup process, creating a new user.

    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.

    Returns:
        RedirectResponse: A redirect to the signin page if successful or an error page if the user already exists.
    """
    try:
        if await get_user(username=username):
            logger.error(f"User {username} redirected to sign up page because is already registered")
            return RedirectResponse(url="/signup?error=User+already+registered", status_code=303)

        hashed_pass = get_password_hash(password)
        await create_user(username=username, hashed_pass=hashed_pass)

        return RedirectResponse(url="/signin", status_code=303)
    except Exception as ex:
        logger.error(f"An error occurred in signup method: {ex}")
        raise HTTPException(status_code=500)


@router.get("/signin", response_class=HTMLResponse)
async def signin_page(request: Request, error: str = None) -> HTMLResponse:
    """
    Serve the signin page with an optional error message.

    Args:
        request (Request): The request object.
        error (str, optional): An error message to display. Defaults to None.

    Returns:
        HTMLResponse: The rendered signin page with error message if any.
    """
    return templates.TemplateResponse("signin.html", {"request": request, "error": error})


@router.post("/signin", response_class=RedirectResponse)
async def login_for_access_token(username: str = Form(...), password: str = Form(...)) -> RedirectResponse:
    """
    Authenticate the user and return an access token.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        RedirectResponse: A redirect to the chat page with an access token set in the cookie.
    """
    try:
        user = await authenticate_user(username=username, password=password)
        if not user:
            logger.error(f"User {username} redirected to sign in page because does not exist")
            return RedirectResponse(url="/signin?error=User+does+not+exist", status_code=303)

        access_token = create_access_token(data={"sub": username})
        response = RedirectResponse(url="/chat", status_code=status.HTTP_302_FOUND)
        logger.info(f"User {username} authenticate and redirected to chat page")

        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="strict",
        )
        logger.info(f"Set cookie for user {username}.")

        return response
    except Exception as ex:
        logger.error(f"An error occurred in signin method: {ex}")
        raise HTTPException(status_code=500)

