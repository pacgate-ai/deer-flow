"""Matter Management API — PacGate-Law matter overview endpoint.

Provides a read-only dashboard endpoint that aggregates thread metadata
into a matter-centric view: conflict status (Gate 1), DD pipeline progress,
and per-thread skill activity.  This is a thin read layer over the existing
thread metadata store — no new database tables are created.
"""

from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.gateway.authz import require_permission
from app.gateway.deps import get_optional_user_from_request, get_thread_store

router = APIRouter(prefix="/api", tags=["matters"])


class MatterSummary(BaseModel):
    """A single matter (thread) with PacGate-specific metadata."""

    thread_id: str
    title: str | None = None
    agent_name: str | None = None
    conflicts_cleared: bool = False
    last_activity: str | None = None
    message_count: int = 0
    has_dd_report: bool = False
    active_skills: list[str] = []


class MatterListResponse(BaseModel):
    """Response for the matters list endpoint."""

    matters: list[MatterSummary]
    total: int


@router.get("/matters")
@require_permission("threads", "read")
async def list_matters(request: Request) -> MatterListResponse:
    """List all matters (threads) with PacGate metadata for the current user.

    Each thread is mapped to a MatterSummary with conflict status, DD report
    presence, and active skill list extracted from thread metadata.
    """
    user = await get_optional_user_from_request(request)
    if user is None:
        return MatterListResponse(matters=[], total=0)

    thread_store = get_thread_store(request)
    threads = await thread_store.list_threads(str(user.id))

    matters: list[MatterSummary] = []
    for thread in threads:
        thread_id = thread.get("thread_id", "")
        if not thread_id:
            continue

        meta = thread.get("metadata", {})
        if not isinstance(meta, dict):
            meta = {}

        # Extract PacGate-specific fields from thread state metadata
        conflicts_cleared = bool(meta.get("pacgate_conflicts_cleared", False))
        skill_context = meta.get("skill_context", [])
        active_skills = list(skill_context) if isinstance(skill_context, list) else []

        # Check for DD report artifacts
        artifacts = meta.get("artifacts", [])
        has_dd_report = False
        if isinstance(artifacts, list):
            for art in artifacts:
                name = art.get("name", "") if isinstance(art, dict) else ""
                if "dd-report" in name.lower() or "尽职调查" in name:
                    has_dd_report = True
                    break

        matters.append(
            MatterSummary(
                thread_id=thread_id,
                title=thread.get("display_name"),
                agent_name=thread.get("assistant_id"),
                conflicts_cleared=conflicts_cleared,
                last_activity=thread.get("updated_at"),
                message_count=int(thread.get("message_count", 0)),
                has_dd_report=has_dd_report,
                active_skills=active_skills,
            )
        )

    return MatterListResponse(matters=matters, total=len(matters))