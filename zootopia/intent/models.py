from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from zootopia.langchain.models import LLMConfig


class Confidence(Enum):
    LOW = "low"
    MID = "medium"
    HIGH = "high"

    def __ge__(self, other):
        order = [Confidence.LOW, Confidence.MID, Confidence.HIGH]
        return order.index(self) >= order.index(other)


class IntentFilters(BaseModel):
    title: str
    description: str


class IntentConfig(BaseModel):
    llm_config: LLMConfig
    filters: List[IntentFilters]


class LLMResponseStructure(BaseModel):
    intent: dict = Field(
        "{ (dict) A dictionary of intents as keys and their confidence levels "
        f"('{Confidence.LOW.value}', '{Confidence.MID.value}', '{Confidence.HIGH.value}') as values. "
        "Only include relavent intent keys. "
        "It is possible no intents exist, making this an empty dictionary. }"
    )
