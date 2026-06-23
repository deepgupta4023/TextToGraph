from core.graph.graph_db import GraphDB

db = GraphDB()

db.create_node("Person", "Elon Musk")
db.create_node("Company", "SpaceX")

db.create_relationship("Elon Musk", "SpaceX", "FOUNDED")

summary = db.graph_summary()

print(summary)