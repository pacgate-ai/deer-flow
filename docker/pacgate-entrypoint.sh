#!/bin/sh
set -e

# PacGate-Law all-in-one container entrypoint
# Starts: backend (uvicorn) + frontend (Next.js) + nginx (reverse proxy)
#
# Config files are expected at:
#   /app/config/config.yaml
#   /app/config/extensions_config.json
#   /app/config/.env          (sourced if present)
#   /app/agents/               (5 role-tier agent dirs with SOUL.md + config.yaml)
#
# If agent templates are not mounted, the baked-in defaults from
# /app/agents-templates/ are copied to /app/agents/ on first start.

echo "=== PacGate-Law Container Starting ==="

# Source .env if present
if [ -f /app/config/.env ]; then
    echo "Loading .env from /app/config/.env"
    set -a
    . /app/config/.env
    set +a
fi

# Initialize agent templates if /app/agents is empty
if [ ! -d /app/agents/sylvie ] && [ -d /app/agents-templates/sylvie ]; then
    echo "Initializing agent templates from baked-in defaults..."
    cp -r /app/agents-templates/* /app/agents/
elif [ ! -d /app/agents/sylvie ]; then
    echo "WARNING: No agent templates found in /app/agents. Please mount .deer-flow/users/default/agents/ as /app/agents."
fi

# Link .deer-flow agents if the data dir exists
if [ -d /app/agents ]; then
    mkdir -p /app/data/users/default
    ln -sf /app/agents /app/data/users/default/agents
fi

# Configure nginx
echo "Configuring nginx..."
cp /etc/nginx/nginx.conf.template /etc/nginx/nginx.conf
test -e /proc/net/if_inet6 || sed -i '/^[[:space:]]*listen[[:space:]]\+\[::\]:2026[[:space:]]/d' /etc/nginx/nginx.conf

# Start backend
echo "Starting backend (Gateway API on :8001)..."
cd /app/backend
PYTHONPATH=/app/backend uv run --no-sync uvicorn app.gateway.app:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to start..."
for i in $(seq 1 30); do
    if wget -q -O- http://localhost:8001/health 2>/dev/null | grep -q "healthy"; then
        echo "Backend is healthy."
        break
    fi
    sleep 1
done

# Start frontend
echo "Starting frontend (Next.js on :3000)..."
cd /app/frontend
node node_modules/.bin/next start -p 3000 &
FRONTEND_PID=$!

# Start nginx
echo "Starting nginx on :2026..."
nginx -g 'daemon off;' &
NGINX_PID=$!

echo "=== PacGate-Law is running ==="
echo "  Unified endpoint: http://localhost:2026"
echo "  Gateway API:      http://localhost:8001"
echo "  Frontend:         http://localhost:3000"

# Wait for any process to exit
trap "kill $BACKEND_PID $FRONTEND_PID $NGINX_PID 2>/dev/null; exit 0" TERM INT
wait