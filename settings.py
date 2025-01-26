from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration class for application settings, loaded from environment variables.
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        frozen = True

    POSTGRES_HOST: str = Field(
        ...,
        description="The hostname of the PostgreSQL database."
    )

    POSTGRES_PORT: int = Field(
        ...,
        description="The port number for connecting to the PostgreSQL database."
    )

    POSTGRES_USER: str = Field(
        ...,
        description="The username for authenticating to the PostgreSQL database."
    )

    POSTGRES_PASSWORD: str = Field(
        ...,
        description="The password for authenticating to the PostgreSQL database."
    )

    POSTGRES_DB: str = Field(
        ...,
        description="The name of the PostgreSQL database to connect to."
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: str = Field(
        ...,
        description="Expiration time for access tokens in minutes."
    )

    AUTH_SECRET_KEY: str = Field(
        ...,
        description="The secret key used for signing authentication tokens."
    )

    AUTH_ALGORITHM: str = Field(
        ...,
        description="The algorithm used for signing authentication tokens."
    )

    LLM_NAME: str = Field(
        ...,
        description="The name of the language model being used (e.g., 'ollama' or 'openai')."
    )

    OPENAI_API_KEY: str = Field(
        ...,
        description="API key for accessing OpenAI services."
    )

    OPENAI_MODEL: str = Field(
        ...,
        description="The model to be used with OpenAI (e.g., 'gpt-3.5')."
    )

    OLLAMA_URL: str = Field(
        ...,
        description="Base URL for the Ollama service."
    )

    OLLAMA_MODEL: str = Field(
        ...,
        description="The model to be used with Ollama."
    )


# Instance of the Settings class, which loads the configuration from the environment.
settings: Settings = Settings()
