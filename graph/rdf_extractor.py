from typing import List

from ollama import Message
from pydantic import BaseModel

from llm.llm_gateway import LLMGateway


class Subject(BaseModel):
    label: str

class Predicate(BaseModel):
    label: str

class Object(BaseModel):
    label: str

class Triple(BaseModel):
    subject: Subject
    predicate: Predicate
    object: Object

class TripleExtractor:
    def __init__(self, llm: LLMGateway):
        self.llm = llm

    def extract_object(self, triples: List[Triple], text: str):
        existing_triples = "\n".join([f"[{t.subject.label} -> {t.predicate.label} -> {t.object.label}]" for t in triples])
        prompt = f"""
        The goal is to study the connections and relations between entities and their features in order to understand all available information from the text.
        Do this in an RDF subject, predicate, object format.
        Reuse existing subjects and predicates when possible.
        Avoid general subjects or objects such as "other" or "unknown".
        This is VERY IMPORTANT: Do not generate redundant or overlapping subjects. For example, if the text contains "company" and "organization" subjects, you should return only one of them.
        Use the is_a predicate to describe the type of entity.
        Use the label predicate to describe the name of the entity.
        Create predicates as needed to describe the relationships between entities.
        Output only RDF triples in the provided format, one per line. The format is [subject_label -> predicate_label -> object_label]. There is no need to specify label predicates.
        
        Existing triples:
        [Stacey Vetzal -> is_a -> Person]
        [Scrum -> is_a -> Agile Framework]
        [Scrum Alliance -> is_a -> Organization]
        [Kanban -> is_a -> Agile Framework]
        [Dave Snowden -> is_a -> Person]
        [Dave Snowden -> created -> Cynefin Framework]
        [Dave Thomas -> is_a -> Person]
        [Agile Manifesto -> is_a -> Document]
        [Dave Thomas -> co_authored -> Agile Manifesto]
        {existing_triples}
        
        Input text:
        {text} 

        Output triples:
        """
        return self.llm.generate_text(messages=[Message(role="user", content=prompt)], temperature=0.5, num_ctx=32768)