#!/bin/bash
# Post-restart debugging script for snowflake-mcp
# Run this after restarting Claude Code to diagnose the connection failure

echo "🔍 Reading snowflake-mcp debug log..."
echo ""

if [ -f /tmp/snowflake-mcp-debug.log ]; then
    cat /tmp/snowflake-mcp-debug.log
    echo ""
    echo "---"
    echo ""
else
    echo "❌ No debug log found at /tmp/snowflake-mcp-debug.log"
    echo "This means the wrapper script never executed, or failed before creating the log."
    echo ""
fi

echo "📊 Current MCP server status:"
claude mcp list

echo ""
echo "🔧 Next steps:"
echo "1. Review the debug log above"
echo "2. If you want to restore the original wrapper, run:"
echo "   git checkout .claude/mcp.json"
echo ""
echo "3. Or I can analyze the log and fix the issue"
