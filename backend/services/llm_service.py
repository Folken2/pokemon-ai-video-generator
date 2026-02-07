"""
LLM Service - Wraps Anthropic Claude API for creative generation steps.
Each pipeline step that needs LLM uses this service with its specific SOP prompt.
"""

from __future__ import annotations

import anthropic

from backend.config import ANTHROPIC_API_KEY, LLM_MODEL, LLM_MAX_TOKENS
from backend.utils.logging_config import logger


class LLMService:
    """Wrapper around Anthropic Claude API for pipeline LLM calls."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.model = model or LLM_MODEL
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not configured. Add it to scripts/.env or environment.")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int | None = None,
        temperature: float = 1.0,
    ) -> str:
        """
        Send a message to Claude and return the text response.

        Args:
            system_prompt: The SOP prompt that defines the role and instructions.
            user_message: The user input (pokemon name, selections, etc.)
            max_tokens: Max response tokens (default from config).
            temperature: Sampling temperature (default 1.0 for creative work).

        Returns:
            The assistant's text response.
        """
        max_tokens = max_tokens or LLM_MAX_TOKENS
        logger.info(f"LLM call: model={self.model}, system_len={len(system_prompt)}, user_len={len(user_message)}")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        # Extract text from response
        text_parts = []
        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)

        result = "\n".join(text_parts)
        logger.info(f"LLM response: {len(result)} chars, stop_reason={response.stop_reason}")
        return result

    def generate_with_continuation(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int | None = None,
        temperature: float = 1.0,
        max_continuations: int = 3,
    ) -> str:
        """
        Generate with automatic continuation if the response is truncated.
        Useful for long outputs like asset manifests and production scripts.
        """
        max_tokens = max_tokens or LLM_MAX_TOKENS
        full_response = ""
        messages = [{"role": "user", "content": user_message}]

        for i in range(max_continuations + 1):
            logger.info(f"LLM call (part {i+1}): model={self.model}")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=messages,
            )

            text_parts = []
            for block in response.content:
                if block.type == "text":
                    text_parts.append(block.text)

            chunk = "\n".join(text_parts)
            full_response += chunk

            if response.stop_reason == "end_turn":
                break

            if response.stop_reason == "max_tokens" and i < max_continuations:
                logger.info("Response truncated, requesting continuation...")
                messages.append({"role": "assistant", "content": chunk})
                messages.append({"role": "user", "content": "Continue from exactly where you left off."})
            else:
                break

        logger.info(f"LLM total response: {len(full_response)} chars")
        return full_response
