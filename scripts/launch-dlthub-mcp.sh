#!/bin/bash
# Launch dlthub-MCP server with dlt+ license from 1Password
# Follows dbt-mcp pattern: load secrets, launch with uv, debug logging

set -e

# Self-locate script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Debug log
DEBUG_LOG="/tmp/dlthub-mcp-debug.log"
echo "DEBUG: Launching dlthub-MCP server" >> "$DEBUG_LOG"

# Load secrets from 1Password (provides DLTHUB_LICENSE_KEY)
source "$HOME/dotfiles/load-secrets-from-1password.sh" >> "$DEBUG_LOG" 2>&1

# Verify license key is set
if [ -z "$DLTHUB_LICENSE_KEY" ]; then
    echo "ERROR: DLTHUB_LICENSE_KEY not set - check 1Password configuration" >> "$DEBUG_LOG"
    echo "ERROR: DLTHUB_LICENSE_KEY not set - check 1Password configuration" >&2
    exit 1
fi

echo "DEBUG: DLTHUB_LICENSE_KEY is set: yes" >> "$DEBUG_LOG"

# Launch dlthub MCP server with dlt+ license
# Using uv tool runner with dlt-plus[mcp] package
# Per dlthub docs: https://dlthub.com/docs/hub/features/mcp-server
# IMPORTANT: Use 'run_plus' for licensed version (not 'run')
exec uvx --from "dlt-plus[mcp]==0.9.0" dlt mcp run_plus 2>> "$DEBUG_LOG"
