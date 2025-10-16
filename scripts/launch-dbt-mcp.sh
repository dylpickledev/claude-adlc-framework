#!/bin/bash
# dbt-MCP Launcher with Environment Variable Authentication
# Passes authentication via environment variables from 1Password

set -e

# Self-locate the script and navigate to project root (PORTABLE PATTERN)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Source 1Password secrets (provides DBT_CLOUD_API_TOKEN, DBT_CLOUD_ACCOUNT_ID)
if [ -f "$HOME/dotfiles/load-secrets-from-1password.sh" ]; then
    source "$HOME/dotfiles/load-secrets-from-1password.sh" 2>/dev/null || true
fi

# Map 1Password variable names to dbt-mcp expected names
export DBT_HOST="te240.us1.dbt.com"  # Multi-tenant instance (not cloud.getdbt.com)
export DBT_TOKEN="${DBT_CLOUD_API_TOKEN}"
export DBT_PROD_ENV_ID="${DBT_CLOUD_PROD_ENV_ID:-12333}"  # Default from .env.template
export DBT_PATH="/usr/local/bin/dbt"
# DBT_PROJECT_DIR is already set by 1Password

# Debug: Log configuration (helps troubleshoot connection issues)
echo "DEBUG: Launching dbt-MCP server" >> /tmp/dbt-mcp-debug.log
echo "DEBUG: DBT_HOST=$DBT_HOST" >> /tmp/dbt-mcp-debug.log
echo "DEBUG: DBT_TOKEN is set: ${DBT_TOKEN:+yes}" >> /tmp/dbt-mcp-debug.log
echo "DEBUG: DBT_PROD_ENV_ID=$DBT_PROD_ENV_ID" >> /tmp/dbt-mcp-debug.log
echo "DEBUG: DBT_PATH=$DBT_PATH" >> /tmp/dbt-mcp-debug.log
echo "DEBUG: DBT_PROJECT_DIR=$DBT_PROJECT_DIR" >> /tmp/dbt-mcp-debug.log

# Launch dbt-MCP with Python 3.12 (Python 3.13 has asyncio stdio bug)
# Environment variables are inherited from shell (loaded by 1Password)
uvx --python 3.12 dbt-mcp
