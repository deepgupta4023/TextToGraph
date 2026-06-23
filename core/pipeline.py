from core.ingestion.chunker import chunk_text
from core.ingestion.extractor import extract_graph_from_text
from core.ingestion.normaliser import normalise_entities
from core.ingestion.graph_builder import build_graph


def ingest_text(text):

    chunks = chunk_text(text)

    all_entities = []
    all_relations = []

    for chunk in chunks:

        data = extract_graph_from_text(chunk)

        entities = data.get("entities", [])
        relations = data.get("relations", [])

        all_entities.extend(entities)
        all_relations.extend(relations)

    all_entities = normalise_entities(all_entities)

    graph_data = {
        "entities": all_entities,
        "relations": all_relations
    }

    build_graph(graph_data)

    return {
        "entities": len(all_entities),
        "relations": len(all_relations)
    }