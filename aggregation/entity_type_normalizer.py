from typing import List

from ollama import Message

from llm.llm_gateway import LLMGateway
from models import EntityType, EntityTypes


class EntityTypeNormalizer:
    def __init__(self, llm: LLMGateway):
        self.llm = llm

    def normalize(self, entity_types: List[EntityType]) -> EntityTypes:
        prompt = [
            Message(role="user", content=f"""
The following is a list of entity types extracted from various input text:

{"\n".join([f"{entity_type.label}: {entity_type.description}" for entity_type in entity_types])}

Normalize this list, removing similar items, and ensuring every entry is lowercase, words separated by spaces, without any punctuation like _ or -.
"""),
        ]
        return self.llm.generate_object(prompt, EntityTypes, temperature=0.5)
