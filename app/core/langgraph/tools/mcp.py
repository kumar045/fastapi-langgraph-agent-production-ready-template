"""Optional MCP tool loading for LangGraph workflows."""

from importlib import import_module
from typing import Any

from langchain_core.tools.base import BaseTool

from app.core.config import settings
from app.core.logging import logger


def _build_mcp_server_config() -> dict[str, dict[str, Any]]:
    """Build MCP server configuration from env settings."""
    if settings.MCP_SERVER_CONFIGS:
        return {
            str(name): dict(config)
            for name, config in settings.MCP_SERVER_CONFIGS.items()
            if isinstance(config, dict)
        }

    return {
        f"server_{idx}": {"url": server_url, "transport": "streamable_http"}
        for idx, server_url in enumerate(settings.MCP_SERVER_URLS)
    }


async def load_mcp_tools() -> list[BaseTool]:
    """Load tools from configured MCP servers when available."""
    if not settings.ENABLE_MCP:
        return []

    server_config = _build_mcp_server_config()
    if not server_config:
        logger.info("mcp_disabled_due_to_missing_server_configuration")
        return []

    try:
        client_module = import_module("langchain_mcp_adapters.client")
        client_class = getattr(client_module, "MultiServerMCPClient")
    except Exception as import_error:
        logger.exception("mcp_adapter_import_failed", error=str(import_error))
        return []

    try:
        client = client_class(server_config)
        mcp_tools = await client.get_tools()
        logger.info("mcp_tools_loaded", tool_count=len(mcp_tools), server_count=len(server_config))
        return mcp_tools
    except Exception as runtime_error:
        logger.exception("mcp_tools_loading_failed", error=str(runtime_error))
        return []
