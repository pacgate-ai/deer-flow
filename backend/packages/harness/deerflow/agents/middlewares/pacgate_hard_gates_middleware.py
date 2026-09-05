"""PacGate hard-gates middleware.

System-enforced gates from the PacGate Big Law workflow:

* **Gate 1** (conflicts-clear): blocks matter-work skills until the
  ``intake-conflicts`` skill has been activated in the current thread.
  Tracked via ``skill_context`` in thread state — if the intake skill
  name appears in the skill context, the gate is cleared.

* **Gate 3** (cite-verified): blocks ``write_file`` calls targeting report
  paths when the content lacks the ``<!-- pacgate:cite-verified: -->``
  marker.  The marker is inserted by the cite-checker subagent after
  verifying citations.

Gates 2, 4, 5 are advisory / SOUL.md-only and are not enforced here.
"""

from __future__ import annotations

import fnmatch
import logging
from collections.abc import Awaitable, Callable
from typing import Any, override

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import ToolMessage
from langgraph.errors import GraphBubbleUp
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command

from deerflow.config.pacgate_config import PacGateConfig, get_pacgate_config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Gate 1 helpers
# ---------------------------------------------------------------------------

def _skill_names_in_context(state: AgentState) -> set[str]:
    """Return the set of skill names that have been loaded in this thread."""
    skill_context = state.get("skill_context") or []
    if not isinstance(skill_context, list):
        return set()
    names: set[str] = set()
    for entry in skill_context:
        if isinstance(entry, dict):
            name = entry.get("name")
            if isinstance(name, str) and name:
                names.add(name)
    return names


def _active_skill_names(state: AgentState) -> set[str]:
    """Return the set of skill names currently active (loaded in skill_context)."""
    return _skill_names_in_context(state)


def _is_gate1_cleared(state: AgentState, config: PacGateConfig) -> bool:
    """Check if Gate 1 (conflicts-clear) has been satisfied."""
    gate1 = config.hard_gates.gate1_conflicts_clear
    if not gate1.enabled:
        return True
    # Check if the intake-conflicts skill has been loaded
    skill_names = _skill_names_in_context(state)
    return gate1.intake_skill in skill_names


def _is_matter_work_skill(skill_name: str, config: PacGateConfig) -> bool:
    """Check if a skill name is in the matter-work list."""
    gate1 = config.hard_gates.gate1_conflicts_clear
    return skill_name in gate1.matter_work_skills


def _active_matter_work_skills(state: AgentState, config: PacGateConfig) -> list[str]:
    """Return the list of active matter-work skills that would be blocked."""
    skill_names = _active_skill_names(state)
    return [s for s in skill_names if _is_matter_work_skill(s, config)]


# ---------------------------------------------------------------------------
# Gate 3 helpers
# ---------------------------------------------------------------------------

def _is_report_path(path: str, config: PacGateConfig) -> bool:
    """Check if a file path matches any report path pattern."""
    gate3 = config.hard_gates.gate3_cite_verified
    if not gate3.enabled:
        return False
    for pattern in gate3.report_path_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def _has_cite_verified_marker(content: str, config: PacGateConfig) -> bool:
    """Check if content contains the cite-verified marker."""
    gate3 = config.hard_gates.gate3_cite_verified
    return gate3.required_marker in content


def _is_write_tool(tool_name: str, config: PacGateConfig) -> bool:
    """Check if a tool name is a write tool that triggers Gate 3."""
    gate3 = config.hard_gates.gate3_cite_verified
    return tool_name in gate3.write_tool_names


def _requested_path(request: ToolCallRequest) -> str | None:
    """Extract the file path from a write_file tool call."""
    args = request.tool_call.get("args") or {}
    if not isinstance(args, dict):
        return None
    path = args.get("path")
    return path if isinstance(path, str) and path else None


def _requested_content(request: ToolCallRequest) -> str | None:
    """Extract the content from a write_file tool call."""
    args = request.tool_call.get("args") or {}
    if not isinstance(args, dict):
        return None
    content = args.get("content")
    return content if isinstance(content, str) else None


# ---------------------------------------------------------------------------
# Blocked message builders
# ---------------------------------------------------------------------------

_GATE1_BLOCK_TEMPLATE = (
    "PacGate Gate 1 blocked: 利冲未清不开工 (conflicts not cleared). "
    "The active skill '{skill}' is a matter-work skill, but the conflicts "
    "intake skill '{intake_skill}' has not been run in this thread. "
    "Run /{intake_skill} first to clear the conflicts gate, then retry."
)

_GATE3_BLOCK_TEMPLATE = (
    "PacGate Gate 3 blocked: 引证未核验不上行 (citations not verified). "
    "Writing to report path '{path}' requires the cite-verified marker "
    "'{marker}' in the content, but it was not found. "
    "Run the cite-checker subagent to verify citations, then re-attempt the write."
)


