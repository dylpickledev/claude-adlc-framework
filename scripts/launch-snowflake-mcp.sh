#!/bin/bash
# Snowflake MCP Launcher with Runtime Credential Injection (Portable)
# Week 1 Day 5 solution: Inject password into config at runtime (works around ${VAR} expansion issue)

set -e

# Self-locate the script and navigate to project root (PORTABLE PATTERN)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Create temporary config with actual password injected
TEMP_CONFIG=$(mktemp)

sed "s/PLACEHOLDER_REPLACED_AT_RUNTIME/$SNOWFLAKE_PASSWORD/g" config/snowflake_tools_config.yaml > "$TEMP_CONFIG"

# Launch Snowflake MCP with temp config
uvx snowflake-labs-mcp --service-config-file "$TEMP_CONFIG"

# Cleanup (won't run if MCP server keeps running, but that's okay)
rm -f "$TEMP_CONFIG"
