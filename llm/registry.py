from enum import Enum

from pydantic import BaseModel

from llm.adapters import LLMProviderAdapter


class LLMSizeEnum(str, Enum):
    tiny = 'tiny'
    small = "small"
    medium = 'medium'
    large = 'large'
    giant = 'giant'


class LLMTypeEnum(str, Enum):
    instruct = 'instruct'
    chat = 'chat'


class LLMCapabilities(BaseModel):
    size: LLMSizeEnum
    type: LLMTypeEnum

    @property
    def supports_tools(self) -> bool:
        return self.type == LLMTypeEnum.chat

    def supports_structured_output(self) -> bool:
        return self.type == LLMTypeEnum.instruct


class LLMRegistryEntry:
    def __init__(self, name: str, capabilities: LLMCapabilities, adapter: LLMProviderAdapter):
        self.name = name
        self.capabilities = capabilities
        self.adapter = adapter


class LLMRegistry:
    def __init__(self):
        self.llms = []

    def register(self, entry: LLMRegistryEntry):
        self.llms.append(entry)

    def find_first(self, capabilities: LLMCapabilities) -> LLMRegistryEntry:
        return next((llm for llm in self.llms if llm.capabilities == capabilities), None)

    def model_name_matching(self, capabilities: LLMCapabilities) -> str:
        entry = self.find_first(capabilities)
        if entry is None:
            raise ValueError(f"No LLM found for requested capabilities {capabilities}")
        return entry.name
