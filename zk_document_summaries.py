from agents.document_summarizer import DocumentSummarizerAgent
from app.settings import vault_root, available_llms
from chroma_gateway import ChromaGateway
from zettelkasten import Zettelkasten

chroma = ChromaGateway()
zk = Zettelkasten(vault_root, chroma)
agent = DocumentSummarizerAgent.start(available_llms, zk)

for document in zk.all_markdown_documents():
    agent.tell({
        'document_id': document.id,
        'callback': lambda x: print(x)
    })

agent.stop()