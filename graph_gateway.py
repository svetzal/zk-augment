import os

from rdflib import Graph


class GraphGateway():
    def __init__(self, file_path, graph=None):
        self.file_path = file_path
        if graph is None:
            self.graph = Graph()
        else:
            self.graph = graph

    @classmethod
    def load(cls, file_path):
        graph = Graph()
        graph.parse(file_path, format="turtle")
        return cls(file_path, graph)

    def save(self):
        self.graph.serialize(destination=self.file_path, format="turtle")

    @classmethod
    def load_or_create(cls, file_path='zksv.ttl'):
        if os.path.exists(file_path):
            return cls.load(file_path)
        else:
            return cls(file_path)

    def query(self, query):
        return self.graph.query(query)

    def add(self, triple):
        self.graph.add(triple)

    def bind(self, prefix, namespace):
        self.graph.bind(prefix, namespace)
