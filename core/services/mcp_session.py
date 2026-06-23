"""
app/services/mcp_session.py — MCP connection factory.

Supports three transports:
    streamable_http  — modern single-endpoint HTTP (recommended)
    sse              — legacy HTTP + Server-Sent Events
    stdio            — spawns MCP server as a local subprocess
"""

from contextlib import asynccontextmanager
import logging
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters

from config import config as settings
import subprocess


@asynccontextmanager
async def memgraph_session():
    """
    Async context manager that yields an initialised MCP ClientSession.

    Usage:
        async with memgraph_session() as session:
            tools = await session.list_tools()
            result = await session.call_tool("run_query", {"query": "..."})
    """
    transport = settings.MCP_TRANSPORT.lower()

    if transport == "streamable_http":
        try:
            async with streamable_http_client(settings.MCP_URL) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    yield session
        except Exception as e:
            logging.error(f"streamable_http MCP error: {e}")
            raise

    elif transport == "sse":
        async with sse_client(settings.MCP_URL) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield session

    elif transport == "stdio":
        
        server_params = StdioServerParameters(
            command=settings.MCP_COMMAND,
            args=settings.MCP_ARGS,
            env=settings.MCP_ENV,
        )
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    yield session
        except Exception as e:
            logging.error(f"stdio MCP error: {e}")
            raise

    else:
        raise ValueError(
            f"Unknown MCP_TRANSPORT: '{transport}'. "
            "Must be 'streamable_http', 'sse', or 'stdio'."
        )
