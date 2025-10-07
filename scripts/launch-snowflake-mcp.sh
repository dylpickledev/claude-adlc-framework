#!/bin/bash
# Snowflake MCP Launcher with Runtime Credential Injection
# This script injects the Snowflake password from environment variable into the config
# before launching the MCP server

set -e

# Create temporary config with actual password
TEMP_CONFIG=$(mktemp)
sed "s/PLACEHOLDER_REPLACED_AT_RUNTIME/$SNOWFLAKE_PASSWORD/g" config/snowflake_tools_config.yaml > "$TEMP_CONFIG"

# Launch Snowflake MCP with temp config (no --connection-name needed, it reads from YAML)
uvx snowflake-labs-mcp --service-config-file "$TEMP_CONFIG"

# Cleanup (this won't run if MCP server keeps running, but that's okay)
rm -f "$TEMP_CONFIG"
