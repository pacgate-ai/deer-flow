#!/usr/bin/env python3
"""Smoke test all MCP servers — check config, env vars, and connectivity."""
import json
import os
import subprocess
import time

with open("/app/backend/extensions_config.json") as f:
    ext = json.load(f)

mcps = ext.get("mcpServers", {})

print("=" * 70)
print("MCP SERVER SMOKE TEST")
print("=" * 70)

results = []

for name, conf in sorted(mcps.items()):
    enabled = conf.get("enabled", True)
    typ = conf.get("type", "stdio")
    desc = conf.get("description", "")[:50]

    # Check env vars / headers for API keys
    env = conf.get("env", {})
    headers = conf.get("headers", {})
    all_vars = {**env, **headers}
    missing_keys = []
    set_keys = []

    for k, v in all_vars.items():
        if isinstance(v, str) and "$" in v:
            # Extract var name from $VAR or ${VAR}
            var_name = v.replace("$", "").replace("{", "").replace("}", "")
            val = os.environ.get(var_name, "")
            if val:
                set_keys.append(var_name)
            else:
                missing_keys.append(var_name)

    status = "ENABLED" if enabled else "DISABLED"
    key_status = "OK" if not missing_keys else f"MISSING: {', '.join(missing_keys)}"

    print(f"\n[{name}]")
    print(f"  status: {status}")
    print(f"  type: {typ}")
    print(f"  desc: {desc}")
    print(f"  keys: {key_status}")

    if not enabled:
        results.append((name, "DISABLED", "n/a"))
        continue

    # For stdio servers, try to start the process briefly
    if typ == "stdio":
        command = conf.get("command", "")
        args = conf.get("args", [])
        cmd_str = f"{command} {' '.join(args)}"

        print(f"  cmd: {cmd_str}")

        # Check if command exists
        which = subprocess.run(
            f"which {command}", shell=True, capture_output=True, text=True
        )
        if which.returncode != 0:
            print(f"  ❌ binary not found: {command}")
            results.append((name, "FAIL", f"binary not found: {command}"))
            continue

        # For officecli and markitdown, try a quick version check
        if command == "officecli":
            r = subprocess.run(
                f"{command} --version", shell=True, capture_output=True, text=True, timeout=10
            )
            if r.returncode == 0:
                ver = r.stdout.strip().split("\n")[0]
                print(f"  ✅ version: {ver}")
                results.append((name, "PASS", f"v{ver}"))
            else:
                err = r.stderr.strip()[:100]
                print(f"  ⚠ version check failed: {err}")
                results.append((name, "WARN", err))
        elif command == "python":
            # markitdown_mcp
            r = subprocess.run(
                f"{command} -m markitdown_mcp --help",
                shell=True, capture_output=True, text=True, timeout=10
            )
            if r.returncode == 0:
                print(f"  ✅ markitdown_mcp starts")
                results.append((name, "PASS", "starts ok"))
            else:
                print(f"  ⚠ markitdown_mcp failed: {r.stderr[:100]}")
                results.append((name, "WARN", r.stderr[:100]))
        elif command == "uvx":
            # sec-edgar / vaquill — just check uvx exists
            print(f"  ✅ uvx available (will download on first use)")
            results.append((name, "PASS", "uvx available"))
        else:
            print(f"  ✅ binary found at: {which.stdout.strip()}")
            results.append((name, "PASS", "binary found"))

    elif typ == "http":
        url = conf.get("url", "")
        print(f"  url: {url}")

        if missing_keys:
            print(f"  ⚠ cannot test — API key missing")
            results.append((name, "WARN", f"missing keys: {', '.join(missing_keys)}"))
        else:
            # Try a quick HTTP connection (just check if server responds)
            import urllib.request
            try:
                req = urllib.request.Request(url, method="HEAD")
                # Add auth header
                for k, v in headers.items():
                    if isinstance(v, str) and "$" in v:
                        var_name = v.replace("$", "").replace("{", "").replace("}", "")
                        val = os.environ.get(var_name, "")
                        req.add_header(k, v.replace(f"${var_name}", val).replace(f"${{{var_name}}}", val))
                    else:
                        req.add_header(k, v)

                r = urllib.request.urlopen(req, timeout=10)
                print(f"  ✅ HTTP {r.status}")
                results.append((name, "PASS", f"HTTP {r.status}"))
            except Exception as e:
                err_str = str(e)[:100]
                print(f"  ⚠ HTTP error: {err_str}")
                results.append((name, "WARN", err_str))

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"{'Server':<25} {'Status':<8} {'Detail'}")
print("-" * 70)
for name, status, detail in results:
    icon = "✅" if status == "PASS" else ("⚠" if status == "WARN" else ("❌" if status == "FAIL" else "⏸"))
    print(f"{icon} {name:<23} {status:<8} {detail}")

print("\n" + "=" * 70)
print("API KEYS NEEDED IN .env")
print("=" * 70)
needed = [
    ("YUANDIAN_API_KEY", "元典 — get from open.chineselaw.com developer console"),
    ("PKULAW_BEARER_TOKEN", "北大法宝 — get after institutional license purchase"),
    ("QCC_API_KEY", "企查查 — get from agent.qcc.com/profile/api-key"),
    ("SEC_EDGAR_USER_AGENT", "SEC EDGAR — free, format: 'Your Name (email@domain.com)'"),
    ("COURTLISTENER_API_KEY", "CourtListener — free, from courtlistener.com/help/api/rest/ (disabled)"),
    ("VAQUILL_API_KEY", "Vaquill — from vaquill.ai/settings (disabled)"),
]
for var, desc in needed:
    val = os.environ.get(var, "")
    status = "✅ SET" if val else "❌ EMPTY"
    print(f"  {status} {var:<25} {desc}")