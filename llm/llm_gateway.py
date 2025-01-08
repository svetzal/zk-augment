from llm.adapters import LLMProviderAdapter, OllamaAdapter
from utility.logger import log
from tokenizer_gateway import TokenizerGateway


class LLMGateway():
    adapter: LLMProviderAdapter
    tokenizer: TokenizerGateway
    model: str

    def __init__(self, model: str, adapter: LLMProviderAdapter = None, tokenizer: TokenizerGateway = None):
        self.model = model
        if tokenizer is None:
            self.tokenizer = TokenizerGateway()
        else:
            self.tokenizer = tokenizer
        if adapter is None:
            self.adapter = OllamaAdapter()
        else:
            self.adapter = adapter

    def generate_text(self, messages, temperature=1.0, num_ctx=32768, num_predict=-1):
        approximate_tokens = len(self.tokenizer.encode("".join([message.content for message in messages])))
        log.info(f"Requesting chat response with approx {approximate_tokens} tokens")
        return self.adapter.complete(self.model, messages, temperature, num_ctx, num_predict)

    def generate_object(self, messages, response_model, temperature=1.0, num_ctx=32768, num_predict=-1):
        approximate_tokens = len(self.tokenizer.encode("".join([message.content for message in messages])))
        log.info(f"Requesting chat response with approx {approximate_tokens} tokens")
        return self.adapter.complete_with_object(self.model, messages, response_model, temperature, num_ctx, num_predict)
