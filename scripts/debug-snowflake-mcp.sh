#!/bin/bash
# Debug wrapper for snowflake-mcp to see what's failing
# Week 1 Day 5 diagnostics

# Get the directory where this script lives, then navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Log to file since MCP uses stdio
LOG_FILE="/tmp/snowflake-mcp-debug.log"
echo "=== Snowflake MCP Debug Log ===" > "$LOG_FILE"
echo "Started at: $(date)" >> "$LOG_FILE"

# Check environment
echo "Script dir: $SCRIPT_DIR" >> "$LOG_FILE"
echo "Project root: $PROJECT_ROOT" >> "$LOG_FILE"
echo "Working directory: $(pwd)" >> "$LOG_FILE"
echo "SNOWFLAKE_PASSWORD set: ${SNOWFLAKE_PASSWORD:+YES}" >> "$LOG_FILE"
echo "Config file exists: $(test -f config/snowflake_tools_config.yaml && echo YES || echo NO)" >> "$LOG_FILE"

# Try the sed replacement
TEMP_CONFIG=$(mktemp)
echo "Temp config: $TEMP_CONFIG" >> "$LOG_FILE"

if sed "s/PLACEHOLDER_REPLACED_AT_RUNTIME/$SNOWFLAKE_PASSWORD/g" config/snowflake_tools_config.yaml > "$TEMP_CONFIG" 2>>"$LOG_FILE"; then
  echo "✅ sed replacement succeeded" >> "$LOG_FILE"
  grep "password:" "$TEMP_CONFIG" | head -1 >> "$LOG_FILE"
else
  echo "❌ sed replacement failed" >> "$LOG_FILE"
  exit 1
fi

# Try to launch
echo "Launching uvx snowflake-labs-mcp..." >> "$LOG_FILE"
uvx snowflake-labs-mcp --service-config-file "$TEMP_CONFIG" 2>>"$LOG_FILE"
EXIT_CODE=$?

echo "Exit code: $EXIT_CODE" >> "$LOG_FILE"
rm -f "$TEMP_CONFIG"
exit $EXIT_CODE
