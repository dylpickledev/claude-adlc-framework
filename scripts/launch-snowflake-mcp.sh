#!/bin/bash
# Snowflake MCP Launcher with Runtime Credential Injection + Debug Logging
# Week 1 Day 5 solution: Inject password into config at runtime (works around ${VAR} expansion issue)

set -e

# Debug logging
DEBUG_LOG="/tmp/snowflake-mcp-debug.log"
exec 2> >(tee -a "$DEBUG_LOG")

echo "=== Snowflake MCP Launch Debug Log ===" >&2
echo "Timestamp: $(date)" >&2
echo "Working directory: $(pwd)" >&2
echo "SNOWFLAKE_PASSWORD set: ${SNOWFLAKE_PASSWORD:+YES}" >&2
echo "" >&2

# Create temporary config with actual password injected
TEMP_CONFIG=$(mktemp)
echo "Created temp config: $TEMP_CONFIG" >&2

sed "s/PLACEHOLDER_REPLACED_AT_RUNTIME/$SNOWFLAKE_PASSWORD/g" config/snowflake_tools_config.yaml > "$TEMP_CONFIG"
echo "Password injected into config" >&2

echo "Launching Snowflake MCP..." >&2
# Launch Snowflake MCP with temp config
uvx snowflake-labs-mcp --service-config-file "$TEMP_CONFIG"

# Cleanup (won't run if MCP server keeps running, but that's okay)
rm -f "$TEMP_CONFIG"
