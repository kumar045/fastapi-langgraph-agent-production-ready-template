"""Optional A2A tool loading for LangGraph workflows."""

from langchain_core.tools.base import BaseTool

from app.core.config import settings
from app.core.langgraph.tools.a2a import delegate_to_a2a_agent


async def load_a2a_tools() -> list[BaseTool]:
    """Load A2A tools based on runtime configuration."""
    if not settings.ENABLE_A2A:
        return []

    return [delegate_to_a2a_agent]
