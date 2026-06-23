from core.graph.graph_db import GraphDB

db = GraphDB()


def get_node_count():

    query = """
    MATCH (n)
    RETURN COUNT(n) AS nodes
    """

    result = db.run_query(query)
    return result[0]["nodes"]


def get_edge_count():

    query = """
    MATCH ()-[r]->()
    RETURN COUNT(r) AS edges
    """

    result = db.run_query(query)
    return result[0]["edges"]


def most_connected_nodes(limit=5):

    query = f"""
    MATCH (n)-[r]-()
    RETURN n.name AS node,
           COUNT(r) AS degree
    ORDER BY degree DESC
    LIMIT {limit}
    """

    return db.run_query(query)