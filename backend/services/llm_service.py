"""
LLM Service - Wraps OpenRouter API (OpenAI-compatible) for creative generation steps.
Each pipeline step that needs LLM uses this service with its specific SOP prompt.
"""

from __future__ import annotations

from openai import OpenAI

from backend.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL, LLM_MAX_TOKENS
from backend.utils.logging_config import logger


class LLMService:
    """Wrapper around OpenRouter API for pipeline LLM calls."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.model = model or LLM_MODEL
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not configured. Add it to scripts/.env or environment.")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": "https://github.com/Folken2/pokemon-ai-video-generator",
                "X-Title": "AI Documentary Pipeline",
            },
        )

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int | None = None,
        temperature: float = 1.0,
        plugins: list[dict] | None = None,
    ) -> str:
        """
        Send a message to the LLM and return the text response.

        Args:
            system_prompt: The SOP prompt that defines the role and instructions.
            user_message: The user input (pokemon name, selections, etc.)
            max_tokens: Max response tokens (default from config).
            temperature: Sampling temperature (default 1.0 for creative work).
            plugins: Optional OpenRouter plugins (e.g. [{"id": "web", "max_results": 5}]).

        Returns:
            The assistant's text response.
        """
        max_tokens = max_tokens or LLM_MAX_TOKENS
        logger.info(f"LLM call: model={self.model}, system_len={len(system_prompt)}, user_len={len(user_message)}")

        kwargs = dict(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        if plugins:
            kwargs["extra_body"] = {"plugins": plugins}

        response = self.client.chat.completions.create(**kwargs)

        result = response.choices[0].message.content or ""
        logger.info(f"LLM response: {len(result)} chars, finish_reason={response.choices[0].finish_reason}")
        return result

    def generate_with_continuation(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int | None = None,
        temperature: float = 1.0,
        max_continuations: int = 3,
        plugins: list[dict] | None = None,
    ) -> str:
        """
        Generate with automatic continuation if the response is truncated.
        Useful for long outputs like asset manifests and production scripts.
        Plugins (e.g. web search) are only applied to the first call.
        """
        max_tokens = max_tokens or LLM_MAX_TOKENS
        full_response = ""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        for i in range(max_continuations + 1):
            logger.info(f"LLM call (part {i+1}): model={self.model}")

            kwargs = dict(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages,
            )
            # Only apply plugins on the first call (continuations don't need fresh search)
            if plugins and i == 0:
                kwargs["extra_body"] = {"plugins": plugins}

            response = self.client.chat.completions.create(**kwargs)

            chunk = response.choices[0].message.content or ""
            full_response += chunk

            finish_reason = response.choices[0].finish_reason
            if finish_reason == "stop":
                break

            if finish_reason == "length" and i < max_continuations:
                logger.info("Response truncated, requesting continuation...")
                messages.append({"role": "assistant", "content": chunk})
                messages.append({"role": "user", "content": "Continue from exactly where you left off."})
            else:
                break

        logger.info(f"LLM total response: {len(full_response)} chars")
        return full_response
