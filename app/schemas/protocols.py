"""Schemas for MCP and A2A protocol endpoints."""

from typing import Any

from pydantic import BaseModel, Field


class A2AProxyRequest(BaseModel):
    """Request payload for forwarding an A2A envelope to a remote agent."""

    target_url: str = Field(..., description="Remote A2A endpoint URL")
    payload: dict[str, Any] = Field(..., description="A2A envelope payload")


class A2AProxyResponse(BaseModel):
    """Response payload for A2A forwarding."""

    status_code: int = Field(..., description="HTTP status code returned by the target agent")
    response: dict[str, Any] = Field(..., description="Response JSON payload from the target agent")
