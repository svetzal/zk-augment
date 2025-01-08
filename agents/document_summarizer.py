import pykka

from aggregation.document_summarizer import DocumentSummarizer
from llm.llm_gateway import LLMGateway
from llm.registry import LLMRegistry, LLMCapabilities, LLMTypeEnum, LLMSizeEnum
from zettelkasten import Zettelkasten


class DocumentSummarizerAgent(pykka.ThreadingActor):
    def __init__(self, registry: LLMRegistry, zk: Zettelkasten):
        super().__init__()
        # Large forces this to use an external llm (OpenAI gpt-4o-mini)
        model = registry.find_first(LLMCapabilities(size=LLMSizeEnum.medium, type=LLMTypeEnum.chat))
        self.llm = LLMGateway(model.name, model.adapter)
        self.zk = zk
        self.summarizer = DocumentSummarizer(self.llm)

    def on_receive(self, message):
        document_id = message.get('document_id')
        callback = message.get('callback', None)

        document = self.zk.find_by_id(document_id)
        summary = self.summarizer.create(document)

        if callback:
            callback(summary)
