from typing import List, Tuple
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from logger.logger import logger
from settings import settings


class MainAgent:
    def __init__(self) -> None:
        """
        Initialize the agent by selecting the appropriate model based on settings.

        If the `LLM_NAME` setting is 'ollama', use the ChatOllama model;
        otherwise, use the ChatOpenAI model.
        """
        self.model = (
            ChatOllama(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_URL,
            )
            if settings.LLM_NAME == "ollama"
            else ChatOpenAI(
                model_name=settings.OPENAI_MODEL,
                openai_api_key=settings.OPENAI_API_KEY,
            )
        )
        self.role_description_file: str = "agent_role.md"
        self.prompt_template = self._load_agent_role

    @staticmethod
    async def _load_agent_role() -> str:
        """
        Load the agent role description from the `agent_role.md` file.

        Returns:
            str: The contents of the agent role description file.
        """
        with open("agent/agent_role.md", "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def messages_to_prompt(chat_history: List[Tuple[str, str]]) -> List[BaseMessage]:
        """
        Convert the chat history into the appropriate messages for the prompt.

        Args:
            chat_history (List[Tuple[str, str]]): A list of chat messages where each tuple contains
                                                  a role ('user', 'agent', or 'system') and the message content.

        Returns:
            List[BaseMessage]: A list of formatted messages for the LLM prompt.

        Raises:
            ValueError: If an unknown role is encountered in the chat history.
        """
        role_message_map = {
            "user": HumanMessage,
            "agent": AIMessage,
            "system": SystemMessage,
        }
        try:
            return [
                role_message_map[item[0].lower()](item[1])
                for item in chat_history
            ]
        except KeyError as e:
            raise ValueError(f"Unknown role: {e}")

    async def generate_response(
        self,
        *,
        chat_history: List[Tuple[str, str]],
    ) -> str:
        """
        Generate a response from the model based on the provided chat history.

        Args:
            chat_history (List[Tuple[str, str]]): The conversation history used to generate the response.

        Returns:
            str: The model's generated response based on the chat history.
        """
        logger.info("Generating LLM answer process is started")

        prompt: str = await self.prompt_template()
        new_chat_history = self.messages_to_prompt(chat_history)

        messages = [SystemMessage(prompt)] + new_chat_history

        result = await self.model.ainvoke(messages)

        logger.info("LLM answer generated successfully")
        return result.content
