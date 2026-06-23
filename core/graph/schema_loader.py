import json
from pathlib import Path


def load_schema():

    path = Path("schema/schema.json")

    with open(path) as f:
        schema = json.load(f)

    return schema["nodes"], schema["relationships"]