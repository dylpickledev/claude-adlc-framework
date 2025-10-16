#!/bin/bash
# Orchestra-MCP Launcher with Environment Variable Authentication
# Passes authentication via environment variables from 1Password

set -e

# Self-locate and navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Source 1Password secrets (provides ORCHESTRA_API_KEY)
if [ -f "$HOME/dotfiles/load-secrets-from-1password.sh" ]; then
    source "$HOME/dotfiles/load-secrets-from-1password.sh" 2>/dev/null || true
fi

# Map 1Password variable names to orchestra-mcp expected names
export ORCHESTRA_API_KEY="${ORCHESTRA_API_KEY}"
export ORCHESTRA_API_BASE_URL="https://app.getorchestra.io/api/engine/public/"

# Debug logging
echo "DEBUG: Launching Orchestra-MCP server" >> /tmp/orchestra-mcp-debug.log
echo "DEBUG: ORCHESTRA_API_KEY is set: ${ORCHESTRA_API_KEY:+yes}" >> /tmp/orchestra-mcp-debug.log
echo "DEBUG: ORCHESTRA_API_BASE_URL=$ORCHESTRA_API_BASE_URL" >> /tmp/orchestra-mcp-debug.log

# Launch orchestra-MCP from local project directory with Python 3.12
# (Python 3.13 has asyncio stdio bug)
ORCHESTRA_MCP_DIR="$PROJECT_ROOT/projects/active/feature-build-orchestra-mcp-server-enable-ai-agents-to-interact-with-orchestra-orchestration-platform-via-mcp-provides-tools-for-querying-pipeline-runs-task-runs-artifacts-and-triggering-pipelines-follows-dbtmcp-pattern-using-fastmcp-framework"
cd "$ORCHESTRA_MCP_DIR"
uvx --python 3.12 --from . orchestra-mcp
