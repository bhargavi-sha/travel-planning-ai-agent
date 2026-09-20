import os
import json
from typing import Any, Dict
import httpx


class BaseLLMProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def call(self, prompt: str, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError()


class DemoLLMProvider(BaseLLMProvider):
    async def call(self, prompt: str, **kwargs):
        # Deterministic demo response
        return {"text": "Demo response", "structured": {}}


class OpenAICompatibleProvider(BaseLLMProvider):
    """Small client for OpenAI and Groq's compatible chat-completions APIs."""

    def __init__(self, api_key: str, base_url: str, model: str):
        super().__init__(api_key)
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def call(self, prompt: str, **kwargs) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "temperature": kwargs.get("temperature", 0.7),
            "messages": [
                {"role": "system", "content": "You are a careful travel planner. Return only valid JSON when requested."},
                {"role": "user", "content": prompt},
            ],
        }
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"]
        return {"text": text, "structured": _extract_json(text)}


def _extract_json(text: str) -> Dict[str, Any]:
    """Accept bare JSON or JSON wrapped in a Markdown code block."""
    clean = text.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    try:
        parsed = json.loads(clean)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def get_provider():
    provider = os.environ.get("LLM_PROVIDER", "groq").lower()
    if os.environ.get("DEMO_MODE", "true").lower() == "true":
        return DemoLLMProvider()
    if provider == "openai" and os.environ.get("OPENAI_API_KEY"):
        return OpenAICompatibleProvider(
            os.environ["OPENAI_API_KEY"],
            os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        )
    if provider == "groq" and os.environ.get("GROQ_API_KEY"):
        return OpenAICompatibleProvider(
            os.environ["GROQ_API_KEY"],
            os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
            os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
        )
    return DemoLLMProvider()
