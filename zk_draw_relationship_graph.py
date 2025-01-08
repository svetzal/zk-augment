import pydot

from chroma_gateway import ChromaGateway
from graph.rdf import ns_documents, ns_entitytypes
from graph_gateway import GraphGateway
from app.settings import vault_root
from zettelkasten import Zettelkasten

chroma = ChromaGateway()
zk = Zettelkasten(vault_root, chroma)

graph: GraphGateway = GraphGateway.load_or_create('zksv.ttl')

dot = pydot.Dot(graph_type='digraph')
dot.set('pack', 'false')
dot.set('overlap', 'prism')

query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?subject ?label
WHERE {
    ?subject rdfs:label ?label .
}
"""
results = graph.query(query)

for row in results:
    node_id = str(row.subject).split('/')[-1]
    label = str(row.label)
    if row.subject.startswith(ns_documents):
        fillcolour = "#ddddff"
    elif row.subject.startswith(ns_entitytypes):
        fillcolour = "#ffffdd"
    else:
        fillcolour = "#ffffff"
    dot.add_node(pydot.Node(node_id, label=label, shape="Mrecord", fillcolor=fillcolour, style="filled"))

query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?subject ?predicate ?object
WHERE {
    ?subject ?predicate ?object .
    FILTER (?predicate != rdfs:label)
}
"""
results = graph.query(query)

for row in results:
    subject = str(row.subject).split('/')[-1]
    predicate = str(row.predicate)
    object = str(row.object).split('/')[-1]
    dot.add_edge(pydot.Edge(subject, object))


dot.write('zksv.dot')
