from typing import List

from zootopia.intent.models import IntentConfig, IntentFilters, LLMResponseStructure
from zootopia.langchain.llm import LLM
from zootopia.utils.utils import clean_and_parse_llm_json_output, render_jinja_template


class IntentDetector:
    """Detect the intent of a given text data."""

    def __init__(self, llm: LLM, filters: List[IntentFilters]):
        """Initialize the IntentDetector."""
        filters_str = ", ".join(
            f"{value.title.upper()} ({value.description})" for value in filters
        )
        system_prompt = render_jinja_template(
            "intent.jinja",
            "zootopia/intent/templates",
            filters=filters_str,
            response_structure=LLMResponseStructure,
        )
        llm.system_prompt = system_prompt
        self.llm = llm

    @classmethod
    def from_config(cls, config: IntentConfig) -> "IntentDetector":
        """Create an IntentDetector instance from a configuration."""
        llm = LLM.from_config(config.llm_config)
        return cls(llm=llm, filters=config.filters)

    def detect_intent(self, data: str) -> dict:
        """
        Detect the intent of the given text data and return a dictionary of intents
        with confidence scores.
        """
        content = self.llm.generate_response(data).content
        cleaned = clean_and_parse_llm_json_output(content)

        if "error" in cleaned:
            raise ValueError(cleaned["error"])

        return cleaned
