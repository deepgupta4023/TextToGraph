from fastapi import APIRouter, HTTPException
from .schemas import TextRequest, QueryRequest
from core.pipeline import ingest_text
from core.services.llm_client import LLMClient
from core.graph.graph_db import GraphDB

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/cleardb")
def cleardb():
    try:
        gd= GraphDB()
        gd.reset_graph()
        return {"status": "ok", "message": "DB Cleared"}
    except Exception as e:
        return {"status":"NOT OK", "message": f"Error occured {e}"}


@router.post("/ingest")
def ingest(request: TextRequest):

    result = ingest_text(request.text)

    return {
        "message": "Graph created",
        "entities": result["entities"],
        "relations": result["relations"]
    }


@router.post("/query")
async def query_graph(request: QueryRequest):

    """
    Send a plain natural-language question to the LLM + MCP pipeline.

    The LLM will autonomously decide which Memgraph tools to call,
    execute them via the MCP server, and return a final answer.
    """
    try:
        
        if request.llm_backend in ['anthropic','openai']:
            client = LLMClient(llm_backend=request.llm_backend)
        else:
            client = LLMClient()
        answer = await client.ask(request.question)
        return {"answer":answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))