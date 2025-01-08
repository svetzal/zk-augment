import hashlib
import os
import re
from typing import List

from pydantic import BaseModel, Field


class ZkDocument(BaseModel):
    relative_path: str
    metadata: dict
    content: str

    @property
    def title(self) -> str:
        return self.strip_identifier_prefix(self.base_filename_without_extension())

    @property
    def context_date(self):
        if "published_on" in self.metadata:
            return self.metadata.get("published_on")
        elif "updated_on" in self.metadata:
            return self.metadata.get("updated_on")
        elif "created_on" in self.metadata:
            return self.metadata.get("created_on")
        else:
            return "Unknown"

    @property
    def author(self):
        return self.metadata.get("author", "Unknown")

    @property
    def id(self) -> str:
        return hashlib.md5(bytes(self.relative_path, 'utf-8')).hexdigest()

    def strip_identifier_prefix(self, string):
        return re.sub(r'^[@!]\s*', '', string)

    def base_filename_without_extension(self):
        return os.path.splitext(os.path.basename(self.relative_path))[0]


class ZkDocumentChunk(BaseModel):
    id: str
    document_id: str
    document_title: str
    text: str


class ZkQueryResult(BaseModel):
    chunk: ZkDocumentChunk
    distance: float

class EntityType(BaseModel):
    label: str = Field(..., description="A label for this type of entity, in singular form, and in lower case.")
    description: str = Field(..., description="A comprehensive description of the entity type.")
    examples: List[str] = Field(..., description="A list of examples of entities that fall under this type.")

class EntityTypes(BaseModel):
    list: List[EntityType] = Field(..., description="List of entity types, like people, events, concepts, etc.")


class Entity(BaseModel):
    entity_name: str = Field(..., description="Name of the entity, capitalized")
    entity_type: str = Field(..., description="Type of the entity, a best-match from the provided list of types.")
    entity_description: str = Field(...,
                                    description="Comprehensive description of the entity's attributes and activities.")

    class Config:
        frozen=True


class EntityRelationship(BaseModel):
    source_entity: Entity = Field(..., description="The entity that is the source of the relationship.")
    target_entity: Entity = Field(..., description="The entity that is the target of the relationship.")
    relationship_description: str = Field(...,
                                          description="Explanation as to why the source entity and the target entity are related to each other.")
    relationship_strength: int = Field(...,
                                       description="An integer score between 1 to 10, indicating strength of the relationship between the source entity and target entity.")

    class Config:
        frozen=True

class EntityRelationshipList(BaseModel):
    list: List[EntityRelationship] = Field(...,
                                           description="List of entity relationships, each containing source entity, target entity, relationship description, and relationship strength.")
