"""Tests for PacGate 3-axis routing middleware."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import HumanMessage, SystemMessage

from deerflow.config.pacgate_config import PacGateConfig, reset_pacgate_config
from deerflow.agents.middlewares.pacgate_routing_middleware import (
    PacGateRoutingMiddleware,
    _build_axis_a_hint,
    _build_axis_b_hint,
    _build_axis_c_hint,
    _build_routing_reminder,
    _extract_pacgate_metadata,
    _load_skill_metadata,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DD_REPORT_METADATA = {
    "name": "dd-report-assembly",
    "metadata": {
        "pacgate-tier-routing": {
            "playbook-load": "low/local",
            "assemble": "mid/local",
            "cite-verify-gate": "upstream(A5)",
        },
        "pacgate-domain": "report-assembly",
        "pacgate-redline": "只装配不创作 + 缺内容留【待补】 + 强制免责声明 + 水印不可删 + 来源分级必标 + 上游必过A5/A6",
    },
}

INTAKE_CONFLICTS_METADATA = {
    "name": "intake-conflicts",
    "metadata": {
        "pacgate-tier-routing": {
            "interview": "low/local",
            "conflicts-run": "mid/local",
            "graph": "mid/local",
        },
        "pacgate-domain": "intake-conflicts",
    },
}

HIGH_RISK_METADATA = {
    "name": "ma-agreement-review",
    "metadata": {
        "pacgate-tier-routing": {"review": "main/local"},
        "pacgate-redline": "high-risk 并购协议审查涉及重大商业风险",
    },
}

LOCAL_ONLY_METADATA = {
    "name": "confidential-skill",
    "metadata": {
        "pacgate-redline": "local-only 客户机密数据不得上传云端",
    },
}

DEID_REQUIRED_METADATA = {
    "name": "sensitive-skill",
    "metadata": {
        "pacgate-redline": "deid-required 涉及个人敏感信息必须脱敏",
    },
}

NO_METADATA = {
    "name": "plain-skill",
    "description": "A skill without pacgate metadata",
}


def _state_with_skill(skill_name: str, skill_path: str | None = None) -> dict:
    """Build a state dict with a single skill in skill_context."""
    path = skill_path or f"skills/public/{skill_name}/SKILL.md"
    return {
        "messages": [],
        "skill_context": [{"name": skill_name, "path": path, "description": "", "loaded_at": 0}],
    }


def _make_middleware(config: PacGateConfig | None = None, skills_container_path: str = "/mnt/skills") -> PacGateRoutingMiddleware:
    return PacGateRoutingMiddleware(
        pacgate_config=config or PacGateConfig(),
        skills_container_path=skills_container_path,
    )


# ---------------------------------------------------------------------------
# Axis A tests (complexity -> tier)
# ---------------------------------------------------------------------------

class TestAxisA:
    def test_axis_a_hint_with_tier_routing(self):
        config = PacGateConfig()
        hint = _build_axis_a_hint(DD_REPORT_METADATA, config)
        assert hint is not None
        assert "Axis A" in hint
        assert "tier routing" in hint
        assert "playbook-load: low/local" in hint
        assert "assemble: mid/local" in hint

    def test_axis_a_no_hint_without_tier_routing(self):
        config = PacGateConfig()
        hint = _build_axis_a_hint(NO_METADATA, config)
        assert hint is None

    def test_axis_a_disabled(self):
        config = PacGateConfig()
        config.routing.axis_a.enabled = False
        hint = _build_axis_a_hint(DD_REPORT_METADATA, config)
        assert hint is None


# ---------------------------------------------------------------------------
# Axis B tests (compliance -> local-only / de-id)
# ---------------------------------------------------------------------------

class TestAxisB:
    def test_axis_b_local_only_hint(self):
        config = PacGateConfig()
        hint = _build_axis_b_hint(LOCAL_ONLY_METADATA, config)
        assert hint is not None
        assert "Axis B" in hint
        assert "local-only" in hint

    def test_axis_b_deid_required_hint(self):
        config = PacGateConfig()
        hint = _build_axis_b_hint(DEID_REQUIRED_METADATA, config)
        assert hint is not None
        assert "Axis B" in hint
        assert "de-identification" in hint or "deid" in hint.lower()

    def test_axis_b_no_hint_without_redline(self):
        config = PacGateConfig()
        hint = _build_axis_b_hint(NO_METADATA, config)
        assert hint is None

    def test_axis_b_disabled(self):
        config = PacGateConfig()
        config.routing.axis_b.enabled = False
        hint = _build_axis_b_hint(LOCAL_ONLY_METADATA, config)
        assert hint is None


# ---------------------------------------------------------------------------
# Axis C tests (resilience -> forced upgrade)
# ---------------------------------------------------------------------------

class TestAxisC:
    def test_axis_c_high_risk_hint(self):
        config = PacGateConfig()
        hint = _build_axis_c_hint(HIGH_RISK_METADATA, config)
        assert hint is not None
        assert "Axis C" in hint
        assert "high-risk" in hint
        assert "escalation" in hint.lower() or "upgrade" in hint.lower()

    def test_axis_c_no_hint_without_high_risk(self):
        config = PacGateConfig()
        hint = _build_axis_c_hint(DD_REPORT_METADATA, config)
        assert hint is None

    def test_axis_c_disabled(self):
        config = PacGateConfig()
        config.routing.axis_c.enabled = False
        hint = _build_axis_c_hint(HIGH_RISK_METADATA, config)
        assert hint is None


# ---------------------------------------------------------------------------
# Combined routing reminder
# ---------------------------------------------------------------------------

class TestRoutingReminder:
    def test_combined_reminder_with_all_axes(self):
        """A skill with tier-routing + high-risk redline produces hints from A + C."""
        config = PacGateConfig()
        metadata = {
            "metadata": {
                "pacgate-tier-routing": {"review": "main/local"},
                "pacgate-redline": "high-risk local-only",
            },
        }
        reminder = _build_routing_reminder(metadata, config)
        assert reminder is not None
        assert "Axis A" in reminder
        assert "Axis B" in reminder
        assert "Axis C" in reminder

    def test_combined_reminder_no_metadata(self):
        config = PacGateConfig()
        reminder = _build_routing_reminder(NO_METADATA, config)
        assert reminder is None


# ---------------------------------------------------------------------------
# Skill metadata extraction
# ---------------------------------------------------------------------------

class TestSkillMetadataExtraction:
    def test_extract_metadata_from_state(self, tmp_path):
        """Test that metadata is extracted from the skill_context in state."""
        # Create a fake skill file
        skill_dir = tmp_path / "public" / "test-skill"
        skill_dir.mkdir(parents=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            "---\nname: test-skill\ndescription: test\nmetadata:\n  pacgate-tier-routing:\n    review: mid/local\n---\n\nBody\n",
            encoding="utf-8",
        )
        # skill_context path is relative to the skills root
        state = _state_with_skill("test-skill", "public/test-skill/SKILL.md")
        metadata = _extract_pacgate_metadata(state, str(tmp_path))
        assert metadata is not None
        assert metadata.get("name") == "test-skill"
        # pacgate-tier-routing is nested under the frontmatter "metadata" key
        nested = metadata.get("metadata", {})
        assert "pacgate-tier-routing" in nested

    def test_extract_metadata_empty_skill_context(self):
        state = {"messages": [], "skill_context": []}
        metadata = _extract_pacgate_metadata(state, "/mnt/skills")
        assert metadata == {}

    def test_extract_metadata_no_skills_root(self):
        state = _state_with_skill("test-skill")
        metadata = _extract_pacgate_metadata(state, None)
        assert metadata == {}


# ---------------------------------------------------------------------------
# Middleware injection
# ---------------------------------------------------------------------------

class TestMiddlewareInjection:
    def test_middleware_injects_reminder_when_skill_active(self, tmp_path):
        """The middleware injects a SystemMessage reminder when a skill with pacgate metadata is active."""
        # Create a fake skill file under the skills root
        skill_dir = tmp_path / "public" / "test-skill"
        skill_dir.mkdir(parents=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            "---\nname: test-skill\ndescription: test\nmetadata:\n  pacgate-tier-routing:\n    review: mid/local\n  pacgate-redline: \"high-risk\"\n---\n\nBody\n",
            encoding="utf-8",
        )
        mw = _make_middleware(skills_container_path=str(tmp_path))
        state = _state_with_skill("test-skill", "public/test-skill/SKILL.md")

        # Mock ModelRequest — use a real-ish mock that supports override()
        from unittest.mock import MagicMock

        request = MagicMock()
        request.state = state
        request.messages = [HumanMessage(content="hello")]

        # Capture the modified request
        captured = []

        def handler(req):
            captured.append(req)
            return MagicMock()

        # Make override return the new request
        def override(**kwargs):
            new_req = MagicMock()
            new_req.state = request.state
            new_req.messages = kwargs.get("messages", request.messages)
            return new_req

        request.override = override

        mw.wrap_model_call(request, handler)

        assert len(captured) == 1
        modified = captured[0]
        # The modified request should have the reminder injected
        new_messages = modified.messages
        # Should have the original message + the injected SystemMessage
        assert len(new_messages) == 2
        # The first message should be the SystemMessage reminder
        assert isinstance(new_messages[0], SystemMessage)
        assert "PacGate" in new_messages[0].content

    def test_middleware_no_injection_when_no_skill_active(self):
        """The middleware does not inject when no skill is active."""
        mw = _make_middleware()
        state = {"messages": [], "skill_context": []}

        request = MagicMock()
        request.state = state
        request.messages = [HumanMessage(content="hello")]

        captured = []

        def handler(req):
            captured.append(req)
            return MagicMock()

        mw.wrap_model_call(request, handler)

        assert len(captured) == 1
        # The request should be unchanged
        assert captured[0] is request


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _reset_pacgate_config():
    """Reset the pacgate config singleton after each test."""
    yield
    reset_pacgate_config()