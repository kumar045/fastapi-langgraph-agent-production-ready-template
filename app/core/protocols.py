"""Protocol integration helpers for MCP and A2A support."""

from importlib import metadata

from app.core.config import settings
from app.core.logging import logger


def _is_installed(package_name: str) -> bool:
    """Check if a package is installed in the runtime environment."""
    try:
        metadata.version(package_name)
        return True
    except metadata.PackageNotFoundError:
        return False


def get_protocol_status() -> dict[str, object]:
    """Return MCP/A2A capability status for this deployment."""
    status = {
        "mcp": {
            "enabled": settings.ENABLE_MCP,
            "servers": settings.MCP_SERVER_URLS,
            "server_count": len(settings.MCP_SERVER_CONFIGS) or len(settings.MCP_SERVER_URLS),
            "auth_configured": bool(settings.MCP_AUTH_HEADERS),
            "adapter_installed": _is_installed("langchain-mcp-adapters"),
        },
        "a2a": {
            "enabled": settings.ENABLE_A2A,
            "agent_card_url": settings.A2A_AGENT_CARD_URL,
            "server_url": settings.A2A_SERVER_URL,
            "agent_endpoints": settings.A2A_AGENT_ENDPOINTS,
            "auth_configured": bool(settings.A2A_AUTH_HEADERS),
            "agent_auth_configured": bool(settings.A2A_AGENT_AUTH_HEADERS),
            "sdk_installed": _is_installed("a2a-sdk"),
            "google_adk_installed": _is_installed("google-adk"),
            "langgraph_server_installed": _is_installed("langgraph-a2a-server"),
        },
    }
    logger.info("protocol_status_generated", mcp_enabled=status["mcp"]["enabled"], a2a_enabled=status["a2a"]["enabled"])
    return status
