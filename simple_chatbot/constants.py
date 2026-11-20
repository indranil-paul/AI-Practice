"""
This file contains constants used in the simple chatbot application.
"""
from enum import StrEnum

# Define the filename for storing chat history.
CHAT_HISTORY_DIR_FILENAME = "output/chat_history.txt"

# Define environment variable names for API key and base URL.
ENV_VAR_APIKEY = "OPENROUTER_API_KEY"
ENV_VAR_BASEURL = "OPENROUTER_BASE_URL"

# Define the default model name to be used in the chatbot.
EXIT_COMMANDS = ["exit", "quit", "bye", "goodbye", "stop", "end", "terminate", "close", "finish", "cancel", "abort"]

# Define a message to display when no response is received from the AI.
NO_RESPONSE_MESSAGE = "No response received!"

# Define the user prompt message to display when asking for user input.
USER_PROMPT = "('!') You: "

# Define the system prompt message to display when initializing the chatbot.
SYSTEM_PROMPT = "You are a helpful and friendly assistant."

# Define the AI models available for use in the chatbot.
class AI_MODEL(StrEnum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"

# Define the default model name to be used in the chatbot.
class ROLE(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
