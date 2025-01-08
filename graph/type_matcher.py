from ollama import Message

from llm.llm_gateway import LLMGateway
from models import EntityTypes


class EntityTypeMatcher:
    def __init__(self, llm: LLMGateway):
        self.llm = llm

    def match(self, available_types: EntityTypes, text: str) -> EntityTypes:
        prompt = [Message(role="user", content=f"""
Your task is to list any of the defined entity types that are present in the input text.
If there are no entity types present in the input text, you should respond with "No entity types found in the input text.".

AVAILABLE ENTITY TYPES
{"\n".join(f"\"{type.label}\": \"{type.description}\"" for type in available_types.list)}

INPUT TEXT:
{text}

MATCHED ENTITY TYPES:
""")]
        return self.llm.generate_object(prompt, EntityTypes, temperature=0.5)
