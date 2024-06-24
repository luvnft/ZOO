from typing import Dict, List, Optional, Type, Union

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.langchain.models import ImitateChat, LLMConfig, LLMProviders


class LLM:
    """Class for Large Language Models (LLMs) usage powered by LangChain"""

    def __init__(
        self,
        llm: Union[ChatOpenAI, ChatAnthropic, ChatGoogleGenerativeAI, ChatGroq],
        system_prompt: str = None,
        structured_output: Optional[Union[Dict, Type[BaseModel]]] = None,
    ) -> None:
        """Initialize LLM with specified model, system prompt, and structured_output."""
        self.llm = llm
        self.system_prompt = system_prompt
        self.structured_output = structured_output

    @classmethod
    def from_config(cls, config: LLMConfig) -> "LLM":
        """Create an LLM instance from a configuration object."""
        name = config.name.value
        match config.provider:
            case LLMProviders.OPENAI:
                llm = ChatOpenAI(model=name)
            case LLMProviders.ANTHROPIC:
                llm = ChatAnthropic(model_name=name)
            case LLMProviders.GOOGLE:
                llm = ChatGoogleGenerativeAI(model=name)
            case LLMProviders.GROQ:
                llm = ChatGroq(model=name)
            case _:
                raise ValueError(f"Unsupported LLM provider: {config.provider}")

        return cls(
            llm=llm,
            system_prompt=config.system_prompt,
            structured_output=config.structured_output,
        )

    def _organize_query(
        self, query: Union[str, List[BaseMessage]]
    ) -> List[BaseMessage]:
        """Organize query into a list of BaseMessage objects (incl. system_prompt)."""

        messages = (
            [SystemMessage(content=self.system_prompt)] if self.system_prompt else []
        )

        if isinstance(query, str):
            messages.append(query)
        elif isinstance(query, list):
            if not all(isinstance(item, BaseMessage) for item in query):
                raise TypeError("Query list must contain only BaseMessage objects")
            messages.extend(query)
        else:
            raise TypeError("Query must be a string or a list of BaseMessage objects")

        return messages

    def generate_response(self, query: Union[str, List[BaseMessage]]) -> AIMessage:
        """Generate an AI response from the LLM given a query."""
        messages = self._organize_query(query)

        if self.structured_output:
            return self.llm.with_structured_output(self.structured_output).invoke(
                messages
            )

        return self.llm.invoke(messages)

    @staticmethod
    def imitate_chat(chat: List[ImitateChat]) -> List[Union[AIMessage, HumanMessage]]:
        """Converts ImitateChat list to AIMessage and HumanMessage list."""
        return [
            (
                AIMessage(content=message.message)
                if message.is_llm
                else HumanMessage(content=message.message)
            )
            for message in chat
        ]
