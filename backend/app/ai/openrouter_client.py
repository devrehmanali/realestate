import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"


class OpenRouterClient:
    """Minimal OpenRouter HTTP client for chat completion requests."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)

        if not self.api_key:
            raise RuntimeError(
                "OpenRouter API key is required. Set OPENROUTER_API_KEY in your environment."
            )

    def chat(self, messages: list[dict[str, str]], temperature: float = 0.7) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        request = Request(
            OPENROUTER_ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=30) as response:
                body = json.load(response)
        except HTTPError as error:
            raise RuntimeError(
                f"OpenRouter request failed: {error.code} {error.reason}"
            ) from error
        except URLError as error:
            raise RuntimeError(f"OpenRouter request failed: {error.reason}") from error

        choices = body.get("choices", [])
        if not choices or not isinstance(choices[0], dict):
            raise RuntimeError("OpenRouter returned an unexpected response.")

        message = choices[0].get("message", {}).get("content", "")
        if not isinstance(message, str):
            raise RuntimeError("OpenRouter response did not include a text message.")

        return message.strip()
