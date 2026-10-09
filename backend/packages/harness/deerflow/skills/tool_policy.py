import logging
from typing import Protocol

from deerflow.skills.types import Skill

logger = logging.getLogger(__name__)


class NamedTool(Protocol):
    name: str


# Framework built-ins that remain available even when an active skill declares
# allowed-tools. They support controlled file/review/discovery workflows rather
# than extending the reviewed/activated skill's own business-tool authority.
# In particular, promotion through tool_search does not restore a tool removed
# by SkillToolPolicyMiddleware, and describe_skill only returns catalog metadata.
ALWAYS_AVAILABLE_BUILTIN_TOOL_NAMES = frozenset(
    {
        "describe_skill",
        "read_file",
        "review_skill_package",
        "tool_search",
    }
)


def allowed_tool_names_for_skills(skills: list[Skill]) -> set[str] | None:
    """Return the union of explicit skill allowed-tools declarations.

    None means legacy allow-all behavior. It is returned only when no loaded
    skill declares allowed-tools. Once any skill declares the field, legacy
    skills without the field contribute no tools instead of disabling the
    explicit restrictions from other skills.
    """
    if not skills:
        return None

    allowed: set[str] = set()
    has_explicit_declaration = False
    for skill in skills:
        if skill.allowed_tools is None:
            continue
        has_explicit_declaration = True
        if not skill.allowed_tools:
            logger.info("Skill %s declared empty allowed-tools", skill.name)
        allowed.update(skill.allowed_tools)

    if not has_explicit_declaration:
        return None
    return allowed


def _tool_matches_declaration(tool_name: str, declaration: str) -> bool:
    """Whether a loaded tool name is covered by one allowed-tools declaration.

    Declarations may be exact tool names (``bash``) or bare MCP server names
    (``pkulaw``, ``yuandian-law``). MCP tool names are prefixed with the
    server name with hyphens normalized to underscores
    (``yuandian-law`` → ``yuandian_law_<tool>``, ``pacgate`` →
    ``pacgate_pacgate_<tool>`` because the bridge server itself is named
    ``pacgate`` and its tools carry the ``pacgate_`` tool-name prefix).
    Match exact, or the underscore-suffixed prefix of the normalized
    declaration, so ``qcc`` does not swallow a hypothetical ``qccother``.
    """
    if tool_name == declaration:
        return True
    normalized = declaration.replace("-", "_")
    return tool_name.startswith(f"{normalized}_")


def filter_tools_by_skill_allowed_tools[ToolT: NamedTool](
    tools: list[ToolT],
    skills: list[Skill],
    *,
    always_allowed_tool_names: set[str] | frozenset[str] = frozenset(),
) -> list[ToolT]:
    allowed = allowed_tool_names_for_skills(skills)
    if allowed is None:
        return tools

    allowed_with_framework_tools = allowed | set(always_allowed_tool_names)
    return [
        tool
        for tool in tools
        if any(_tool_matches_declaration(tool.name, declaration) for declaration in allowed_with_framework_tools)
    ]
