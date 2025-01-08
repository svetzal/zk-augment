import pykka

from graph.extractor import EntityTypeExtractor
from llm.llm_gateway import LLMGateway
from llm.registry import LLMRegistry, LLMCapabilities, LLMSizeEnum, LLMTypeEnum
from zettelkasten import Zettelkasten


class EntityTypesExtractorAgent(pykka.ThreadingActor):
    def __init__(self, registry: LLMRegistry, zk: Zettelkasten):
        super().__init__()
        model = registry.find_first(LLMCapabilities(size=LLMSizeEnum.medium, type=LLMTypeEnum.chat))
        self.llm = LLMGateway(model.name, model.adapter)
        self.zk = zk
        self.registry = registry
        self.type_extractor = EntityTypeExtractor(self.llm)

    def on_receive(self, message):
        chunk_id = message.get('chunk_id')
        available_types = message.get('available_types', [])
        callback = message.get('callback', None)

        chunk = self.zk.find_chunk_by_id(chunk_id)
        types = self.type_extractor.extract_object_with_accumulated_types(available_types, chunk.text)

        if callback:
            callback(types)
