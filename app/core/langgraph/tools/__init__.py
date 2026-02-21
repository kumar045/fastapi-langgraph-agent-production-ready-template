"""LangGraph tools for enhanced language model capabilities."""

from langchain_core.tools.base import BaseTool

from .duckduckgo_search import duckduckgo_search_tool

DEFAULT_TOOLS: list[BaseTool] = [duckduckgo_search_tool]
