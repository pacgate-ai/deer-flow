"""PacGate configuration: 3-axis routing and 5 hard gates for Big Law workflow.

This module defines the typed config models that are loaded from the
``pacgate:`` section of ``config.yaml``.  The config is consumed by two
middlewares:

* ``PacGateRoutingMiddleware`` — 3-axis pre-model routing
  (Axis A: complexity -> tier, Axis B: compliance -> local-only / de-id,
  Axis C: resilience -> forced upgrade).
* ``PacGateHardGatesMiddleware`` — system-enforced hard gates
  (Gate 1: conflicts-clear, Gate 3: cite-verified).

Gates 2, 4, 5 are advisory / SOUL.md-only and are not system-enforced in
this MVP; their config sections exist for documentation and future enablement.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "PacGateAxisAConfig",
    "PacGateAxisBConfig",
    "PacGateAxisCConfig",
    "PacGateRoutingConfig",
    "PacGateGate1Config",
    "PacGateGate2Config",
    "PacGateGate3Config",
    "PacGateGate4Config",
    "PacGateGate5Config",
    "PacGateHardGatesConfig",
    "PacGateConfig",
    "get_pacgate_config",
    "load_pacgate_config_from_dict",
    "reset_pacgate_config",
]


# ---------------------------------------------------------------------------
# Axis A — complexity -> tier routing
# ---------------------------------------------------------------------------

class PacGateAxisAConfig(BaseModel):
    """Axis A: route by skill-declared complexity to the matching tier.

    Skill frontmatter ``pacgate-tier-routing`` declares which tier(s) are
    appropriate for a given skill.  When the active skill declares a tier
    other than the current agent's tier, the middleware injects a routing
    hint into the model context.
    """

    enabled: bool = Field(default=True, description="Enable Axis A tier routing.")
    default_tier: str = Field(
        default="associate",
        description="Fallback tier when skill metadata is absent or ambiguous.",
    )
    tier_skill_prefix: str = Field(
        default="pacgate-tier-",
        description="Skill frontmatter key prefix used to declare tier routing.",
    )


# ---------------------------------------------------------------------------
# Axis B — compliance -> local-only / de-id
# ---------------------------------------------------------------------------

class PacGateAxisBConfig(BaseModel):
    """Axis B: enforce compliance routing (local-only, de-id gate).

    Skills whose frontmatter ``pacgate-redline`` is ``local-only`` or
    ``deid-required`` trigger compliance enforcement.  ``local-only`` skills
    are allowed to run only when the configured model is local (Ollama).
    ``deid-required`` skills inject a de-id reminder into the model context.
    """

    enabled: bool = Field(default=True, description="Enable Axis B compliance routing.")
    local_only_tag: str = Field(
        default="local-only",
        description="Skill redline tag that forces local-only execution.",
    )
    deid_required_tag: str = Field(
        default="deid-required",
        description="Skill redline tag that triggers de-id enforcement.",
    )
    local_model_patterns: list[str] = Field(
        default_factory=lambda: ["ollama", "localhost:11434"],
        description="Model API base URL substrings that identify a local model.",
    )


# ---------------------------------------------------------------------------
# Axis C — resilience -> forced upgrade
# ---------------------------------------------------------------------------

class PacGateAxisCConfig(BaseModel):
    """Axis C: forced model upgrade on high-risk / low-confidence patterns.

    When the active skill's redline tag is ``high-risk`` or the model response
    confidence is below ``low_confidence_threshold``, the middleware injects a
    forced-upgrade hint recommending escalation to a higher-tier model.
    """

    enabled: bool = Field(default=True, description="Enable Axis C resilience routing.")
    high_risk_tag: str = Field(
        default="high-risk",
        description="Skill redline tag that triggers forced upgrade.",
    )
    low_confidence_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Confidence below which forced upgrade is recommended.",
    )


class PacGateRoutingConfig(BaseModel):
    """Top-level routing config aggregating all 3 axes."""

    axis_a: PacGateAxisAConfig = Field(default_factory=PacGateAxisAConfig, description="Axis A: complexity -> tier.")
    axis_b: PacGateAxisBConfig = Field(default_factory=PacGateAxisBConfig, description="Axis B: compliance -> local-only / de-id.")
    axis_c: PacGateAxisCConfig = Field(default_factory=PacGateAxisCConfig, description="Axis C: resilience -> forced upgrade.")


# ---------------------------------------------------------------------------
# Hard gates
# ---------------------------------------------------------------------------

class PacGateGate1Config(BaseModel):
    """Gate 1: conflicts-clear before matter work.

    System-enforced: blocks matter-work skills (listed in
    ``matter_work_skills``) until the ``intake-conflicts`` skill has been
    run in the current thread.  The conflicts-cleared flag is tracked
    per-thread via a state key.
    """

    enabled: bool = Field(default=True, description="Enable Gate 1 conflicts-clear enforcement.")
    intake_skill: str = Field(
        default="intake-conflicts",
        description="Skill name that clears the conflicts gate when activated.",
    )
    matter_work_skills: list[str] = Field(
        default_factory=lambda: [
            "dd-report-assembly",
            "regulation-research",
            "offshore-dd",
            "nda-review",
            "contract-review",
            "ma-agreement-review",
            "vcpe-financing-suite",
            "corporate-equity",
            "finance-tax",
            "labor-hr",
            "regulatory-compliance",
        ],
        description="Skills blocked until conflicts gate is cleared.",
    )
    state_key: str = Field(
        default="pacgate_conflicts_cleared",
        description="Thread state key tracking conflicts-cleared status.",
    )


class PacGateGate2Config(BaseModel):
    """Gate 2: de-id before cloud (advisory in MVP).

    Not system-enforced; documented for future enablement.  When enabled,
    would block cloud-model calls when skill redline is ``deid-required``
    and de-id has not been confirmed.
    """

    enabled: bool = Field(default=False, description="Enable Gate 2 de-id-before-cloud enforcement (advisory in MVP).")
    deid_skill: str = Field(default="cold-start-interview", description="Skill that performs de-id.")
    state_key: str = Field(default="pacgate_deid_passed", description="Thread state key tracking de-id status.")


class PacGateGate3Config(BaseModel):
    """Gate 3: cite-verified before report output.

    System-enforced: blocks ``write_file`` calls targeting report paths
    (matched by ``report_path_patterns``) when the content lacks the
    ``cite-verified`` marker tag.  The marker is a structured HTML comment
    ``<!-- pacgate:cite-verified: A5 -->`` that the cite-checker subagent
    inserts after verifying citations.
    """

    enabled: bool = Field(default=True, description="Enable Gate 3 cite-verified enforcement.")
    report_path_patterns: list[str] = Field(
        default_factory=lambda: ["**/dd-report*", "**/尽职调查*", "**/dd_report*"],
        description="Glob patterns matching report file paths that require cite-verification.",
    )
    required_marker: str = Field(
        default="<!-- pacgate:cite-verified:",
        description="Marker prefix that must appear in file content for the gate to pass.",
    )
    write_tool_names: list[str] = Field(
        default_factory=lambda: ["write_file", "writeFile"],
        description="Tool names that trigger the gate when writing to report paths.",
    )


class PacGateGate4Config(BaseModel):
    """Gate 4: grade-is-advisory (disabled — SOUL.md only).

    Advisory only: the lead agent's SOUL.md instructs the model that
    matter grading is advisory until the associate confirms.  Not
    system-enforced.
    """

    enabled: bool = Field(default=False, description="Enable Gate 4 grade-is-advisory (advisory / SOUL.md only).")


class PacGateGate5Config(BaseModel):
    """Gate 5: partner-signoff (disabled — SOUL.md only).

    Advisory only: the lead agent's SOUL.md instructs the model that
    final deliverables require partner sign-off.  Not system-enforced.
    """

    enabled: bool = Field(default=False, description="Enable Gate 5 partner-signoff (advisory / SOUL.md only).")


class PacGateHardGatesConfig(BaseModel):
    """Top-level hard-gates config aggregating all 5 gates."""

    gate1_conflicts_clear: PacGateGate1Config = Field(
        default_factory=PacGateGate1Config,
        description="Gate 1: conflicts-clear before matter work.",
    )
    gate2_deid_before_cloud: PacGateGate2Config = Field(
        default_factory=PacGateGate2Config,
        description="Gate 2: de-id before cloud (advisory).",
    )
    gate3_cite_verified: PacGateGate3Config = Field(
        default_factory=PacGateGate3Config,
        description="Gate 3: cite-verified before report output.",
    )
    gate4_grade_is_advisory: PacGateGate4Config = Field(
        default_factory=PacGateGate4Config,
        description="Gate 4: grade-is-advisory (SOUL.md only).",
    )
    gate5_partner_signoff: PacGateGate5Config = Field(
        default_factory=PacGateGate5Config,
        description="Gate 5: partner-signoff (SOUL.md only).",
    )


# ---------------------------------------------------------------------------
# Top-level PacGate config
# ---------------------------------------------------------------------------

class PacGateConfig(BaseModel):
    """Top-level PacGate configuration loaded from ``config.yaml -> pacgate:``."""

    routing: PacGateRoutingConfig = Field(
        default_factory=PacGateRoutingConfig,
        description="3-axis routing middleware configuration.",
    )
    hard_gates: PacGateHardGatesConfig = Field(
        default_factory=PacGateHardGatesConfig,
        description="5 hard gates middleware configuration.",
    )


# ---------------------------------------------------------------------------
# Singleton (same pattern as guardrails_config.py)
# ---------------------------------------------------------------------------

_pacgate_config: PacGateConfig | None = None


def get_pacgate_config() -> PacGateConfig:
    """Get the PacGate config, returning defaults if not loaded."""
    global _pacgate_config
    if _pacgate_config is None:
        _pacgate_config = PacGateConfig()
    return _pacgate_config


def load_pacgate_config_from_dict(data: dict) -> PacGateConfig:
    """Load PacGate config from a dict (called during AppConfig loading)."""
    global _pacgate_config
    _pacgate_config = PacGateConfig.model_validate(data)
    return _pacgate_config


def reset_pacgate_config() -> None:
    """Reset the cached config instance. Used in tests to prevent singleton leaks."""
    global _pacgate_config
    _pacgate_config = None