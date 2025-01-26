from typing import Union, List, Dict
from db.db_models import UserModel, MessageModel
from logger.logger import logger


async def get_user(*, username: str) -> Union[UserModel, None]:
    """
    Retrieve a user by their username.

    Args:
        username (str): The username to search for.

    Returns:
        Union[UserModel, None]: The user if found, otherwise None.
    """
    try:
        return await UserModel.get_or_none(username=username)
    except Exception as ex:
        logger.error(f"An error occurred in getting user from db: {ex}")
        raise ex


async def create_user(*, username: str, hashed_pass: str) -> None:
    """
    Create a new user and store them in the database with a hashed password.

    Args:
        username (str): The username of the new user.
        hashed_pass (str): The hashed password of the new user.

    Returns:
        None: This function does not return anything.
    """
    try:
        await UserModel.create(
            username=username, hashed_password=hashed_pass
        )
        logger.info(f"User {username} created successfully")
    except Exception as ex:
        logger.error(f"An error occurred in creating user method: {ex}")
        raise ex


async def get_chat_history(*, user: UserModel) -> List[MessageModel]:
    """
    Retrieve the chat history for a given user.

    Args:
        user (UserModel): The user whose chat history is to be fetched.

    Returns:
        List[MessageModel]: A list of messages associated with the user.
    """
    try:
        if user:
            return await MessageModel.filter(user=user)
        logger.error(f"User {user.username} didn't found")
    except Exception as ex:
        logger.error(f"An error occurred in getting chat history method: {ex}")
        raise ex


async def save_message_to_db(*, user: UserModel, message: Dict[str, str]) -> None:
    """
    Save a new message to the database.

    Args:
        user (UserModel): The user who sent the message.
        message (Dict[str, str]): The message data to be saved, containing "content" and "role".

    Returns:
        None: This function does not return anything.
    """
    try:
        if user:
            await MessageModel.create(
                user=user,
                content=message["content"],
                role=message["role"]
            )
            logger.info(f"Message saved to db successfully: {message}")
    except Exception as ex:
        logger.error(f"An error occurred in saving message to db method: {ex}")
        raise ex
