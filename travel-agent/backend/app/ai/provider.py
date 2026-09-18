import os
from typing import Any, Dict


class BaseLLMProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def call(self, prompt: str, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError()


class DemoLLMProvider(BaseLLMProvider):
    async def call(self, prompt: str, **kwargs):
        # Deterministic demo response
        return {"text": "Demo response", "structured": {}}


def get_provider():
    provider = os.environ.get("LLM_PROVIDER", "groq")
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if os.environ.get("DEMO_MODE", "true").lower() == "true":
        return DemoLLMProvider()
    # TODO: add real providers
    return DemoLLMProvider()
