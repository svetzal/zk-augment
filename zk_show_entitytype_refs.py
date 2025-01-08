from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from rich.console import Console

from graph_gateway import GraphGateway

console = Console()

graph = GraphGateway.load_or_create('zksv.ttl')

query = prepareQuery("""
    SELECT ?document ?document_label ?entitytype ?entitytype_label
    WHERE {
        ?chunk <http://zksv.org/relationships/extracted_from> ?document .
        ?entitytype <http://zksv.org/relationships/extracted_from> ?chunk .
        ?document <http://www.w3.org/2000/01/rdf-schema#label> ?document_label .
        ?entitytype <http://www.w3.org/2000/01/rdf-schema#label> ?entitytype_label .
    }
""")

results = graph.query(query)

all_entitytypes = set()
document_entitytypes = {}
for row in results:
    document_label = str(row.document_label)
    entitytype_label = str(row.entitytype_label)
    all_entitytypes.add(entitytype_label)
    if document_label not in document_entitytypes:
        document_entitytypes[document_label] = set()
    document_entitytypes[document_label].add(entitytype_label)

console.print("[bold]Document Entity Types:[/bold]")
for document_label, entitytypes in document_entitytypes.items():
    sorted_entitytypes = sorted(entitytypes)
    console.print(f"Document: {document_label}")
    for type in sorted_entitytypes:
        print(f"   {type}")

console.print("[bold]Entity Types:[/bold]")
for type in sorted(all_entitytypes):
    console.print(f"   {type}")