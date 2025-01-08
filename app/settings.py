import os

from llm.adapters import OllamaAdapter, OpenAIAdapter
from llm.registry import LLMRegistry, LLMRegistryEntry, LLMCapabilities, LLMSizeEnum, LLMTypeEnum

homedir = os.environ['HOME']
# vault_root = f"{homedir}/Documents/ToyVault"
vault_root = f"{homedir}/Documents/HostedVault"
ollama_model = 'llama3.1-instruct-8b-32k'
# ollama_model = 'llama3.3-instruct-70b-32k'

available_llms = LLMRegistry()
available_llms.register(
    LLMRegistryEntry(
        name="llama3.3-70b-32k",
        capabilities=LLMCapabilities(size=LLMSizeEnum.medium, type=LLMTypeEnum.chat),
        adapter=OllamaAdapter()
    )
)
available_llms.register(
    LLMRegistryEntry(
        name="llama3.3-instruct-70b-32k",
        capabilities=LLMCapabilities(size=LLMSizeEnum.medium, type=LLMTypeEnum.instruct),
        adapter = OllamaAdapter()
)
)
available_llms.register(
    LLMRegistryEntry(
        name="llama3.1:8b",
        capabilities=LLMCapabilities(size=LLMSizeEnum.small, type=LLMTypeEnum.chat),
        adapter=OllamaAdapter()
    )
)
available_llms.register(
    LLMRegistryEntry(
        name="llama3.1-instruct-8b-32k",
        capabilities=LLMCapabilities(size=LLMSizeEnum.small, type=LLMTypeEnum.instruct),
        adapter=OllamaAdapter()
    )
)
available_llms.register(
    LLMRegistryEntry(
        name="gpt-4o-mini",
        capabilities=LLMCapabilities(size=LLMSizeEnum.large, type=LLMTypeEnum.chat),
        adapter=OpenAIAdapter(os.environ['OPENAI_ACCESS_TOKEN'])
    )
)