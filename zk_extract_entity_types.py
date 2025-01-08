import os
from typing import List
from urllib.parse import quote

from rdflib import Literal
from rdflib.namespace import RDFS

from agents.entity_types_extractor import EntityTypesExtractorAgent
from aggregation.entity_type_normalizer import EntityTypeNormalizer
from chroma_gateway import ChromaGateway
from graph.extractor import EntityTypeExtractor, EntityRelationshipExtractor
from graph.rdf import ns_entitytypes, ns_chunks, ns_relationships, ns_documents
from graph.type_matcher import EntityTypeMatcher
from graph_gateway import GraphGateway
from llm.adapters import OpenAIAdapter
from llm.llm_gateway import LLMGateway
from models import EntityType
from app.settings import vault_root, available_llms
from zettelkasten import Zettelkasten

from utility.logger import log

chroma = ChromaGateway()
zk = Zettelkasten(vault_root, chroma)

types_extractor_agent = EntityTypesExtractorAgent.start(available_llms, zk)

# Maybe this should be a specialized agent, a place to put all
# type registry behaviours, except for the query methods
class TypeRegistry:
    def __init__(self):
        self.types: dict[str, EntityType] = {}

    def exists(self, type: EntityType) -> bool:
        return type.label in self.types

    def add(self, type: EntityType):
        if not self.exists(type):
            self.types[type.label] = type

    def add_all(self, types: List[EntityType]):
        for type in types:
            self.add(type)

    def get(self, label: str) -> EntityType:
        return self.types.get(label)

    def labels(self):
        return self.types.keys()

    def size(self):
        return len(self.types)


type_registry = TypeRegistry()

matches = zk.all_chunks()
for i, match in enumerate(matches):
    log.info("Evaluating chunk", num=i, total=len(matches), id=match.id, document_id=match.document_id,
             document_title=match.document_title,
             accumulated_types=type_registry.size())
    types_extractor_agent.tell({
        'chunk_id': match.id,
        'callback': lambda extracted_types: type_registry.add_all(extracted_types.list)
    })

print("Awaiting stop")
types_extractor_agent.stop()
print("Stopped")

# normalizer = EntityTypeNormalizer(llm)
# refined_types = normalizer.normalize(list(types.values()))
#
# all_labels = [type.label for type in refined_types.list]
#
# graph: GraphGateway = GraphGateway.load_or_create('zksv.ttl')
#
# graph.bind("entitytypes", ns_entitytypes)
# graph.bind("chunks", ns_chunks)
# graph.bind("relationships", ns_relationships)
# graph.bind("documents", ns_documents)
# graph.bind("rdfs", RDFS)
#
# ns_relationships_extracted_from = ns_relationships.extracted_from
# ns_relationships_referenced_by = ns_relationships.referenced_by
#
# for match in matches:
#
#     subject = ns_chunks.term(match.id)
#     predicate = ns_relationships_extracted_from
#     object = ns_documents.term(match.document_id)
#     graph.add((subject, predicate, object))
#     graph.add((object, RDFS.label, Literal(match.document_title)))
#
#     rematched_types = EntityTypeMatcher(llm).match(refined_types, match.text)
#     for type in rematched_types.list:
#         if type.label not in all_labels:
#             refined_types.list.append(type)
#             print(f"    {type.label} **** it made this one up")
#         else:
#             print(f"    {type.label}")
#         graph.add((ns_entitytypes.term(quote(type.label)), ns_relationships_extracted_from, subject))
#         graph.add((ns_entitytypes.term(quote(type.label)), RDFS.label, Literal(type.label)))
#
# with open("types.csv", "w") as f:
#     f.write("Label, Description, Examples\n")
#     for type in refined_types.list:
#         examples = ', '.join(type.examples)
#         f.write(f"\"{type.label}\",\"{type.description}\",\"{examples}\"\n")
#
# graph.save()

# all_entities = set()
# all_relationships = set()
# for match in matches:
#     relationships = relationship_extractor.extract_object(entity_types=list(types), text=match.chunk.text)
#     all_entities.update([r.source_entity for r in relationships.list])
#     all_entities.update([r.target_entity for r in relationships.list])
#     all_relationships.update(relationships.list)
#     for relationship in relationships.list:
#         print(f"{relationship.source_entity.entity_name} ({relationship.source_entity.entity_type}) -> {relationship.target_entity.entity_name} ({relationship.target_entity.entity_type}): {relationship.relationship_description}")
#
#
# print(f"Identified {len(all_entities)} entities and {len(all_relationships)} relationships")
