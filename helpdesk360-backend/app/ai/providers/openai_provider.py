import json
import httpx
from typing import List, Dict
from app.ai.base import AIProvider
from app.core.config import settings
from app.core.logging import logger


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.AI_API_KEY
        self.model = model or settings.AI_MODEL or "gpt-4o-mini"
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    def complete(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        json_mode: bool = False,
        timeout_seconds: int = 15,
    ) -> str:
        if not self.api_key:
            raise ValueError("OpenAI API key is missing. Set AI_API_KEY or use AI_PROVIDER=mock.")

        all_messages = [{"role": "system", "content": system_prompt}] + messages
        payload = {
            "model": self.model,
            "messages": all_messages,
            "temperature": 0.2,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # 1 retry on timeout / connection error
        last_err = None
        for attempt in range(2):
            try:
                with httpx.Client(timeout=timeout_seconds) as client:
                    resp = client.post(self.endpoint, json=payload, headers=headers)
                    resp.raise_for_status()
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
            except Exception as e:
                last_err = e
                logger.warning(f"OpenAI call attempt {attempt+1} failed: {e}")

        raise last_err
