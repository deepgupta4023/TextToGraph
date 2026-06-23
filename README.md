# TextToGraph

Convert unstructured text into a structured graph representation using AI-powered extraction pipelines.

TextToGraph processes natural language documents, extracts entities and relationships, and transforms them into graph structures that can be visualized, queried, and integrated into graph databases such as Neo4j, Memgraph, or TigerGraph.

---

## Features

- Text ingestion pipeline
- Entity extraction
- Relationship extraction
- Graph generation
- REST API for processing requests
- UI for graph visualization and interaction
- Modular architecture for extending extraction logic
- Dockerized deployment

---

## Architecture

```text
                +------------------+
                |     User / UI    |
                +---------+--------+
                          |
                          v
                +------------------+
                |      API Layer   |
                +---------+--------+
                          |
                          v
                +------------------+
                |     Pipeline     |
                +---------+--------+
                          |
          +---------------+----------------+
          |                                |
          v                                v
+------------------+          +----------------------+
| Text Ingestion   |          | Prompt Generation    |
+------------------+          +----------------------+
          |                                |
          +---------------+----------------+
                          |
                          v
                +------------------+
                | AI/LLM Extraction|
                +---------+--------+
                          |
                          v
                +------------------+
                | Graph Builder    |
                +---------+--------+
                          |
                          v
                +------------------+
                | Graph Output     |
                +------------------+
```

---

## Project Structure

```text
TextToGraph/
│
├── api/
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
│
├── core/
│   ├── graph/
│   ├── ingestion/
│   ├── services/
│   ├── pipeline.py
│   └── prompts.py
│
├── schema/
├── scripts/
├── ui/
│
├── config.py
├── requirements.txt
├── docker-compose.yml
└── Dockerfile.api
```

---

## Tech Stack

- Python
- FastAPI
- Docker
- LLM-based Information Extraction
- Graph Processing
- REST APIs

---

## Installation

### Clone Repository

```bash
git clone https://github.com/deepgupta4023/TextToGraph.git
cd TextToGraph
```

### Create Virtual Environment

```bash
python -m venv venv
```

Linux / Mac

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Update configuration values inside:

```python
config.py
```

Configure:

- LLM provider
- API keys
- Graph database credentials
- Runtime settings

---

## Running the API

```bash
python api/main.py
```

Or

```bash
uvicorn api.main:app --reload
```

API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## Running with Docker

Build and start services:

```bash
docker-compose up --build
```

Run in detached mode:

```bash
docker-compose up -d
```

---

## Example Workflow

### Input

```text
Elon Musk founded SpaceX.
SpaceX launched Falcon 9.
```

### Extracted Entities

```json
[
  "Elon Musk",
  "SpaceX",
  "Falcon 9"
]
```

### Extracted Relationships

```json
[
  {
    "source": "Elon Musk",
    "relationship": "FOUNDED",
    "target": "SpaceX"
  },
  {
    "source": "SpaceX",
    "relationship": "LAUNCHED",
    "target": "Falcon 9"
  }
]
```

### Graph Representation

```text
(Elon Musk)-[:FOUNDED]->(SpaceX)
(SpaceX)-[:LAUNCHED]->(Falcon 9)
```

---

## Use Cases

- Knowledge Graph Construction
- Document Intelligence
- Research Analysis
- Political Relationship Mapping
- Enterprise Data Discovery
- RAG Enhancement
- Entity Relationship Analysis

---

## Future Enhancements

- Neo4j integration
- Memgraph integration
- Graph visualization dashboard
- Batch document processing
- Multi-document relationship discovery
- Graph analytics

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Submit a Pull Request

---

## Author

**Deep Gupta**

Data Scientist | AI Engineer | Graph Technologies Enthusiast

GitHub:
https://github.com/deepgupta4023

LinkedIn:
https://www.linkedin.com/in/deepgupta4023/

---
