from openai import OpenAI
from .models import Mood, MoodResponse


PROMPT_FOR_MOOD_DETECTION = f"""
    [ ROLE ]: You are a strict mood classifier.

    [ ACTION ]: Read and analyze the entire text carefully and correctly determine its single most dominant mood.

    [ CONTEXT ]: The text may contain various mental states, sentiments or emotions, but you must identify the most prominent one. 
    Concentrate on the tone, intent, wording, and overall meaning.
    Here are the available moods for your reference: {", ".join(m.value for m in Mood)}

    [ EXECUTE ]: 
        Rules:
            - Select EXACTLY ONE mood from the available moods.
            - Do not assume positive or negative sentiment.
            - Base your decision only on the tone and meaning of the text.
            - If multiple moods are present, choose the strongest one.
            - If the mood is unclear, choose "neutral".
            - If you found a mood outside the allowed list, choose "confused".

        Response Format: Return the response strictly in the provided response_format."
"""


class MoodClassifier:
    """Class to determine the mood of a given text using OpenAI's API."""

    def __init__(self, client: OpenAI, model: str, temperature: float = 0.0):
        self.client = client
        self.model = model
        self.temperature = temperature

    def get_mood(self, text: str) -> Mood:
        """Determine the mood of the given text and return the corresponding face representation."""

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": PROMPT_FOR_MOOD_DETECTION},
                {"role": "user", "content": text}
            ],
            response_format=MoodResponse,
            temperature=self.temperature,
        )

        parsed_response = completion.choices[0].message.parsed
        if not parsed_response:
            return Mood.CONFUSED
        
        return parsed_response.mood
    