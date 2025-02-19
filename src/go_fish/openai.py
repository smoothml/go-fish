import json

from loguru import logger
from openai import OpenAI

from go_fish.settings import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.api_key, base_url=str(settings.base_url))


def make_request(prompt: str, model: str = "gpt-4o-2024-08-06", temperature: float = 0.7) -> str:
    """Make a request to the OpenAI API.

    Args:
        prompt: The prompt to send to the API.
        model: The model to use for the request (defaults to GPT-4o).
        temperature: The temperature to use for the request (defaults to 0.7).

    Returns:
        The API response.
    """
    args = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model,
    }
    if not model.startswith("o1") and not model.startswith("o3"):
        args["temperature"] = temperature
    else:
        logger.info("Using a reasoning model, ignoring temperature setting.")

    try:
        response = client.chat.completions.create(**args)
        logger.debug(json.dumps({"response": response.model_dump(mode="json")}))
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error making request to OpenAI: {e}")
        return ""
