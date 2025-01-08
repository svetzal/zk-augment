from typing import List

from ollama import Message

from llm.llm_gateway import LLMGateway
from utility.logger import log
from models import EntityTypes, EntityRelationship, EntityRelationshipList, Entity, EntityType


class EntityTypeExtractor:
    def __init__(self, llm: LLMGateway):
        self.llm = llm

    @property
    def domain(self) -> str:
        return "agile software development"

    @property
    def user_goal(self) -> str:
        return f"""
        Identify the relations and structure of the community of interest, specifically within the {self.domain} domain.
        """

    def extract_object(self, text) -> EntityTypes:
        prompt = f"""
        The goal is to study the connections and relations between the entity types and their features in order to understand all available information from the text.
        The user's goal is to {self.user_goal}.
        As part of the analysis, you want to identify the entity types present in the following text.
        The entity types must be relevant to the user task.
        Avoid general entity types such as "other" or "unknown".
        This is VERY IMPORTANT: Do not generate redundant or overlapping entity types. For example, if the text contains "company" and "organization" entity types, you should return only one of them.
        Don't worry about quantity, always choose quality over quantity. And make sure EVERYTHING in your answer is relevant to the context of entity extraction.
        ---
        EXAMPLE SECTION: The following section includes example output. These examples **must be excluded from your answer**.
        
        EXAMPLE 1
        Task: Determine the connections and organizational hierarchy within the specified community.
        Text: Example_Org_A is a company in Sweden. Example_Org_A's director is Example_Individual_B.
        JSON RESPONSE:
        {EntityTypes(list=[
            EntityType(label="organization", description="A systematic arrangement or structure of people, processes, and resources that work together to achieve a common goal", examples=["Example_Org_A"]),
            EntityType(label="person", description="An individual human being with their own unique characteristics, thoughts, feelings, and experiences, possessing consciousness, identity, and autonomy", examples=["Example_Individual_B"])
        ]).model_dump_json()}
        END OF EXAMPLE 1
        
        EXAMPLE 2
        Task: Identify the key concepts, principles, and arguments shared among different philosophical schools of thought, and trace the historical or ideological influences they have on each other.
        Text: Rationalism, epitomized by thinkers such as René Descartes, holds that reason is the primary source of knowledge. Key concepts within this school include the emphasis on the deductive method of reasoning.
        JSON RESPONSE:
        {EntityTypes(list=[
            EntityType(label="concept", description="An abstract idea or notion that represents a thought, object, or phenomenon, often formed through mental perception, understanding, or imagination, and used to convey meaning, classify information, or explain complex ideas", examples=["deductive method of reasoning"]),
            EntityType(label="person", description="An individual human being with their own unique characteristics, thoughts, feelings, and experiences, possessing consciousness, identity, and autonomy", examples=["René Descartes"]),
            EntityType(label="school of thought", description="a distinct philosophical, theoretical, or ideological perspective that represents a set of principles, beliefs, and values shared by a group of people, guiding their understanding, interpretation, and approach to a particular subject, issue, or discipline.", examples=["rationalism"]),
        ]).model_dump_json()}
        END OF EXAMPLE 2
        
        EXAMPLE 3
        Task: Identify the full range of basic forces, factors, and trends that would indirectly shape an issue.
        Text: Industry leaders such as Panasonic are vying for supremacy in the battery production sector. They are investing heavily in research and development and are exploring new technologies to gain a competitive edge.
        JSON RESPONSE:
        {EntityTypes(list=[
            EntityType(label="organization", description="A systematic arrangement or structure of people, processes, and resources that work together to achieve a common goal", examples=["Panasonic"]),
            EntityType(label="technology", description="The application or use of scientific knowledge for practical purposes, especially in industry, such as machines, devices, or methods that make tasks easier, faster, or more efficient.", examples=["battery"]),
            EntityType(label="sector", description="A specific area of industry", examples=["battery production"]),
            EntityType(label="investment strategy", description="a plan or approach for allocating resources, such as money or time, to achieve specific financial or business goals", examples=["research and development"]),
        ]).model_dump_json()}
        END OF EXAMPLE 3
        END OF EXAMPLE SECTION
        ---
        REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Generate Entity Types only.
        Goal: {self.user_goal}
        Text: {text}
        JSON response:
        """

        return self.llm.generate_object(
            messages=[Message(role="user", content=prompt)],
            response_model=EntityTypes,
            temperature=0.5, num_ctx=32768, num_predict=8192
        )

    def extract_object_with_accumulated_types(self, accumulated_types: List[EntityType], text) -> EntityTypes:
        prompt = f"""
The goal is to study the connections and relations between the entity types and their features in order to understand all available information from the text.
The user's goal is to {self.user_goal}.
As part of the analysis, we are iteratively compiling a list of entity types across a larger dataset.
The following tpes have already been identified:
{", ".join([t.label for t in accumulated_types])}

Only add new types if none of the previous types fit the passage in the text.
The entity types must be relevant to the user task.
Avoid general entity types such as "other" or "unknown".
This is VERY IMPORTANT: Do not generate redundant or overlapping entity types. For example, if the text contains "company" and "organization" entity types, you should return only one of them.
Don't worry about quantity, always choose quality over quantity. And make sure EVERYTHING in your answer is relevant to the context of entity extraction.
---
EXAMPLE SECTION: The following section includes example output. These examples **must be excluded from your answer**.

EXAMPLE 1
Task: Determine the connections and organizational hierarchy within the specified community.
Text: Example_Org_A is a company in Sweden. Example_Org_A's director is Example_Individual_B.
JSON RESPONSE:
{EntityTypes(list=[
    EntityType(label="organization", description="A systematic arrangement or structure of people, processes, and resources that work together to achieve a common goal", examples=["Example_Org_A"]),
    EntityType(label="person", description="An individual human being with their own unique characteristics, thoughts, feelings, and experiences, possessing consciousness, identity, and autonomy", examples=["Example_Individual_B"])
]).model_dump_json()}
END OF EXAMPLE 1

EXAMPLE 2
Task: Identify the key concepts, principles, and arguments shared among different philosophical schools of thought, and trace the historical or ideological influences they have on each other.
Text: Rationalism, epitomized by thinkers such as René Descartes, holds that reason is the primary source of knowledge. Key concepts within this school include the emphasis on the deductive method of reasoning.
JSON RESPONSE:
{EntityTypes(list=[
    EntityType(label="concept", description="An abstract idea or notion that represents a thought, object, or phenomenon, often formed through mental perception, understanding, or imagination, and used to convey meaning, classify information, or explain complex ideas", examples=["deductive method of reasoning"]),
    EntityType(label="person", description="An individual human being with their own unique characteristics, thoughts, feelings, and experiences, possessing consciousness, identity, and autonomy", examples=["René Descartes"]),
    EntityType(label="school of thought", description="a distinct philosophical, theoretical, or ideological perspective that represents a set of principles, beliefs, and values shared by a group of people, guiding their understanding, interpretation, and approach to a particular subject, issue, or discipline.", examples=["rationalism"]),
]).model_dump_json()}
END OF EXAMPLE 2

EXAMPLE 3
Task: Identify the full range of basic forces, factors, and trends that would indirectly shape an issue.
Text: Industry leaders such as Panasonic are vying for supremacy in the battery production sector. They are investing heavily in research and development and are exploring new technologies to gain a competitive edge.
JSON RESPONSE:
{EntityTypes(list=[
    EntityType(label="organization", description="A systematic arrangement or structure of people, processes, and resources that work together to achieve a common goal", examples=["Panasonic"]),
    EntityType(label="technology", description="The application or use of scientific knowledge for practical purposes, especially in industry, such as machines, devices, or methods that make tasks easier, faster, or more efficient.", examples=["battery"]),
    EntityType(label="sector", description="A specific area of industry", examples=["battery production"]),
    EntityType(label="investment strategy", description="a plan or approach for allocating resources, such as money or time, to achieve specific financial or business goals", examples=["research and development"]),
]).model_dump_json()}
END OF EXAMPLE 3
END OF EXAMPLE SECTION
---
REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Add new EntityTypes that are not yet defined.
Goal: {self.user_goal}
EXTRACT NEW ENTITY TYPES FROM THIS INPUT TEXT
{text}
END OF INPUT TEXT
JSON response:
""".strip()

        log.info("Prompt generated", prompt=prompt)

        generated_object = self.llm.generate_object(messages=[Message(role="user", content=prompt)],
                                                    response_model=EntityTypes, temperature=0.5, num_ctx=32768,
                                                    num_predict=8192)

        log.info("Response received", model=self.llm.model, response=generated_object.model_dump())

        return generated_object


