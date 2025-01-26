# FastAPI Chat Application

This is a web-based chat application built with FastAPI, PostgreSQL, and a language model (LLM) backend. The application allows users to sign up, sign in, and chat with an agent powered by either OpenAI or Ollama.

## Features

- **User Authentication**: Users can sign up, log in, and access a chat interface.
- **Chat History**: All messages are stored in the database and can be retrieved by the user.
- **WebSocket Communication**: Real-time chat functionality is implemented via WebSocket.
- **AI-Powered Agent**: A language model (OpenAI or Ollama) generates responses to the user's messages.

## Technologies

- **FastAPI**: For building the web framework.
- **Tortoise ORM**: For interacting with PostgreSQL.
- **PostgreSQL**: Database used for storing user and chat data.
- **WebSocket**: For real-time communication in the chat.
- **LangChain**: For generating AI responses to user messages using Ollama or OpenAI LLMs.

## Requirements

To run the project, you need the following tools installed:

- **Docker**: For running the application and its dependencies in containers.
- **Docker Compose**: For managing multi-container Docker applications.

## Setup and Installation

### Clone the Repository

```bash
git clone https://github.com/shkrobik2017/WebChat.git
cd src
```

### Configure Environment Variables

Create a .env file at the root of the project and configure the settings from env_example file.

### Running the Application with Docker

The project uses Docker to handle dependencies and containerization. To run the application, follow these steps:

1. Build the Docker images:

    ```bash
    docker-compose up --build
    ```

2. If you use Ollama LLM, pull model you chose into image:

    ```bash
    docker exec -it ollama ollama pull llama3.2   
    ```

This will start the application and its dependencies (PostgreSQL, FastAPI) in Docker containers. The application will be available at http://localhost:8000.

## Database Setup

The application uses Tortoise ORM to interact with the PostgreSQL database. When you start the containers for the first time, the database schemas will be generated automatically.

## Application Structure

- **db/**: Contains database models and repository logic using Tortoise ORM.
- **routers/**: Contains FastAPI route handlers for user authentication, chat, and main page.
- **agent/**: Contains the MainAgent class that interacts with either OpenAI or Ollama for generating responses.
- **templates/**: Contains HTML templates.
- **settings.py**: Contains all the configuration variables and environment settings.
- **main.py**: The main entry point for the FastAPI application.
- **docker-compose.yml**: Configuration file for Docker Compose.
- **Dockerfile**: Instructions for building the application Docker image.
- **settings.py**: Contains class Settings to get variables from .env.

## API Endpoints

### Main Page
GET / : Main page with sign in/sign up buttons or chat button if you authorized.

### Sign Up
POST /signup: User registration, requires username and password.
Redirects to the sign-in page if successful.

### Sign In
POST /signin: User login, requires username and password.
Returns an access token stored in a secure cookie.

### Chat
GET /chat: Returns the chat page with chat history for the authenticated user.
Requires authentication via a cookie containing the access token.