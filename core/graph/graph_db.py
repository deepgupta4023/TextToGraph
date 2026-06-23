from gqlalchemy import Memgraph
from config import config


class GraphDB:

    def __init__(self):

        self.db = Memgraph(
            host=config.MEMGRAPH_HOST,
            port=int(config.MEMGRAPH_PORT)
                )

    # -----------------------------
    # Generic Query Executor
    # -----------------------------
    def run_query(self, query, params=None):

        if params is None:
            params = {}

        results = list(self.db.execute_and_fetch(query, params))
        return results

    # -----------------------------
    # Create Node
    # -----------------------------
    def create_node(self, label, name):

        query = f"""
        MERGE (n:{label} {{name: $name}})
        RETURN n
        """

        self.run_query(query, {"name": name})

    # -----------------------------
    # Create Relationship
    # -----------------------------
    def create_relationship(self, source, target, relation):

        query = f"""
        MATCH (a {{name:$src}})
        MATCH (b {{name:$dst}})
        MERGE (a)-[:{relation}]->(b)
        """

        self.run_query(query, {
            "src": source,
            "dst": target
        })

    # -----------------------------
    # Graph Summary
    # -----------------------------
    def graph_summary(self):

        query = """
        MATCH (n)
        OPTIONAL MATCH (n)-[r]->()
        RETURN COUNT(DISTINCT n) AS nodes,
               COUNT(DISTINCT r) AS edges
        """

        result = self.run_query(query)

        return result[0] if result else {}

    # -----------------------------
    # Reset Graph
    # -----------------------------
    def reset_graph(self):

        query = """
        MATCH (n)
        DETACH DELETE n
        """

        self.run_query(query)

    # -----------------------------
    # Get Graph Data for Visualization
    # -----------------------------
    def get_graph_data(self, limit=100):

        query = f"""
        MATCH (a)-[r]->(b)
        RETURN a.name AS source,
               TYPE(r) AS relation,
               b.name AS target
        LIMIT {limit}
        """

        return self.run_query(query)