import chromadb
from chromadb import Settings


class ChromaGateway:
    def __init__(self, partition_name: str = "zettelkasten"):
        self.partition_name = partition_name
        self.chroma_client = chromadb.PersistentClient(settings=Settings(allow_reset=True))
        self.collection = self.init_collection()

    def init_collection(self):
        return self.chroma_client.get_or_create_collection(
            name=self.partition_name)  # , embedding_function=OllamaEmbeddingFunction())

    def add_items(self, ids, documents, metadatas, embeddings):
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def reset_indexes(self):
        self.chroma_client.reset()
        self.collection = self.init_collection()

    def query(self, query_embeddings, n_results):
        return self.collection.query(query_embeddings=query_embeddings, n_results=n_results)

    def query_with_metadata_filter(self, query_embeddings, metadata_filter, n_results):
        return self.collection.query(query_embeddings=query_embeddings, n_results=n_results, where=metadata_filter)

    def get_all_items(self):
        return self.collection.get()

    def get_items_with_metadata_filter(self, metadata_filter):
        return self.collection.get(where=metadata_filter)

    def get_item_by_id(self, chunk_id):
        return self.collection.get(ids=[chunk_id])
