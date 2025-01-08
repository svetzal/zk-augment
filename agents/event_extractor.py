from typing import List

import pykka
from ollama import Message

from pydantic import BaseModel

from llm.llm_gateway import LLMGateway
from llm.registry import LLMRegistry, LLMCapabilities, LLMSizeEnum, LLMTypeEnum


class Event(BaseModel):
    date: str
    content: str


class EventList(BaseModel):
    events: List[Event]


class EventExtractorAgent(pykka.ThreadingActor):
    def __init__(self, registry: LLMRegistry, relative_date_resolver_agent: pykka.ActorRef):
        super().__init__()
        self.relative_date_resolver_agent = relative_date_resolver_agent
        model = registry.model_name_matching(LLMCapabilities(size=LLMSizeEnum.medium, type=LLMTypeEnum.instruct))
        self.llm = LLMGateway(model)

    def on_receive(self, message):
        input_text = message.get('input_text')
        callback = message.get('callback', None)

        self.relative_date_resolver_agent.tell({
            'input_text': input_text,
            'reference_date': "2025-01-05 EST",
            'callback': lambda x: self.handle_resolved_text(x, callback)
        })

    def handle_resolved_text(self, resolved_text, callback):
        result = self.process_message(resolved_text)
        if callback:
            callback(result)

    def process_message(self, input_text):
        messages = [
            Message(role="user", content=f"""
                INPUT TEXT:
                {input_text}
                END INPUT TEXT
                
                Your instructions:
                - extract any events from the input text
                - return a list of the extracted events
            """),
        ]

        response = self.llm.generate_object(messages, EventList, temperature=0)

        return response
