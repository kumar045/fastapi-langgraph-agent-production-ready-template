"""Protocol endpoints for MCP and A2A integration visibility."""

from fastapi import APIRouter, Request

from app.core.config import settings
from app.core.limiter import limiter
from app.core.protocols import get_protocol_status

router = APIRouter()


@router.get("/status")
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["health"][0])
async def protocol_status(request: Request) -> dict[str, object]:
    """Return runtime MCP/A2A protocol status."""
    return get_protocol_status()
