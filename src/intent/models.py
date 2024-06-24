from typing import List

from pydantic import BaseModel, Field

from src.langchain.models import LLMConfig


class IntentFilters(BaseModel):
    title: str
    description: str


class IntentConfig(BaseModel):
    llm_config: LLMConfig
    filters: List[IntentFilters]


class LLMResponseStructure(BaseModel):
    intent: dict = Field(
        "{ (dict) A dictionary of intents as keys and their confidence levels "
        "('high', 'medium', 'low') as values. Only include relavent intent keys. "
        "It is possible no intents exist, making this an empty dictionary. }"
    )
