import json
import httpx
from typing import List, Dict
from app.ai.base import AIProvider
from app.core.config import settings
from app.core.logging import logger


class AnthropicProvider(AIProvider):
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.AI_API_KEY
        self.model = model or settings.AI_MODEL or "claude-3-5-sonnet-20241022"
        self.endpoint = "https://api.anthropic.com/v1/messages"

    def complete(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        json_mode: bool = False,
        timeout_seconds: int = 15,
    ) -> str:
        if not self.api_key:
            raise ValueError("Anthropic API key is missing. Set AI_API_KEY or use AI_PROVIDER=mock.")

        payload = {
            "model": self.model,
            "system": system_prompt,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.2,
        }

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        last_err = None
        for attempt in range(2):
            try:
                with httpx.Client(timeout=timeout_seconds) as client:
                    resp = client.post(self.endpoint, json=payload, headers=headers)
                    resp.raise_for_status()
                    data = resp.json()
                    return data["content"][0]["text"]
            except Exception as e:
                last_err = e
                logger.warning(f"Anthropic call attempt {attempt+1} failed: {e}")

        raise last_err
