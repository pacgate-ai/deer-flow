"""Tests for prefix-aware skill allowed-tools matching.

PacGate 2026-10-08: skills declare allowed-tools with bare MCP *server* names
(e.g. ``pkulaw``, ``yuandian-law``, ``pacgate``), but loaded MCP tool names are
prefixed with the (hyphen-normalized) server name, e.g.
``pkulaw_case_keyword_get_case_list``, ``pacgate_pacgate_connector_search``.
Exact-match filtering therefore dropped ALL 137 MCP tools once any skill
declared allowed-tools (verified live 2026-10-08, thread 44e28035 used only
bash/read_file). The filter must treat a declaration as covering every tool
whose name is the declaration itself or starts with ``<declaration>_``.
"""

from pathlib import Path

from deerflow.skills.tool_policy import (
    allowed_tool_names_for_skills,
    filter_tools_by_skill_allowed_tools,
)
from deerflow.skills.types import Skill


class NamedTool:
    def __init__(self, name: str):
        self.name = name


def _make_skill(name: str, allowed_tools: list[str] | None = None) -> Skill:
    return Skill(
        name=name,
        description=f"Description for {name}",
        license="MIT",
        skill_dir=Path(f"/tmp/{name}"),
        skill_file=Path(f"/tmp/{name}/SKILL.md"),
        relative_path=Path(name),
        category="public",
        allowed_tools=allowed_tools,
        enabled=True,
    )


def test_server_name_declaration_covers_prefixed_mcp_tools():
    """Declaring a bare server name (``pkulaw``) must admit its prefixed tools."""
    skills = [_make_skill("legal", ["pkulaw"])]
    tools = [
        NamedTool("pkulaw_case_keyword_get_case_list"),
        NamedTool("pkulaw_citation_validator_adjust_provisions"),
        NamedTool("bash"),
        NamedTool("web_search"),
    ]
    out = filter_tools_by_skill_allowed_tools(tools, skills)
    assert {t.name for t in out} == {
        "pkulaw_case_keyword_get_case_list",
        "pkulaw_citation_validator_adjust_provisions",
    }


def test_hyphenated_server_name_normalizes_to_underscore_prefix():
    """``yuandian-law`` must match tools prefixed ``yuandian_law_``."""
    skills = [_make_skill("legal", ["yuandian-law"])]
    tools = [
        NamedTool("yuandian_law_yuandian_search_law"),
        NamedTool("yuandian_case_yuandian_search_judicial_cases"),  # different server
    ]
    out = filter_tools_by_skill_allowed_tools(tools, skills)
    assert {t.name for t in out} == {"yuandian_law_yuandian_search_law"}


def test_exact_name_still_matches():
    """Exact-name matching (non-MCP tools) must keep working."""
    skills = [_make_skill("s", ["bash", "read_file"])]
    tools = [NamedTool("bash"), NamedTool("read_file"), NamedTool("write_file")]
    out = filter_tools_by_skill_allowed_tools(tools, skills)
    assert {t.name for t in out} == {"bash", "read_file"}


def test_pacgate_bridge_tool_admitted_by_server_declaration():
    """The pacgate bridge tool (double prefix) must be admitted by ``pacgate``."""
    skills = [_make_skill("dd", ["pacgate"])]
    tools = [NamedTool("pacgate_pacgate_connector_search"), NamedTool("pacgate_pacgate_kb_search")]
    out = filter_tools_by_skill_allowed_tools(tools, skills)
    assert {t.name for t in out} == {"pacgate_pacgate_connector_search", "pacgate_pacgate_kb_search"}


def test_declaration_must_not_match_unrelated_prefix_collision():
    """``qcc`` must NOT admit ``qcc_extra_thing``-style tools from other servers
    whose names merely share the prefix — only real ``qcc_<tool>`` names."""
    skills = [_make_skill("s", ["qcc"])]
    tools = [NamedTool("qcc_company_get_company"), NamedTool("qccother_tool")]
    out = filter_tools_by_skill_allowed_tools(tools, skills)
    assert {t.name for t in out} == {"qcc_company_get_company"}


def test_union_across_skills_covers_all_declared_servers():
    """Union across multiple skills: each server declaration admits its tools."""
    skills = [
        _make_skill("a", ["pkulaw", "yuandian-case"]),
        _make_skill("b", ["openviking"]),
    ]
    tools = [
        NamedTool("pkulaw_law_keyword_get_law_list"),
        NamedTool("yuandian_case_yuandian_search_judicial_cases"),
        NamedTool("openviking_search"),
        NamedTool("firecrawl_firecrawl_search"),  # not declared anywhere
    ]
    out = filter_tools_by_skill_allowed_tools(tools, skills)
    assert {t.name for t in out} == {
        "pkulaw_law_keyword_get_law_list",
        "yuandian_case_yuandian_search_judicial_cases",
        "openviking_search",
    }


def test_allowed_tool_names_for_skills_returns_raw_declarations():
    """The union helper keeps returning raw declarations (API unchanged);
    prefix expansion happens in the filter, not in the union."""
    skills = [_make_skill("s", ["pkulaw"])]
    assert allowed_tool_names_for_skills(skills) == {"pkulaw"}


def test_no_declarations_still_allow_all():
    skills = [_make_skill("legacy", None)]
    tools = [NamedTool("anything"), NamedTool("pkulaw_x")]
    assert filter_tools_by_skill_allowed_tools(tools, skills) == tools


def test_always_allowed_tools_still_pass_through():
    """read_file is a framework tool; skills that declare allowed-tools keep it
    via their own declaration (the deployed 0.1.24 image has no
    always_allowed_tool_names parameter — that is newer-upstream)."""
    skills = [_make_skill("s", ["pkulaw", "read_file"])]
    tools = [NamedTool("read_file"), NamedTool("pkulaw_x")]
    out = filter_tools_by_skill_allowed_tools(tools, skills)
    assert {t.name for t in out} == {"read_file", "pkulaw_x"}
