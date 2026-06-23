import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    LLM_BACKEND = os.getenv("LLM_BACKEND","openai")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_MAX_TOKENS= int(os.getenv("OPENAI_MAX_TOKENS", 4096))
    OPENAI_MAX_ITERATIONS= int(os.getenv("OPENAI_MAX_ITERATIONS", 10))

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    CLAUDE_MAX_TOKENS= int(os.getenv("CLAUDE_MAX_TOKENS", 4096))
    CLAUDE_MAX_ITERATIONS= int(os.getenv("CLAUDE_MAX_ITERATIONS", 10))

    MEMGRAPH_HOST = os.getenv("MEMGRAPH_HOST", "localhost")
    MEMGRAPH_PORT = int(os.getenv("MEMGRAPH_PORT", 7687))
    MEMGRAPH_USERNAME= os.getenv("MEMGRAPH_USERNAME", "")
    MEMGRAPH_PASSWORD=os.getenv("MEMGRAPH_PASSWORD", "")
    MEMGRAPH_BOLT_URL= os.getenv("MEMGRAPH_BOLT_URL", "bolt://memgraph:7687")

    MCP_TRANSPORT = "stdio" #os.getenv("MCP_TRANSPORT", "streamable_http")
    MCP_URL = os.getenv("MCP_URL", "http://localhost:8000/mcp")

    # stdio only
    MCP_COMMAND=os.getenv("MCP_COMMAND", "mcp-memgraph")
    @property
    def MCP_ARGS(self) -> list[str]:
        self.mcp_args_list=os.getenv("MCP_ARGS", "")

        return [a for a in self.mcp_args_list.split(",") if a]
    

    @property
    def MCP_ENV(self) -> dict:
        return {
            "MEMGRAPH_HOST":     self.MEMGRAPH_HOST,
            "MEMGRAPH_PORT":     str(self.MEMGRAPH_PORT),
            "MEMGRAPH_USERNAME": self.MEMGRAPH_USERNAME,
            "MEMGRAPH_PASSWORD": self.MEMGRAPH_PASSWORD,
            "MEMGRAPH_URI":      self.MEMGRAPH_BOLT_URL,
            "MEMGRAPH_URL":      self.MEMGRAPH_BOLT_URL,
            "PATH":              os.environ.get("PATH", "")
        }

config = Config()