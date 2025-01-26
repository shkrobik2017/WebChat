import json
from typing import Dict, List, Optional, Any, Tuple
from fastapi import (
    APIRouter,
    Request,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from agent.main_agent import MainAgent
from db.db_repository import get_user, get_chat_history, save_message_to_db
from routers.services import validation_token_from_cookie, get_token_from_cookie_ws, get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

user_connections: Dict[str, WebSocket] = {}


@router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request) -> HTMLResponse:
    """
    Render the chat page with chat history for an authenticated user.

    Args:
        request (Request): The request object.

    Returns:
        HTMLResponse: The rendered HTML page with chat history.
    """
    cookie_header: Optional[str] = request.cookies.get("access_token")
    if not cookie_header or not cookie_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token: str = cookie_header[len("Bearer "):]
    username: str = validation_token_from_cookie(token)

    user = await get_user(username=username)
    messages = await get_chat_history(user=user)
    message_data: List[Dict[str, Any]] = [
        {
            "user": message.user.username,
            "content": message.content,
            "role": message.role,
            "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for message in messages
    ]
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "username": username,
        "messages": message_data
    })


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Handle WebSocket connections for real-time chat.

    Args:
        websocket (WebSocket): The WebSocket connection object.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    cookies: Dict[bytes, bytes] = dict(websocket.scope.get("headers", []))
    token: Optional[str] = await get_token_from_cookie_ws(cookies)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_user = await get_current_user(token=token)
    await websocket.accept()

    user_connections[current_user.username] = websocket
    try:
        while True:
            json_user_message: str = await websocket.receive_text()
            user_message: Dict[str, str] = json.loads(json_user_message)

            await save_message_to_db(user=current_user, message=user_message)

            chat_history: List[Tuple[str, str]] = [
                (item.role, item.content)
                for item in await get_chat_history(user=current_user)
            ]

            agent = MainAgent()
            llm_response: str = await agent.generate_response(
                chat_history=chat_history
            )

            llm_message = {"content": llm_response, "role": "Agent"}
            await save_message_to_db(user=current_user, message=llm_message)

            await websocket.send_text(llm_response)

    except WebSocketDisconnect:
        user_connections.pop(current_user.username, None)
