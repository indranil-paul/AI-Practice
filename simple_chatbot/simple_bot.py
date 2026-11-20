from datetime import datetime
import os
from .constants import AI_MODEL, ROLE, EXIT_COMMANDS, NO_RESPONSE_MESSAGE, USER_PROMPT, SYSTEM_PROMPT, ENV_VAR_APIKEY, ENV_VAR_BASEURL, CHAT_HISTORY_DIR_FILENAME
from dotenv import load_dotenv
from mood_engine.mood_engine import MoodClassifier
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import List, cast


class SimpleChatbot:
    """
    Command-line chatbot using OpenRouter/OpenAI-compatible API.
    Usage:
    - Run the script and start chatting with the bot.
    - Type exit commands (e.g., "exit", "quit") to end the conversation.
        The bot uses a mood classifier to analyze the tone of its responses and displays an appropriate face representation.
    - Make sure to set your OPENROUTER_API_KEY and OPENROUTER_BASE_URL in the environment variables or pass them as arguments when initializing the bot.
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None, temperature: float = 0.7, store_history: bool = True):
        # Load environment variables from .env file if available
        load_dotenv()

        self._api_key = os.environ.get(ENV_VAR_APIKEY, api_key)
        self._base_url = os.environ.get(ENV_VAR_BASEURL, base_url)
        self._bot_temperature = temperature
        self._store_history = store_history
        
        if not self._api_key:
            raise ValueError("API key is missing!")

        if not self._base_url:
            raise ValueError("Base URL is missing!")

        self.client = OpenAI(api_key=self._api_key, base_url=self._base_url)
        if not self.client:
            raise ValueError("Failed to initialize OpenAI client!")
        
        self.mood_classifier = MoodClassifier(client=self.client, model=AI_MODEL.GPT_4O_MINI)

        self.messages: List[ChatCompletionMessageParam] = []
        self._add_message(ROLE.SYSTEM, SYSTEM_PROMPT)


    def __del__(self):
        """Ensure the OpenAI client is closed when the chatbot instance is deleted."""
        self.messages.clear()
        if hasattr(self, 'client') and self.client:
            self.client.close()


    def _format_response(self, text: str) -> str:
        """Format the AI response by analyzing its mood and adding a corresponding face representation."""
        mood = self.mood_classifier.get_mood(text)
        border = "-" * 100
        return f"{border}\n[{mood.value}] {mood.face} AI: \n\n{text}\n{border}"
    
    
    def _add_message(self, role: ROLE, content: str):
        """Add a message to the conversation history."""
        message = cast(ChatCompletionMessageParam, {"role": role, "content": content})
        self.messages.append(message)


    def _store_chat_history(self):
        """Store the chat history to a file."""
        try:
            with open(CHAT_HISTORY_DIR_FILENAME, "w", encoding="utf-8") as f:
                f.write("=" * 100 + "\n")
                f.write(f"Chat History [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
                f.write("=" * 100 + "\n")
                for message in self.messages:
                    f.write(f"\n[{message.get('role').upper()}]:- {message.get('content')}\n")
        except Exception as e:
            print(f"Failed to save chat history: {e}")
        
    
    def _get_ai_response(self, prompt: str) -> str | None:
        """Send the user prompt to the AI and get the response, while also updating the conversation history."""
        try:
            self._add_message(ROLE.USER, prompt)
            response = self.client.chat.completions.create(
                model=AI_MODEL.GPT_4O_MINI,
                messages=self.messages,
                temperature=self._bot_temperature,
            )
            ai_message = response.choices[0].message.content if response.choices else None

            if ai_message:
                self._add_message(ROLE.ASSISTANT, ai_message)

            return ai_message
        except RuntimeError:
            raise


    def _exit_chat(self) -> None:
        """ Exit from chatbot."""
        ai_message = self._get_ai_response("Goodbye!")
        print(self._format_response(ai_message) if ai_message else NO_RESPONSE_MESSAGE)
        
        if self._store_history:
            self._store_chat_history()

        print("\n~~~~~[ SIMPLE CHATBOT IS CLOSED ]~~~~~\n")


    def run(self):
        """Start the chatbot conversation loop."""
        print("\n~~~~~[ SIMPLE CHATBOT IS ON ]~~~~~\n")

        while True:
            user_message = input(USER_PROMPT)
            if not user_message.strip():
                continue

            if user_message.lower() in EXIT_COMMANDS:
                self._exit_chat()
                break

            ai_message = self._get_ai_response(user_message)
            print(self._format_response(ai_message) if ai_message else NO_RESPONSE_MESSAGE)


def main():
    try:
        bot = SimpleChatbot(store_history=True)
        bot.run()
    except Exception as e:
        print(f"\n[ERROR]: {e}")


if __name__ == "__main__":
    main()
