from ollama import Message

from llm.llm_gateway import LLMGateway
from models import ZkDocument


class DocumentSummarizer:
    def __init__(self, llm: LLMGateway) -> None:
        self.llm = llm

    def create(self, document: ZkDocument) -> str:
        prompt = [
            Message(role="user", content=f"""
Title: {document.title}
Author: {document.author}
Created On: {document.context_date}
Content:
{document.content}

Create a detailed summary of the ideas and content of the preceding content. Do not elaborate or
extrapolate. Stick to the summary of the content, jump right into it and don't add anything to the
beginning or end.

Your Summary:
"""),
        ]
        return self.llm.generate_text(prompt, temperature=1)