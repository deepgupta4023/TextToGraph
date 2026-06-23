"""
app/services/llm_client.py — Agentic loop: LLM ↔ MCP session ↔ Memgraph.

Supports two LLM backends (controlled by settings.llm_backend):
    'anthropic' — Claude via Anthropic API
    'openai'    — GPT-4o via OpenAI API

Tool schemas are fetched live from the MCP server on every request.
Nothing is hardcoded.
"""

import json
from typing import Any, Callable, Awaitable, Optional

import anthropic
import openai
from mcp import ClientSession

from config import config as settings
from core.services.mcp_session import memgraph_session
import logging
import traceback

logging.basicConfig(level=logging.INFO)


# -----------------------------------------------------------------------
# System prompt
# -----------------------------------------------------------------------

SYSTEM_PROMPT = """You are an expert graph database analyst specialising in Memgraph and Cypher.

You have access to a Memgraph database. Use the available MCP tools to answer
user questions accurately. Follow this approach:

1. If unsure about the schema, call the schema tool first.
2. Translate natural-language questions into precise, efficient Cypher queries.
3. Return clear, concise answers with key numbers and names where relevant.
4. If a query fails, diagnose the error and try an alternative approach.
5. Never invent or guess data — only report what the database actually returns.
"""

# Type alias for the optional progress callback
ToolCallCallback = Callable[[str, Any, str], Awaitable[None]]


# -----------------------------------------------------------------------
# Tool format converters
# -----------------------------------------------------------------------

def _to_anthropic_tools(mcp_tools) -> list[dict]:
    return [
        {
            "name": t.name,
            "description": t.description or "",
            "input_schema": t.inputSchema,
        }
        for t in mcp_tools
    ]


def _to_openai_tools(mcp_tools) -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description or "",
                "parameters": t.inputSchema,
            },
        }
        for t in mcp_tools
    ]


# -----------------------------------------------------------------------
# LLM Client
# -----------------------------------------------------------------------

class LLMClient:
    """
    Agentic loop that routes to the correct LLM backend based on
    settings.llm_backend ('anthropic' or 'openai').
    """

    def __init__(self,llm_backend: Optional[str] = None):
        # Use provided backend, fall back to settings
        self.backend = llm_backend or settings.LLM_BACKEND.lower()
        

        if self.backend == "anthropic":
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        elif self.backend == "openai":
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            raise ValueError(f"Unknown LLM_BACKEND: '{self.backend}'. Use 'anthropic' or 'openai'.")

    async def ask(
        self,
        question: str,
        on_tool_call: ToolCallCallback | None = None,
    ) -> str:
        """
        Run the full agentic loop for a natural-language question.

        Args:
            question:     Plain-English question about the Memgraph database.
            on_tool_call: Optional async callback fired on each tool execution.
                          Signature: async (tool_name, tool_input, result) -> None

        Returns:
            The LLM's final plain-text answer.
        """
        try:
            async with memgraph_session() as session:
                tools_response = await session.list_tools()

                if self.backend == "anthropic":
                    tools = _to_anthropic_tools(tools_response.tools)
                    return await self._loop_anthropic(session, tools, question, on_tool_call)
                else:
                    tools = _to_openai_tools(tools_response.tools)
                    return await self._loop_openai(session, tools, question, on_tool_call)
        except Exception as e:
            logging.error(f"LLMClient.ask failed: {e}")
            logging.error(traceback.format_exc())
            raise
    # -------------------------------------------------------------------
    # Anthropic loop
    # -------------------------------------------------------------------

    async def _loop_anthropic(
        self,
        session: ClientSession,
        tools: list[dict],
        question: str,
        on_tool_call: ToolCallCallback | None,
    ) -> str:
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": question}
        ]

        for _ in range(settings.CLAUDE_MAX_ITERATIONS):
            response = self.client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=settings.CLAUDE_MAX_TOKENS,
                system=SYSTEM_PROMPT,
                tools=tools,
                messages=messages,
            )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                return _extract_text(response.content)

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    mcp_result = await session.call_tool(block.name, block.input)
                    tool_output = _flatten_mcp_result(mcp_result)

                    if on_tool_call:
                        await on_tool_call(block.name, block.input, tool_output)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": tool_output,
                    })
                messages.append({"role": "user", "content": tool_results})
                continue

            return f"[Stopped: {response.stop_reason}]\n" + _extract_text(response.content)

        return "Reached maximum iterations without a final answer."

    # -------------------------------------------------------------------
    # OpenAI loop
    # -------------------------------------------------------------------

    async def _loop_openai(
        self,
        session: ClientSession,
        tools: list[dict],
        question: str,
        on_tool_call: ToolCallCallback | None,
    ) -> str:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": question},
        ]

        for _ in range(settings.OPENAI_MAX_ITERATIONS):
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                tools=tools,
                messages=messages,
            )

            choice = response.choices[0]
            messages.append(choice.message)

            if choice.finish_reason == "stop":
                return choice.message.content or ""

            if choice.finish_reason == "tool_calls":
                for tool_call in choice.message.tool_calls:
                    mcp_result = await session.call_tool(
                        tool_call.function.name,
                        json.loads(tool_call.function.arguments),
                    )
                    tool_output = _flatten_mcp_result(mcp_result)

                    if on_tool_call:
                        await on_tool_call(
                            tool_call.function.name,
                            tool_call.function.arguments,
                            tool_output,
                        )

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output,
                    })
                continue

            return f"[Stopped: {choice.finish_reason}]"

        return "Reached maximum iterations without a final answer."

    async def rephrase(self, system_prompt, content: str) -> str:
        """
        Call the LLM directly without MCP tools — just for text generation/rephrasing.
        """
        if self.backend == "anthropic":
            response = self.client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=settings.CLAUDE_MAX_TOKENS,
                system=system_prompt,
                messages=[{"role": "user", "content": content}]
            )
            return response.content[0].text

        else:  # openai
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ]
            )
            return response.choices[0].message.content

# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------

def _extract_text(content_blocks: list) -> str:
    return "\n".join(
        block.text for block in content_blocks if hasattr(block, "text")
    ).strip()


def _flatten_mcp_result(mcp_result) -> str:
    parts = []
    for item in mcp_result.content:
        if hasattr(item, "text"):
            parts.append(item.text)
        else:
            parts.append(f"[{item.type} content]")
    return "\n".join(parts) if parts else json.dumps({"status": "ok", "data": None})
