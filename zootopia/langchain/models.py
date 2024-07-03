from enum import Enum
from typing import Dict, Optional, Type, Union

from pydantic import BaseModel


class LLMProviders(Enum):
    """Enumeration of supported Large Language Model (LLM) providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GROQ = "groq"


class LLMNames(Enum):
    """Enumeration of available LLM models."""

    # LLMProviders.OPENAI
    GPT_4O = "gpt-4o"
    GPT_35_TURBO = "gpt-3.5-turbo"

    # LLMProviders.ANTHROPIC
    CLAUDE_OPUS = "claude-3-opus-20240229"
    CLAUDE_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_HAIKU = "claude-3-haiku-20240307"

    # LLMProviders.GOOGLE
    GEMINI_PRO = "gemini-1.5-pro"
    GEMINI_FLASH = "gemini-1.5-flash"

    # LLMProviders.GROQ
    LLAMA3_8B = "llama3-8b-8192"
    LLAMA3_70B = "llama3-70b-8192"
    MIXTRAL = "mixtral-8x7b-32768"
    GEMMA = "gemma-7b-it"


class LLMConfig(BaseModel):
    """Configuration for an LLM instance."""

    provider: LLMProviders
    name: LLMNames
    system_prompt: str = None
    structured_output: Optional[Union[Dict, Type[BaseModel]]] = None


class ImitateChat(BaseModel):
    """Representation of a chat message with LLM indicator."""

    message: str
    is_llm: bool = False