def _build_gate1_block(request: ToolCallRequest, skill_name: str, config: PacGateConfig) -> ToolMessage:
    gate1 = config.hard_gates.gate1_conflicts_clear
    tool_name = str(request.tool_call.get("name", "unknown"))
    tool_call_id = str(request.tool_call.get("id", "missing_id"))
    content = _GATE1_BLOCK_TEMPLATE.format(
        skill=skill_name,
        intake_skill=gate1.intake_skill,
    )
    return ToolMessage(
        content=content,
        tool_call_id=tool_call_id,
        name=tool_name,
        status="error",
    )


def _build_gate3_block(request: ToolCallRequest, path: str, config: PacGateConfig) -> ToolMessage:
    gate3 = config.hard_gates.gate3_cite_verified
    tool_name = str(request.tool_call.get("name", "unknown"))
    tool_call_id = str(request.tool_call.get("id", "missing_id"))
    content = _GATE3_BLOCK_TEMPLATE.format(
        path=path,
        marker=gate3.required_marker,
    )
    return ToolMessage(
        content=content,
        tool_call_id=tool_call_id,
        name=tool_name,
        status="error",
    )


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

class PacGateHardGatesMiddleware(AgentMiddleware[AgentState]):
    """PacGate hard-gates middleware.

    Hooks ``wrap_tool_call`` / ``awrap_tool_call`` to enforce:

    * Gate 1: blocks matter-work skill tool calls if conflicts not cleared.
    * Gate 3: blocks write_file to report paths if cite-verified marker absent.

    Gate 1 checks the *active skill context* — if any matter-work skill is
    active and the intake-conflicts skill has not been loaded, the tool call
    is blocked.  This is a per-thread gate tracked via ``skill_context``.
    """

    def __init__(
        self,
        *,
        pacgate_config: PacGateConfig | None = None,
    ) -> None:
        super().__init__()
        self._config = pacgate_config or get_pacgate_config()

    def _check_gate1(self, request: ToolCallRequest) -> ToolMessage | None:
        """Check Gate 1: conflicts-clear before matter work."""
        gate1 = self._config.hard_gates.gate1_conflicts_clear
        if not gate1.enabled:
            return None
        state = request.state
        if not isinstance(state, dict):
            state = {}
        # Check if any active skill is a matter-work skill
        blocked_skills = _active_matter_work_skills(state, self._config)
        if not blocked_skills:
            return None
        # Check if the gate is cleared
        if _is_gate1_cleared(state, self._config):
            return None
        # Gate is not cleared — block the first blocked skill
        return _build_gate1_block(request, blocked_skills[0], self._config)

    def _check_gate3(self, request: ToolCallRequest) -> ToolMessage | None:
        """Check Gate 3: cite-verified before report output."""
        gate3 = self._config.hard_gates.gate3_cite_verified
        if not gate3.enabled:
            return None
        tool_name = str(request.tool_call.get("name", ""))
        if not _is_write_tool(tool_name, self._config):
            return None
        path = _requested_path(request)
        if path is None:
            return None
        if not _is_report_path(path, self._config):
            return None
        content = _requested_content(request)
        if content is None:
            # No content to check — let the tool handle it
            return None
        if _has_cite_verified_marker(content, self._config):
            return None
        # Marker not found — block
        return _build_gate3_block(request, path, self._config)

    def _check_gates(self, request: ToolCallRequest) -> ToolMessage | None:
        """Check all enabled gates. Returns a blocked ToolMessage or None."""
        # Gate 1 first (conflicts-clear is the highest priority gate)
        blocked = self._check_gate1(request)
        if blocked is not None:
            return blocked
        # Gate 3 (cite-verified)
        blocked = self._check_gate3(request)
        if blocked is not None:
            return blocked
        return None

    @override
    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        try:
            blocked = self._check_gates(request)
        except GraphBubbleUp:
            raise
        except Exception:
            logger.warning("PacGate hard-gates check failed; allowing tool call (fail-open)", exc_info=True)
            return handler(request)
        if blocked is not None:
            logger.info(
                "PacGate hard gate blocked: tool=%s id=%s",
                request.tool_call.get("name"),
                request.tool_call.get("id"),
            )
            return blocked
        return handler(request)

    @override
    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command]],
    ) -> ToolMessage | Command:
        try:
            blocked = self._check_gates(request)
        except GraphBubbleUp:
            raise
        except Exception:
            logger.warning("PacGate hard-gates check failed; allowing tool call (fail-open)", exc_info=True)
            return await handler(request)
        if blocked is not None:
            logger.info(
                "PacGate hard gate blocked: tool=%s id=%s",
                request.tool_call.get("name"),
                request.tool_call.get("id"),
            )
            return blocked
        return await handler(request)