"""Tests for PacGate hard-gates middleware (Gate 1 + Gate 3)."""

from unittest.mock import MagicMock

import pytest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest

from deerflow.config.pacgate_config import PacGateConfig, reset_pacgate_config
from deerflow.agents.middlewares.pacgate_hard_gates_middleware import (
    PacGateHardGatesMiddleware,
    _is_report_path,
    _has_cite_verified_marker,
    _is_write_tool,
    _skill_names_in_context,
    _is_gate1_cleared,
    _active_matter_work_skills,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_request(name: str, args: dict, state: dict | None = None) -> ToolCallRequest:
    runtime = MagicMock()
    runtime.context = {"thread_id": "t-test"}
    return ToolCallRequest(
        tool_call={"name": name, "args": args, "id": "call-1"},
        tool=None,
        state=state or {"messages": []},
        runtime=runtime,
    )


def _state_with_skills(skill_names: list[str]) -> dict:
    """Build a state dict with skill_context populated by skill names."""
    return {
        "messages": [],
        "skill_context": [{"name": n, "path": f"skills/public/{n}/SKILL.md", "description": "", "loaded_at": 0} for n in skill_names],
    }


def _make_middleware(config: PacGateConfig | None = None) -> PacGateHardGatesMiddleware:
    return PacGateHardGatesMiddleware(pacgate_config=config or PacGateConfig())


# ---------------------------------------------------------------------------
# Gate 1: conflicts-clear
# ---------------------------------------------------------------------------

class TestGate1ConflictsClear:
    def test_gate1_blocks_matter_work_skill_when_conflicts_not_cleared(self):
        """Gate 1 blocks tool calls when a matter-work skill is active and intake-conflicts hasn't run."""
        mw = _make_middleware()
        state = _state_with_skills(["dd-report-assembly"])
        request = _make_request("write_file", {"path": "/tmp/output.txt", "content": "test"}, state=state)
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert isinstance(result, ToolMessage)
        assert result.status == "error"
        assert "Gate 1" in result.content
        assert "conflicts" in result.content.lower()

    def test_gate1_allows_when_intake_conflicts_has_run(self):
        """Gate 1 is cleared when intake-conflicts skill is in the skill context."""
        mw = _make_middleware()
        state = _state_with_skills(["intake-conflicts", "dd-report-assembly"])
        request = _make_request("write_file", {"path": "/tmp/output.txt", "content": "test"}, state=state)
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert result.content == "ok"

    def test_gate1_allows_when_no_matter_work_skill_active(self):
        """Gate 1 does not block when no matter-work skill is active."""
        mw = _make_middleware()
        state = _state_with_skills(["cold-start-interview"])
        request = _make_request("write_file", {"path": "/tmp/output.txt", "content": "test"}, state=state)
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert result.content == "ok"

    def test_gate1_allows_when_no_skill_active(self):
        """Gate 1 does not block when no skill is active at all."""
        mw = _make_middleware()
        state = {"messages": [], "skill_context": []}
        request = _make_request("write_file", {"path": "/tmp/output.txt", "content": "test"}, state=state)
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert result.content == "ok"

    def test_gate1_disabled_allows_everything(self):
        """Gate 1 disabled = no blocking even with matter-work skill and no intake."""
        config = PacGateConfig()
        config.hard_gates.gate1_conflicts_clear.enabled = False
        mw = _make_middleware(config)
        state = _state_with_skills(["dd-report-assembly"])
        request = _make_request("write_file", {"path": "/tmp/output.txt", "content": "test"}, state=state)
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert result.content == "ok"

    def test_gate1_blocks_all_matter_work_skills(self):
        """Gate 1 blocks every skill in the matter_work_skills list."""
        mw = _make_middleware()
        for skill_name in mw._config.hard_gates.gate1_conflicts_clear.matter_work_skills:
            state = _state_with_skills([skill_name])
            request = _make_request("write_file", {"path": "/tmp/test.txt", "content": "x"}, state=state)
            result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
            assert isinstance(result, ToolMessage)
            assert result.status == "error", f"Gate 1 should block skill '{skill_name}'"
            assert "Gate 1" in result.content


class TestGate1Helpers:
    def test_skill_names_in_context(self):
        state = _state_with_skills(["intake-conflicts", "dd-report-assembly"])
        names = _skill_names_in_context(state)
        assert names == {"intake-conflicts", "dd-report-assembly"}

    def test_skill_names_empty_context(self):
        state = {"messages": [], "skill_context": []}
        assert _skill_names_in_context(state) == set()

    def test_is_gate1_cleared_when_intake_present(self):
        config = PacGateConfig()
        state = _state_with_skills(["intake-conflicts", "contract-review"])
        assert _is_gate1_cleared(state, config) is True

    def test_is_gate1_not_cleared_when_intake_absent(self):
        config = PacGateConfig()
        state = _state_with_skills(["contract-review"])
        assert _is_gate1_cleared(state, config) is False

    def test_active_matter_work_skills(self):
        config = PacGateConfig()
        state = _state_with_skills(["intake-conflicts", "contract-review", "cold-start-interview"])
        active = _active_matter_work_skills(state, config)
        assert "contract-review" in active
        assert "intake-conflicts" not in active
        assert "cold-start-interview" not in active


# ---------------------------------------------------------------------------
# Gate 3: cite-verified
# ---------------------------------------------------------------------------

class TestGate3CiteVerified:
    def test_gate3_blocks_write_to_report_path_without_marker(self):
        """Gate 3 blocks write_file to a report path when content lacks the cite-verified marker."""
        mw = _make_middleware()
        # Clear gate 1 by including intake-conflicts in the skill context
        state = _state_with_skills(["intake-conflicts", "dd-report-assembly"])
        request = _make_request(
            "write_file",
            {"path": "/tmp/dd-report-final.md", "content": "# DD Report\n\nSome content without marker."},
            state=state,
        )
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert isinstance(result, ToolMessage)
        assert result.status == "error"
        assert "Gate 3" in result.content
        assert "cite-verified" in result.content.lower() or "引证" in result.content

    def test_gate3_allows_write_to_report_path_with_marker(self):
        """Gate 3 allows write_file to a report path when content has the cite-verified marker."""
        mw = _make_middleware()
        state = _state_with_skills(["intake-conflicts", "dd-report-assembly"])
        content = "# DD Report\n\nSome content.\n<!-- pacgate:cite-verified: A5 -->\n"
        request = _make_request(
            "write_file",
            {"path": "/tmp/dd-report-final.md", "content": content},
            state=state,
        )
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert result.content == "ok"

    def test_gate3_allows_write_to_non_report_path(self):
        """Gate 3 does not block writes to non-report paths."""
        mw = _make_middleware()
        state = _state_with_skills(["intake-conflicts", "dd-report-assembly"])
        request = _make_request(
            "write_file",
            {"path": "/tmp/notes.txt", "content": "no marker here"},
            state=state,
        )
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert result.content == "ok"

    def test_gate3_disabled_allows_all_writes(self):
        """Gate 3 disabled = no blocking even for report paths without marker."""
        config = PacGateConfig()
        config.hard_gates.gate3_cite_verified.enabled = False
        mw = _make_middleware(config)
        state = _state_with_skills(["intake-conflicts", "dd-report-assembly"])
        request = _make_request(
            "write_file",
            {"path": "/tmp/dd-report-final.md", "content": "no marker"},
            state=state,
        )
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert result.content == "ok"

    def test_gate3_blocks_append_to_report_path(self):
        """Gate 3 blocks even append=True writes to report paths without marker."""
        mw = _make_middleware()
        state = _state_with_skills(["intake-conflicts", "dd-report-assembly"])
        request = _make_request(
            "write_file",
            {"path": "/tmp/dd-report-chapter3.md", "content": "appended content", "append": True},
            state=state,
        )
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        assert isinstance(result, ToolMessage)
        assert result.status == "error"


class TestGate3Helpers:
    def test_is_report_path_matches(self):
        config = PacGateConfig()
        assert _is_report_path("/tmp/dd-report-final.md", config) is True
        assert _is_report_path("/tmp/dd_report_v2.md", config) is True
        assert _is_report_path("/tmp/尽职调查报告.md", config) is True

    def test_is_report_path_no_match(self):
        config = PacGateConfig()
        assert _is_report_path("/tmp/notes.txt", config) is False
        assert _is_report_path("/tmp/contract.txt", config) is False

    def test_has_cite_verified_marker_present(self):
        config = PacGateConfig()
        content = "Some text\n<!-- pacgate:cite-verified: A5 -->\nMore text"
        assert _has_cite_verified_marker(content, config) is True

    def test_has_cite_verified_marker_absent(self):
        config = PacGateConfig()
        content = "Some text without marker"
        assert _has_cite_verified_marker(content, config) is False

    def test_is_write_tool(self):
        config = PacGateConfig()
        assert _is_write_tool("write_file", config) is True
        assert _is_write_tool("writeFile", config) is True
        assert _is_write_tool("read_file", config) is False
        assert _is_write_tool("web_search", config) is False


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------

class TestAsyncBehavior:
    @pytest.mark.asyncio
    async def test_awrap_tool_call_gate1_blocks(self):
        """Async Gate 1 blocking works."""
        mw = _make_middleware()
        state = _state_with_skills(["dd-report-assembly"])
        request = _make_request("write_file", {"path": "/tmp/test.txt", "content": "x"}, state=state)

        async def handler(req):
            return ToolMessage(content="ok", tool_call_id="call-1", name="write_file")

        result = await mw.awrap_tool_call(request, handler)
        assert isinstance(result, ToolMessage)
        assert result.status == "error"
        assert "Gate 1" in result.content

    @pytest.mark.asyncio
    async def test_awrap_tool_call_gate3_blocks(self):
        """Async Gate 3 blocking works."""
        mw = _make_middleware()
        state = _state_with_skills(["intake-conflicts", "dd-report-assembly"])
        request = _make_request(
            "write_file",
            {"path": "/tmp/dd-report.md", "content": "no marker"},
            state=state,
        )

        async def handler(req):
            return ToolMessage(content="ok", tool_call_id="call-1", name="write_file")

        result = await mw.awrap_tool_call(request, handler)
        assert isinstance(result, ToolMessage)
        assert result.status == "error"
        assert "Gate 3" in result.content

    @pytest.mark.asyncio
    async def test_awrap_tool_call_allows_when_cleared(self):
        """Async: both gates pass when cleared."""
        mw = _make_middleware()
        state = _state_with_skills(["intake-conflicts", "dd-report-assembly"])
        content = "# Report\n<!-- pacgate:cite-verified: A5 -->\n"
        request = _make_request(
            "write_file",
            {"path": "/tmp/dd-report.md", "content": content},
            state=state,
        )

        async def handler(req):
            return ToolMessage(content="ok", tool_call_id="call-1", name="write_file")

        result = await mw.awrap_tool_call(request, handler)
        assert result.content == "ok"


# ---------------------------------------------------------------------------
# Fail-open behavior
# ---------------------------------------------------------------------------

class TestFailOpen:
    def test_fail_open_on_exception(self):
        """Middleware fails open if gate check raises an exception."""
        mw = _make_middleware()
        # Create a state that will cause an exception in _check_gate1
        # by making skill_context a non-list, non-dict value
        state = {"messages": [], "skill_context": "invalid"}
        request = _make_request("write_file", {"path": "/tmp/test.txt", "content": "x"}, state=state)
        result = mw.wrap_tool_call(request, handler=lambda r: ToolMessage(content="ok", tool_call_id="call-1", name="write_file"))
        # Should fail open and allow the tool call
        assert result.content == "ok"


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _reset_pacgate_config():
    """Reset the pacgate config singleton after each test."""
    yield
    reset_pacgate_config()