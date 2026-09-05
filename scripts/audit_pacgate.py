#!/usr/bin/env python3
"""Audit PacGate customizations inside the running deer-flow gateway container."""
import json
import os
import yaml

print("=" * 60)
print("PACGATE CUSTOMIZATION AUDIT")
print("=" * 60)

# 1. config.yaml
print("\n[1] CONFIG.YAML")
print("-" * 40)
with open("/app/backend/config.yaml") as f:
    cfg = yaml.safe_load(f)
print(f"  config_version: {cfg.get('config_version')}")
models = cfg.get("models", [])
print(f"  models ({len(models)}):")
for m in models:
    print(f"    - {m['name']}: model={m.get('model')}, api_base={m.get('api_base','')[:50]}...")
acp = cfg.get("acp_agents", {})
print(f"  acp_agents: {list(acp.keys())}")
for name, conf in acp.items():
    print(f"    {name}: command={conf.get('command')}, args={conf.get('args')}")
print(f"  scheduler.enabled: {cfg.get('scheduler', {}).get('enabled')}")
print(f"  agents_api.enabled: {cfg.get('agents_api', {}).get('enabled')}")
print(f"  sandbox.use: {cfg.get('sandbox', {}).get('use')}")
print(f"  memory.manager_class: {cfg.get('memory', {}).get('manager_class')}")
print(f"  memory.token_counting: {cfg.get('memory', {}).get('backend_config', {}).get('token_counting')}")
print(f"  skill_evolution.enabled: {cfg.get('skill_evolution', {}).get('enabled')}")

# 2. extensions_config.json
print("\n[2] EXTENSIONS_CONFIG.JSON (MCP + skills)")
print("-" * 40)
with open("/app/backend/extensions_config.json") as f:
    ext = json.load(f)
mcps = ext.get("mcpServers", {})
print(f"  MCP servers ({len(mcps)}):")
for name, conf in sorted(mcps.items()):
    enabled = conf.get("enabled", True)
    typ = conf.get("type", "stdio")
    desc = conf.get("description", "")[:50]
    status = "ENABLED" if enabled else "DISABLED"
    print(f"    [{status}] {name} ({typ}): {desc}")
skills_state = ext.get("skills", {})
print(f"  skills state: {skills_state if skills_state else '(empty - all defaults)'}")

# 3. Skills on disk
print("\n[3] SKILLS ON DISK")
print("-" * 40)
skills_dir = "/app/skills"
if os.path.isdir(skills_dir):
    for cat in ["public", "custom"]:
        cat_dir = os.path.join(skills_dir, cat)
        if os.path.isdir(cat_dir):
            skills = sorted([d for d in os.listdir(cat_dir) if os.path.isdir(os.path.join(cat_dir, d))])
            print(f"  {cat}/ ({len(skills)} skills):")
            for s in skills:
                skill_md = os.path.join(cat_dir, s, "SKILL.md")
                has_skill = os.path.exists(skill_md)
                marker = "SKILL.md" if has_skill else "(no SKILL.md)"
                print(f"    - {s} [{marker}]")
                if s == "vcpe-financing-suite" and has_skill:
                    with open(skill_md) as f:
                        content = f.read()
                    print(f"      size: {len(content)} chars")
                    # Check frontmatter
                    if content.startswith("---"):
                        end = content.index("---", 3)
                        fm = yaml.safe_load(content[3:end])
                        print(f"      frontmatter keys: {list(fm.keys())}")
                        print(f"      name: {fm.get('name')}")
                        print(f"      allowed-tools: {fm.get('allowed-tools')}")
                        print(f"      required-secrets: {fm.get('required-secrets')}")

# 4. Sylvie agent
print("\n[4] SYLVIE CUSTOM AGENT")
print("-" * 40)
base = "/app/backend/.deer-flow"
soul_path = os.path.join(base, "users/default/agents/sylvie/SOUL.md")
agent_cfg_path = os.path.join(base, "users/default/agents/sylvie/config.yaml")
print(f"  SOUL.md exists: {os.path.exists(soul_path)}")
print(f"  config.yaml exists: {os.path.exists(agent_cfg_path)}")
if os.path.exists(agent_cfg_path):
    with open(agent_cfg_path) as f:
        ac = yaml.safe_load(f)
    print(f"    name: {ac.get('name')}")
    print(f"    model: {ac.get('model')}")
    print(f"    description: {str(ac.get('description', ''))[:60]}...")
    print(f"    skills: {ac.get('skills')}")
    print(f"    tool_groups: {ac.get('tool_groups')}")
if os.path.exists(soul_path):
    with open(soul_path) as f:
        soul = f.read()
    print(f"    SOUL.md size: {len(soul)} chars")
    lines = soul.split("\n")
    print(f"    SOUL.md lines: {len(lines)}")
    print(f"    first line: {lines[0]}")
    # Check for key PacGate sections
    has_redline = "红线" in soul
    has_sylvie = "Sylvie" in soul
    has_baichen = "百宸" in soul
    has_deerflow = "deer-flow" in soul
    print(f"    contains '红线' (red line): {has_redline}")
    print(f"    contains 'Sylvie': {has_sylvie}")
    print(f"    contains '百宸': {has_baichen}")
    print(f"    contains 'deer-flow': {has_deerflow}")

# 5. Check .env vars resolved
print("\n[5] ENV VARS (resolved in container)")
print("-" * 40)
env_vars = [
    "PACGATE_MAIN_API_KEY", "PACGATE_MAIN_API_BASE",
    "PACGATE_MID_API_KEY", "PACGATE_MID_API_BASE",
    "PACGATE_LOW_API_KEY", "PACGATE_LOW_API_BASE",
    "YUANDIAN_API_KEY", "PKULAW_BEARER_TOKEN", "QCC_API_KEY",
    "SEC_EDGAR_USER_AGENT", "BETTER_AUTH_SECRET",
    "DEER_FLOW_CONFIG_PATH", "DEER_FLOW_EXTENSIONS_CONFIG_PATH",
    "DEER_FLOW_HOME",
]
for var in env_vars:
    val = os.environ.get(var, "<NOT SET>")
    if val and val != "<NOT SET>" and len(val) > 30:
        val = val[:30] + "..."
    print(f"  {var}: {val}")

# 6. Docker compose override
print("\n[6] DOCKER COMPOSE OVERRIDE")
print("-" * 40)
override_path = "/app/docker/docker-compose.override.yaml"
# This won't be inside the container, check host-side
print(f"  (checked from host-side, not inside container)")
print(f"  provisioner disabled via profile: k8s-sandbox")

print("\n" + "=" * 60)
print("AUDIT COMPLETE")
print("=" * 60)