#!/usr/bin/env python3
"""Check Sylvie agent memory and config inside running container."""
import os, json

base = '/app/backend/.deer-flow'

print('=== MEMORY STORAGE ===')
users_dir = os.path.join(base, 'users')
if os.path.isdir(users_dir):
    for user in sorted(os.listdir(users_dir)):
        user_path = os.path.join(users_dir, user)
        if os.path.isdir(user_path):
            mem_path = os.path.join(user_path, 'memory.json')
            if os.path.exists(mem_path):
                with open(mem_path) as f:
                    mem = json.load(f)
                count = len(mem) if isinstance(mem, list) else len(str(mem))
                print(f'  user={user}: memory.json exists, {count} entries')
            else:
                print(f'  user={user}: no memory.json yet (created on first interaction)')
            # Check agent dirs
            agents_dir = os.path.join(user_path, 'agents')
            if os.path.isdir(agents_dir):
                for a in sorted(os.listdir(agents_dir)):
                    print(f'    agent: {a}')
else:
    print('  users/ dir does not exist yet')

global_mem = os.path.join(base, 'memory.json')
print(f'  global memory.json: {os.path.exists(global_mem)}')
user_md = os.path.join(base, 'USER.md')
print(f'  global USER.md: {os.path.exists(user_md)}')

print()
print('=== SYLVIE AGENT DIR ===')
sylvie_dir = os.path.join(base, 'users/default/agents/sylvie')
if os.path.isdir(sylvie_dir):
    for item in sorted(os.listdir(sylvie_dir)):
        full = os.path.join(sylvie_dir, item)
        if os.path.isfile(full):
            print(f'  {item}: {os.path.getsize(full)} bytes')
        else:
            print(f'  {item}/ (dir)')
else:
    print('  sylvie dir does not exist')

print()
print('=== RESOLVED CONFIG ===')
from deerflow.config.app_config import get_app_config
cfg = get_app_config()
print(f'  memory.enabled: {cfg.memory.enabled}')
print(f'  memory.injection_enabled: {cfg.memory.injection_enabled}')
print(f'  memory.manager_class: {cfg.memory.manager_class}')
print(f'  memory.mode: {cfg.memory.mode}')
bc = cfg.memory.backend_config
print(f'  memory.backend_config.model: {bc.get("model", {}).get("model", "N/A")}')
print(f'  memory.backend_config.token_counting: {bc.get("token_counting")}')
print(f'  memory.backend_config.max_facts: {bc.get("max_facts")}')
print(f'  agents_api.enabled: {cfg.agents_api.enabled}')
print(f'  acp_agents: {list(cfg.acp_agents.keys())}')
print(f'  scheduler.enabled: {cfg.scheduler.enabled}')
print(f'  sandbox.use: {cfg.sandbox.use}')

print()
print('=== SYLVIE AGENT LOADED ===')
from deerflow.config.agents_config import load_agent_config, load_agent_soul
try:
    ac = load_agent_config('sylvie')
    if ac:
        print(f'  name: {ac.name}')
        print(f'  model: {ac.model}')
        print(f'  description: {str(ac.description)[:60]}')
        print(f'  skills: {ac.skills}')
        print(f'  tool_groups: {ac.tool_groups}')
    else:
        print('  Agent config returned None')
except Exception as e:
    print(f'  ERROR loading config: {e}')

try:
    soul = load_agent_soul('sylvie')
    if soul:
        print(f'  SOUL.md loaded: {len(soul)} chars')
        print(f'  SOUL.md preview: {soul[:80]}...')
    else:
        print('  SOUL.md returned None')
except Exception as e:
    print(f'  ERROR loading soul: {e}')

print()
print('=== DONE ===')