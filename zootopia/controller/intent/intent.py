from typing import List
from zootopia.controller.intent.models import (
    Confidence,
    IntentConfig,
    IntentFilters,
    LLMResponseStructure,
)
from zootopia.llm.llm import LLM
from zootopia.core.utils.utils import clean_and_parse_llm_json_output, render_jinja_template


class IntentManager:
    """Detect the intent of a given text data."""

    def __init__(self, llm: LLM, filters: List[IntentFilters]):
        """Initialize the IntentManager."""
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
    def from_config(cls, config: IntentConfig) -> "IntentManager":
        """Create an IntentManager instance from a configuration."""
        llm = LLM.from_config(config.llm_config)
        return cls(llm=llm, filters=config.filters)


    def detect_intent(
        self,
        data: str,
        detect_single: bool = False,
        confidence_threshold: Confidence = Confidence.LOW,
    ) -> List[str]:
        """
        Detects the intent of the given text data and returns a list of intents that
        pass the confidence threshold.
        """
        content = self.llm.generate_response(data).content
        cleaned = clean_and_parse_llm_json_output(content)

        if "error" in cleaned:
            raise ValueError(cleaned["error"])

        def filter_intents(conf_level):
            return [
                intent
                for intent, conf in cleaned["intent"].items()
                if Confidence(conf) == conf_level
            ]

        confidence_levels = {
            Confidence.HIGH: filter_intents(Confidence.HIGH),
            Confidence.MID: filter_intents(Confidence.MID),
            Confidence.LOW: filter_intents(Confidence.LOW),
        }

        result = []
        for level in Confidence:
            if level >= confidence_threshold:
                result.extend(confidence_levels[level])

        if detect_single and result:
            return [result[0]]

        return result