class EntityRelationshipExtractor:
    def __init__(self, llm: LLMGateway):
        self.llm = llm

    def extract_object(self, entity_types: List[str], text: str) -> EntityRelationshipList:
        prompt = f"""
        -Goal-
        Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
        
        -Steps-
        1. Identify all entities. For each identified entity, extract the following information:
        - entity_name: Name of the entity, capitalized
        - entity_type: One of the following types: [ {", ".join(entity_types)} ]
        - entity_description: Comprehensive description of the entity's attributes and activities
        
        2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
        For each pair of related entities, extract the following information:
        - source_entity: name of the source entity, as identified in step 1
        - target_entity: name of the target entity, as identified in step 1
        - relationship_description: explanation as to why you think the source entity and the target entity are related to each other
        - relationship_strength: an integer score between 1 to 10, indicating strength of the relationship between the source entity and target entity
        
        ---
        EXAMPLE SECTION: The following section includes example output. These examples **must be excluded from your answer**.
        
        EXAMPLE 1
        Input:
        Entity_types: organization,person
        Text: "The Verdantis's Central Institution is scheduled to meet on Monday and Thursday, with the institution planning to release its latest policy decision on Thursday at 1:30 p.m. PDT, followed by a press conference where Central Institution Chair Martin Smith will take questions. Investors expect the Market Strategy Committee to hold its benchmark interest rate steady in a range of 3.5%-3.75%."
        
        Output:
        {EntityRelationshipList(list=[
            EntityRelationship(
                source_entity=Entity(entity_name="Martin Smith", entity_type="person", entity_description="Martin Smith is the chair of the Central Institution"),
                target_entity=Entity(entity_name="Central Institution", entity_type="organization", entity_description="The Central Institution is the Federal Reserve of Verdantis, which is setting interest rates on Monday and Thursday"),
                relationship_description="Martin Smith is the Chair of the Central Institution and will answer questions at a press conference",
                relationship_strength=9
            )
        ]).model_dump_json()}
        END OF EXAMPLE 1
        
        EXAMPLE 2
        Input:
        Entity_types: organization
        Text: "TechGlobal's (TG) stock skyrocketed in its opening day on the Global Exchange Thursday. But IPO experts warn that the semiconductor corporation's debut on the public markets isn't indicative of how other newly listed companies may perform. TechGlobal, a formerly public company, was taken private by Vision Holdings in 2014. The well-established chip designer says it powers 85% of premium smartphones."

        Output:
        {EntityRelationshipList(list=[
            EntityRelationship(
                source_entity=Entity(entity_name="TechGlobal", entity_type="organization", entity_description="TechGlobal is a stock now listed on the Global Exchange which powers 85% of premium smartphones"),
                target_entity=Entity(entity_name="Vision Holdings", entity_type="organization", entity_description="Vision Holdings is a firm that previously owned TechGlobal"),
                relationship_description="Vision Holdings formerly owned TechGlobal from 2014 until present",
                relationship_strength=5
            )
        ]).model_dump_json()}
        END OF EXAMPLE 2
        
        EXAMPLE 3
        Input:
        Entity_types: organization,geo,person
        Text:
        START OF INPUT TEXT
        Five Aurelians jailed for 8 years in Firuzabad and widely regarded as hostages are on their way home to Aurelia.
        
        The swap orchestrated by Quintara was finalized when $8bn of Firuzi funds were transferred to financial institutions in Krohaara, the capital of Quintara.
        
        The exchange initiated in Firuzabad's capital, Tiruzia, led to the four men and one woman, who are also Firuzi nationals, boarding a chartered flight to Krohaara.
        
        They were welcomed by senior Aurelian officials and are now on their way to Aurelia's capital, Cashion.
        
        The Aurelians include 39-year-old businessman Samuel Namara, who has been held in Tiruzia's Alhamia Prison, as well as journalist Durke Bataglani, 59, and environmentalist Meggie Tazbah, 53, who also holds Bratinas nationality.
        END OF INPUT TEXT
        Output:
        {EntityRelationshipList(list=[
            EntityRelationship(
                source_entity=Entity(entity_name="Firuzabad", entity_type="geo", entity_description="Firuzabad held Aurelians as hostages"),
                target_entity=Entity(entity_name="Aurelia", entity_type="geo", entity_description="Country seeking to release hostages"),
                relationship_description="Firuzabad negotiated a hostage exchange with Aurelia",
                relationship_strength=2
            ),
            EntityRelationship(
                source_entity=Entity(entity_name="Quintara", entity_type="organization", entity_description="Quintara brokered the hostage exchange between Firuzabad and Aurelia"),
                target_entity=Entity(entity_name="Aurelia", entity_type="geo", entity_description="Country seeking to release hostages"),
                relationship_description="Quintara brokered the hostage exchange between Firuzabad and Aurelia",
                relationship_strength=2
            ),
            EntityRelationship(
                source_entity=Entity(entity_name="Quintara", entity_type="organization", entity_description="Quintara brokered the hostage exchange between Firuzabad and Aurelia"),
                target_entity=Entity(entity_name="Firuzabad", entity_type="geo", entity_description="Firuzabad held Aurelians as hostages"),
                relationship_description="Quintara brokered the hostage exchange between Firuzabad and Aurelia",
                relationship_strength=2
            ),
            EntityRelationship(
                source_entity=Entity(entity_name="Samuel Namara", entity_type="person", entity_description="Samuel Namara was a prisoner at Alhamia prison"),
                target_entity=Entity(entity_name="Alhamia Prison", entity_type="geo", entity_description="Alhamia Prison is a prison in Tiruzia"),
                relationship_description="Samuel Namara was a hostage in Firuzabad",
                relationship_strength=2
            ),
            EntityRelationship(
                source_entity=Entity(entity_name="Samuel Namara", entity_type="person", entity_description="Samuel Namara was a prisoner at Alhamia prison"),
                target_entity=Entity(entity_name="Meggie Tazbah", entity_type="person", entity_description="Meggie Tazbah was a hostage in Firuzabad"),
                relationship_description="Samuel Namara and Meggie Tazbah were exchanged in the same hostage release",
                relationship_strength=2
            ),
            EntityRelationship(
                source_entity=Entity(entity_name="Samuel Namara", entity_type="person", entity_description="Samuel Namara was a prisoner at Alhamia prison"),
                target_entity=Entity(entity_name="Durke Bataglani", entity_type="person", entity_description="Durke Bataglani was a hostage in Firuzabad"),
                relationship_description="Samuel Namara and Durke Bataglani were exchanged in the same hostage release",
                relationship_strength=2
            ),
            EntityRelationship(
                source_entity=Entity(entity_name="Meggie Tazbah", entity_type="person", entity_description="Meggie Tazbah was a hostage in Firuzabad"),
                target_entity=Entity(entity_name="Durke Bataglani", entity_type="person", entity_description="Durke Bataglani was a hostage in Firuzabad"),
                relationship_description="Meggie Tazbah and Durke Bataglani were exchanged in the same hostage release",
                relationship_strength=2
            ),
            EntityRelationship(
                source_entity=Entity(entity_name="Samuel Namara", entity_type="person", entity_description="Samuel Namara was a prisoner at Alhamia prison"),
                target_entity=Entity(entity_name="Firuzabad", entity_type="geo", entity_description="Firuzabad held Aurelians as hostages"),
                relationship_description="Samuel Namara was a hostage in Firuzabad",
                relationship_strength=2
            ),
            EntityRelationship(
                source_entity=Entity(entity_name="Meggie Tazbah", entity_type="person", entity_description="Meggie Tazbah was a hostage in Firuzabad"),
                target_entity=Entity(entity_name="Firuzabad", entity_type="geo", entity_description="Firuzabad held Aurelians as hostages"),
                relationship_description="Meggie Tazbah was a hostage in Firuzabad",
                relationship_strength=2
            ),
            EntityRelationship(
                source_entity=Entity(entity_name="Durke Bataglani", entity_type="person", entity_description="Durke Bataglani was a hostage in Firuzabad"),
                target_entity=Entity(entity_name="Firuzabad", entity_type="geo", entity_description="Firuzabad held Aurelians as hostages"),
                relationship_description="Durke Bataglani was a hostage in Firuzabad",
                relationship_strength=2
            )
        ]).model_dump_json()}
        END OF EXAMPLE 3
        END OF EXAMPLE SECTION
        ---
        REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Generate Entity Types only.
        Text: {text}
        JSON response:
        """

        return self.llm.generate_object(
            messages=[Message(role="user", content=prompt)],
            response_model=EntityRelationshipList,
            temperature=0.1, num_ctx=32768
        )
