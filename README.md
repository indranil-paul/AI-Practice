# Simple Chatbot with Mood Detection

A command-line chatbot built on an OpenAI-compatible API (e.g., OpenRouter). After every AI reply, a second LLM call classifies the reply's dominant mood and prints a matching ASCII face next to it.

```
----------------------------------------------------------------------------------------------------
[happy] (^_^) AI:

Hello! How can I help you today?
----------------------------------------------------------------------------------------------------
```

## Features

- Interactive CLI chat loop with full conversation context
- Mood classification of each AI response, with 17 moods and ASCII faces
- Structured output from the mood classifier, validated with Pydantic
- Optional chat history export to a text file on exit
- Configuration through environment variables or a `.env` file
- Several exit commands, such as `exit`, `quit`, and `bye`

## Project Structure

```
AI-Practice/
├── mood_engine/
│   ├── mood_engine.py      # MoodClassifier: LLM-based mood detection
│   └── models.py           # Mood enum (with faces) and MoodResponse model
├── simple_chatbot/
│   ├── simple_bot.py       # SimpleChatbot class and entry point
│   └── constants.py        # Models, roles, prompts, env var names, exit commands
├── output/                 # Chat history is saved here (chat_history.txt)
├── .env                    # API credentials (not committed)
├── .python-version         # Set by pyenv
├── requirements.txt
└── setup.sh                # One-step environment setup
```

## Prerequisites

- macOS or Linux with [pyenv](https://github.com/pyenv/pyenv) installed
- Python 3.14.5 (installed by `setup.sh`). `StrEnum` requires Python 3.11 or later.
- An API key and base URL for an OpenAI-compatible provider, such as OpenRouter

## Setup

1. Clone the repository and move to the project root:

   ```bash
   cd AI-Practice
   ```

2. Run the setup script. It installs Python via pyenv, creates `.venv`, and installs the requirements:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. Activate the virtual environment (the script can't keep it active in your shell):

   ```bash
   source .venv/bin/activate
   ```

4. Create a `.env` file in the project root:

   ```env
   OPENROUTER_API_KEY=your_api_key_here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```

5. Create the output folder for chat history:

   ```bash
   mkdir -p output
   ```

> **Note:** Never commit `.env`. Make sure it is listed in `.gitignore`.

## Usage

Run the chatbot **from the project root** as a module:

```bash
python -m simple_chatbot.simple_bot
```

Then chat in the terminal. To end the session, type any of these exit commands:

`exit`, `quit`, `bye`, `goodbye`, `stop`, `end`, `terminate`, `close`, `finish`, `cancel`, `abort`

On exit, the bot sends a final "Goodbye!" message to the AI, prints the reply, and saves the conversation to `output/chat_history.txt`.

### Using the class in your own code

```python
from simple_chatbot.simple_bot import SimpleChatbot

bot = SimpleChatbot(temperature=0.7, store_history=True)
bot.run()
```

| Parameter       | Type          | Default | Description                                                       |
|-----------------|---------------|---------|-------------------------------------------------------------------|
| `api_key`       | `str \| None` | `None`  | Fallback API key, used only if the env variable is not set        |
| `base_url`      | `str \| None` | `None`  | Fallback base URL, used only if the env variable is not set       |
| `temperature`   | `float`       | `0.7`   | Sampling temperature for chat responses                           |
| `store_history` | `bool`        | `True`  | Save the conversation to `output/chat_history.txt` on exit        |

## Configuration

| Variable              | Description                                  |
|-----------------------|----------------------------------------------|
| `OPENROUTER_API_KEY`  | API key for your provider (required)         |
| `OPENROUTER_BASE_URL` | Base URL of the OpenAI-compatible API (required) |

Other settings live in `simple_chatbot/constants.py`:

- `AI_MODEL`: available model names (the bot currently uses `GPT_4O_MINI`)
- `SYSTEM_PROMPT`: the chatbot's personality
- `EXIT_COMMANDS`: words that end the chat
- `USER_PROMPT`: the input prompt text
- `CHAT_HISTORY_DIR_FILENAME`: where history is saved

## How It Works

1. `SimpleChatbot` keeps a running list of messages (system, user, assistant) and sends it with each request.
2. After each reply, `MoodClassifier.get_mood()` sends the text to the model using structured output (`MoodResponse`), so the result is always one valid `Mood`.
3. The `Mood` enum maps to an ASCII face, and the response is printed with it.
4. If the mood can't be parsed, the classifier falls back to `confused`.

Because each reply triggers an extra API call for mood detection, expect roughly double the API usage per turn.

## Supported Moods

| Mood          | Face    | Mood          | Face    |
|---------------|---------|---------------|---------|
| `afraid`      | `(o_o)` | `smile`       | `(^.^)` |
| `confused`    | `(?_?)` | `thinking`    | `(o_O)` |
| `cry`         | `(;_;)` | `unimpressed` | `(e_e)` |
| `dizzy`       | `(@_@)` | `very_happy`  | `(^o^)` |
| `error`       | `(>_<)` | `very_tired`  | `(=_=)` |
| `fail`        | `(x_x)` | `wink`        | `(^_~)` |
| `happy`       | `(^_^)` | `wow`         | `(O_O)` |
| `neutral`     | `('_')` | `sad`         | `(T_T)` |
| `sleepy`      | `(-_-)` |               |         |

To add a mood, add it to the `Mood` enum and to the `face` mapping in `mood_engine/models.py`. The classifier prompt picks it up automatically.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'mood_engine'` | Script run from inside `simple_chatbot/`, so the project root isn't on the import path | Run from the project root with `python -m simple_chatbot.simple_bot` |
| `ImportError: attempted relative import with no known parent package` | Running `simple_bot.py` directly breaks the relative import `from .constants import ...` | Use the `-m` form above |
| `[ERROR]: API key is missing!` / `Base URL is missing!` | Environment variables not set | Check your `.env` file and variable names |
| `Failed to save chat history` | The `output/` folder doesn't exist | Run `mkdir -p output` from the project root |

## Notes

- Run commands from the project root, since the history path `output/chat_history.txt` is relative to the working directory.
- If environment variables are set, they take priority over `api_key` and `base_url` passed to the constructor.

## License

Add your license here.