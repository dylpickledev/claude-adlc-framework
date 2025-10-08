#!/bin/bash
# Snowflake MCP Launcher with Environment Variable Authentication
# Passes authentication via environment variables (official method)

set -e

# Self-locate the script and navigate to project root (PORTABLE PATTERN)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Debug: Log auth configuration
echo "DEBUG: Launching Snowflake MCP with key pair authentication" >> /tmp/snowflake-mcp-debug.log
echo "DEBUG: SNOWFLAKE_ACCOUNT=$SNOWFLAKE_ACCOUNT" >> /tmp/snowflake-mcp-debug.log
echo "DEBUG: SNOWFLAKE_USER=$SNOWFLAKE_USER" >> /tmp/snowflake-mcp-debug.log
echo "DEBUG: SNOWFLAKE_PRIVATE_KEY_PATH=$SNOWFLAKE_PRIVATE_KEY_PATH" >> /tmp/snowflake-mcp-debug.log
echo "DEBUG: SNOWFLAKE_PRIVATE_KEY_PASSPHRASE is set: ${SNOWFLAKE_PRIVATE_KEY_PASSPHRASE:+yes}" >> /tmp/snowflake-mcp-debug.log

# Suppress Python warnings (Pydantic deprecation warnings break MCP stdio protocol)
# CRITICAL: Filter stderr to remove warnings while preserving stdout for MCP JSON-RPC protocol
# Strategy:
#   1. Save file descriptor 3 as a copy of stdout (for MCP protocol)
#   2. Redirect both stdout and stderr to filter
#   3. Filter out Pydantic warnings from stderr only
#   4. Restore stdout to original (fd 3) for MCP protocol

# Launch Snowflake MCP with service config and authentication via CLI arguments
# The service config file only defines which tools/services to enable
# Authentication is passed as CLI arguments using our environment variables
# Note: Database/schema/warehouse/role are configured in the service config file
{ PYTHONWARNINGS="ignore::DeprecationWarning" uvx snowflake-labs-mcp \
  --service-config-file config/snowflake_tools_config.yaml \
  --account "$SNOWFLAKE_ACCOUNT" \
  --user "$SNOWFLAKE_USER" \
  --private-key-file "$SNOWFLAKE_PRIVATE_KEY_PATH" \
  --private-key-file-pwd "$SNOWFLAKE_PRIVATE_KEY_PASSPHRASE" 2>&1 1>&3 | \
  grep -v "PydanticDeprecatedSince20" >&2; } 3>&1
