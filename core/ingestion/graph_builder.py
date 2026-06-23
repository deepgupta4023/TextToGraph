from core.graph.graph_db import GraphDB
import re
db = GraphDB()

def normalize_relation(rel):
    rel = rel.upper()
    rel = rel.replace(" ", "_")
    rel = re.sub(r"[^A-Z0-9_]", "", rel)
    return rel



def build_graph(data):

    entities = data.get("entities", [])
    relations = data.get("relations", [])

    # Create nodes
    for e in entities:

        label = e.get("type")
        name = e.get("name")

        if label and name:
            db.create_node(label, name)

    # Create edges
    for r in relations:

        source = r.get("source")
        target = r.get("target")
        relation = r.get("relation")

        if source and target and relation:
            relation = normalize_relation(relation)

            db.create_relationship(
                source,
                target,
                relation
            )