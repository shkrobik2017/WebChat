from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from logger.logger import logger
from routers.services import validation_token_from_cookie

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """
    Render the main page, ensuring that the user is authenticated.

    Args:
        request (Request): The HTTP request object, which includes cookies for authentication.

    Returns:
        HTMLResponse: The rendered HTML response containing the main page.
    """
    try:
        cookie_header: str = request.cookies.get("access_token", "")
        if not cookie_header or not cookie_header.startswith("Bearer "):
            logger.info("User is not authenticated")
            raise HTTPException(status_code=401, detail="Not authenticated")

        token: str = cookie_header[len('Bearer '):]
        username: str = validation_token_from_cookie(token)

        return templates.TemplateResponse("main.html", {"request": request, "username": username})
    except Exception as ex:
        logger.error(f"An error occurred in index method: {ex}")
        raise HTTPException(status_code=500)

