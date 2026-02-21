"""Optional A2A delegation tool for LangGraph workflows."""

from typing import Any

import httpx
from langchain_core.tools import tool

from app.core.config import settings
from app.core.logging import logger


def _resolve_a2a_headers(agent_name: str) -> dict[str, str]:
    """Resolve global and per-agent auth headers for A2A requests."""
    merged_headers: dict[str, Any] = dict(settings.A2A_AUTH_HEADERS)
    agent_headers = settings.A2A_AGENT_AUTH_HEADERS.get(agent_name)
    if isinstance(agent_headers, dict):
        merged_headers.update(agent_headers)

    return {str(key): str(value) for key, value in merged_headers.items() if value is not None}


@tool("delegate_to_a2a_agent")
async def delegate_to_a2a_agent(task: str, agent_name: str = "default") -> str:
    """Delegate a task to a configured A2A-compatible HTTP endpoint and return the response."""
    if not settings.ENABLE_A2A:
        return "a2a_is_disabled"

    target_url = settings.A2A_AGENT_ENDPOINTS.get(agent_name, settings.A2A_SERVER_URL)
    if not target_url:
        return "a2a_server_url_not_configured"

    payload = {"task": task, "agent_name": agent_name}
    request_headers = _resolve_a2a_headers(agent_name)

    try:
        async with httpx.AsyncClient(timeout=settings.A2A_TIMEOUT_SECONDS) as client:
            response = await client.post(target_url, json=payload, headers=request_headers or None)
            response.raise_for_status()
            response_data = response.json()
            logger.info(
                "a2a_task_delegated",
                a2a_server_url=target_url,
                agent_name=agent_name,
                auth_configured=bool(request_headers),
            )
            return str(response_data)
    except Exception as request_error:
        logger.exception(
            "a2a_task_delegation_failed",
            error=str(request_error),
            a2a_server_url=target_url,
            agent_name=agent_name,
        )
        return "a2a_task_failed"
