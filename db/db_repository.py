from typing import Union, List, Dict
from db.db_models import UserModel, MessageModel
from routers.user_router.services import get_password_hash


async def get_user(*, username: str) -> Union[UserModel, None]:
    """
    Retrieve a user by their username.

    Args:
        username (str): The username to search for.

    Returns:
        Union[UserModel, None]: The user if found, otherwise None.
    """
    return await UserModel.get_or_none(username=username)


async def create_user(*, username: str, password: str) -> None:
    """
    Create a new user and store them in the database with a hashed password.

    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.

    Returns:
        None: This function does not return anything.
    """
    hashed_pass = get_password_hash(password)
    await UserModel.create(
        username=username, hashed_password=hashed_pass
    )


async def get_chat_history(*, user: UserModel) -> List[MessageModel]:
    """
    Retrieve the chat history for a given user.

    Args:
        user (UserModel): The user whose chat history is to be fetched.

    Returns:
        List[MessageModel]: A list of messages associated with the user.
    """
    if user:
        return await MessageModel.filter(user=user)


async def save_message_to_db(*, user: UserModel, message: Dict[str, str]) -> None:
    """
    Save a new message to the database.

    Args:
        user (UserModel): The user who sent the message.
        message (Dict[str, str]): The message data to be saved, containing "content" and "role".

    Returns:
        None: This function does not return anything.
    """
    if user:
        await MessageModel.create(
            user=user,
            content=message["content"],
            role=message["role"]
        )