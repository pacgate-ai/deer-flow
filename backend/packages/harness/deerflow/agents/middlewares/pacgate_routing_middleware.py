"""PacGate 3-axis routing middleware.

Injects pre-model routing hints based on the active skill's frontmatter
metadata:

* **Axis A** (complexity -> tier): reads ``pacgate-tier-routing`` from the
  skill's frontmatter and injects a tier-routing reminder.
* **Axis B** (compliance -> local-only / de-id): reads ``pacgate-redline``
  from the skill's frontmatter.  ``local-only`` skills get a local-only
  enforcement reminder; ``deid-required`` skills get a de-id reminder.
* **Axis C** (resilience -> forced upgrade): reads ``pacgate-redline`` for
  ``high-risk`` tags and injects a forced-upgrade recommendation.

The middleware is **advisory** — it injects system-reminders into the model
context but does not block execution.  Hard enforcement is handled by
``PacGateHardGatesMiddleware``.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import SystemMessage

from deerflow.config.pacgate_config import PacGateConfig, get_pacgate_config
from deerflow.skills.frontmatter import split_skill_markdown

if TYPE_CHECKING:
    from langchain.agents.middleware.types import ModelCallResult, ModelRequest, ModelResponse

logger = logging.getLogger(__name__)

_PACGATE_ROUTING_REMINDER_KEY = "pacgate_routing_reminder"

# ---------------------------------------------------------------------------
# Skill frontmatter cache (process-local, keyed by skill path)
# ---------------------------------------------------------------------------

_skill_metadata_cache: dict[str, dict[str, Any]] = {}


def _load_skill_metadata(skill_path: str) -> dict[str, Any]:
    """Load and cache the frontmatter metadata for a skill."""
    if skill_path in _skill_metadata_cache:
        return _skill_metadata_cache[skill_path]
    metadata: dict[str, Any] = {}
    try:
        parts, _err = split_skill_markdown(Path(skill_path).read_text(encoding="utf-8"))
        if parts is not None:
            metadata = parts.metadata
    except Exception:  # noqa: BLE001
        logger.debug("Failed to read skill metadata: %s", skill_path, exc_info=True)
    _skill_metadata_cache[skill_path] = metadata
    return metadata


def _extract_pacgate_metadata(state: AgentState, skills_root: str | None) -> dict[str, Any]:
    """Extract pacgate-* metadata from the active skill(s) in thread state."""
    skill_context = state.get("skill_context") or []
    if not skill_context or skills_root is None:
        return {}
    # Use the most recently loaded skill (last in list)
    entry = skill_context[-1] if isinstance(skill_context, list) and skill_context else None
    if not isinstance(entry, dict):
        return {}
    path = entry.get("path")
    if not isinstance(path, str) or not path:
        return {}
    # skill_context paths are normalized under the skills root (posix).
    # They may be absolute (e.g. "/mnt/skills/public/foo/SKILL.md") or
    # relative to the root (e.g. "public/foo/SKILL.md").  Resolve accordingly.
    import posixpath

    normalized_root = posixpath.normpath(skills_root)
    normalized_path = posixpath.normpath(path)
    if normalized_path.startswith(normalized_root + "/") or normalized_path == normalized_root:
        # Already under the skills root — use as-is
        full_path = Path(normalized_path)
    else:
        # Relative to skills root
        full_path = Path(skills_root) / normalized_path
    return _load_skill_metadata(str(full_path))


# ---------------------------------------------------------------------------
# Routing hint builders
# ---------------------------------------------------------------------------

def _build_axis_a_hint(metadata: dict[str, Any], config) -> str | None:
    """Axis A: complexity -> tier routing hint."""
    if not config.routing.axis_a.enabled:
        return None
    # pacgate-tier-routing is nested under the frontmatter "metadata" key
    skill_meta = metadata.get("metadata", {}) if isinstance(metadata.get("metadata"), dict) else {}
    tier_routing = skill_meta.get("pacgate-tier-routing")
    if not isinstance(tier_routing, dict) or not tier_routing:
        return None
    # Flatten the tier-routing dict into a compact hint
    parts = [f"{subtask}: {tier}" for subtask, tier in tier_routing.items()]
    return f"[PacGate Axis A — tier routing] Active skill declares tier routing: {'; '.join(parts)}. Follow the declared tier for each subtask."


def _build_axis_b_hint(metadata: dict[str, Any], config) -> str | None:
    """Axis B: compliance -> local-only / de-id hint."""
    if not config.routing.axis_b.enabled:
        return None
    skill_meta = metadata.get("metadata", {}) if isinstance(metadata.get("metadata"), dict) else {}
    redline = skill_meta.get("pacgate-redline")
    if not isinstance(redline, str) or not redline:
        return None
    redline_lower = redline.lower()
    hints: list[str] = []
    if config.routing.axis_b.local_only_tag in redline_lower:
        hints.append("This skill is tagged local-only — all processing must stay on local models. Do not send data to cloud APIs.")
    if config.routing.axis_b.deid_required_tag in redline_lower:
        hints.append("This skill requires de-identification — strip PII / client-identifying data before any cloud call or external output.")
    if not hints:
        return None
    return f"[PacGate Axis B — compliance] {' '.join(hints)}"


def _build_axis_c_hint(metadata: dict[str, Any], config) -> str | None:
    """Axis C: resilience -> forced upgrade hint."""
    if not config.routing.axis_c.enabled:
        return None
    skill_meta = metadata.get("metadata", {}) if isinstance(metadata.get("metadata"), dict) else {}
    redline = skill_meta.get("pacgate-redline")
    if not isinstance(redline, str) or not redline:
        return None
    if config.routing.axis_c.high_risk_tag in redline.lower():
        return f"[PacGate Axis C — resilience] This skill is tagged high-risk. If your confidence on any subtask is below {config.routing.axis_c.low_confidence_threshold:.0%}, recommend escalation to a higher-tier model (e.g. partner-level review)."
    return None


def _build_routing_reminder(metadata: dict[str, Any], config: PacGateConfig) -> str | None:
    """Build the combined routing reminder from all 3 axes."""
    hints: list[str] = []
    for builder in (_build_axis_a_hint, _build_axis_b_hint, _build_axis_c_hint):
        hint = builder(metadata, config)
        if hint:
            hints.append(hint)
    if not hints:
        return None
    return "\n".join(hints)


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

class PacGateRoutingMiddleware(AgentMiddleware[AgentState]):
    """PacGate 3-axis routing middleware.

    Hooks ``wrap_model_call`` / ``awrap_model_call`` to inject routing
    hints derived from the active skill's frontmatter metadata.
    """

    def __init__(
        self,
        *,
        app_config: Any | None = None,
        pacgate_config: PacGateConfig | None = None,
        skills_container_path: str | None = None,
    ) -> None:
        super().__init__()
        self._pacgate_config = pacgate_config or get_pacgate_config()
        self._skills_container_path = skills_container_path
        if skills_container_path is None and app_config is not None:
            self._skills_container_path = app_config.skills.container_path

    def _maybe_build_reminder(self, state: AgentState) -> SystemMessage | None:
        metadata = _extract_pacgate_metadata(state, self._skills_container_path)
        if not metadata:
            return None
        reminder_text = _build_routing_reminder(metadata, self._pacgate_config)
        if reminder_text is None:
            return None
        return SystemMessage(
            content=reminder_text,
            additional_kwargs={_PACGATE_ROUTING_REMINDER_KEY: True},
        )

    def _inject(self, request: ModelRequest) -> ModelRequest:
        reminder = self._maybe_build_reminder(request.state)
        if reminder is None:
            return request
        # Insert after leading system messages (same pattern as DurableContextMiddleware)
        messages = list(request.messages)
        insert_idx = 0
        while insert_idx < len(messages) and isinstance(messages[insert_idx], SystemMessage):
            insert_idx += 1
        new_messages = [*messages[:insert_idx], reminder, *messages[insert_idx:]]
        return request.override(messages=new_messages)

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelCallResult:
        return handler(self._inject(request))

    async def awrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], Awaitable[ModelResponse]],
    ) -> ModelCallResult:
        return await handler(self._inject(request))