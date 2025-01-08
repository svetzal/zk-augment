import pykka
from ollama import Message

from llm.llm_gateway import LLMGateway
from llm.registry import LLMRegistry, LLMCapabilities, LLMSizeEnum, LLMTypeEnum


class RelativeDateResolverAgent(pykka.ThreadingActor):
    def __init__(self, registry: LLMRegistry):
        super().__init__()
        model = registry.model_name_matching(LLMCapabilities(size=LLMSizeEnum.medium, type=LLMTypeEnum.chat))
        self.llm = LLMGateway(model)

    def on_receive(self, message):
        input_text = message.get('input_text')
        reference_date = message.get('reference_date', None)
        callback = message.get('callback', None)

        if reference_date:
            result = self.process_message(input_text, reference_date)
            if callback:
                callback(result)

    def process_message(self, input_text, reference_date):
        messages = [
            Message(role="user", content=f"""
                Current Date: {reference_date}
                
                INPUT TEXT:
                {input_text}
                END INPUT TEXT
                
                Your instructions:
                - replace any relative dates with resolved dates
                - return ONLY the input text with the relative dates replaced with resolved dates
            """),
        ]

        response = self.llm.generate_text(messages, temperature=0)

        return response
