#!/bin/bash
# MCP Health Check - Verify all MCP servers at session startup
# Called automatically at the beginning of Claude Code sessions to ensure tools work

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Self-locate script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              MCP Server Health Check                      ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Claude MCP command is available
if ! command -v claude &> /dev/null; then
    echo -e "${RED}✗ Claude Code CLI not found${NC}"
    echo "  Cannot verify MCP server status"
    exit 1
fi

# Get MCP server status
echo -e "${BLUE}Checking MCP server connections...${NC}"
echo ""

MCP_OUTPUT=$(claude mcp list 2>&1)

# Parse output and track failures
TOTAL_SERVERS=0
CONNECTED_SERVERS=0
FAILED_SERVERS=0
KNOWN_ISSUES=0

# Known failing servers (expected failures)
KNOWN_FAILING=(
    "snowflake-mcp"  # Known authentication issue
)

# Parse each server status
while IFS= read -r line; do
    if [[ $line =~ ^([a-zA-Z0-9_-]+):.*-[[:space:]]*(✓|✗)[[:space:]]*(Connected|Failed) ]]; then
        server="${BASH_REMATCH[1]}"
        status="${BASH_REMATCH[2]}"

        TOTAL_SERVERS=$((TOTAL_SERVERS + 1))

        # Check if this is a known issue
        is_known=false
        for known in "${KNOWN_FAILING[@]}"; do
            if [ "$server" = "$known" ]; then
                is_known=true
                break
            fi
        done

        if [ "$status" = "✓" ]; then
            echo -e "  ${GREEN}✓${NC} $server"
            CONNECTED_SERVERS=$((CONNECTED_SERVERS + 1))
        else
            if [ "$is_known" = true ]; then
                echo -e "  ${YELLOW}⚠${NC} $server ${YELLOW}(known issue)${NC}"
                KNOWN_ISSUES=$((KNOWN_ISSUES + 1))
            else
                echo -e "  ${RED}✗${NC} $server ${RED}(UNEXPECTED FAILURE)${NC}"
                FAILED_SERVERS=$((FAILED_SERVERS + 1))
            fi
        fi
    fi
done <<< "$MCP_OUTPUT"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

# Summary
if [ $FAILED_SERVERS -eq 0 ]; then
    echo -e "${GREEN}✓ All expected MCP servers are connected${NC}"
    echo -e "  Connected: $CONNECTED_SERVERS/$TOTAL_SERVERS"
    if [ $KNOWN_ISSUES -gt 0 ]; then
        echo -e "  Known issues: $KNOWN_ISSUES (expected)"
    fi
    echo ""
    echo -e "${CYAN}MCP tools are ready to use!${NC}"
    exit 0
else
    echo -e "${RED}✗ UNEXPECTED MCP SERVER FAILURES DETECTED${NC}"
    echo -e "  Connected: $CONNECTED_SERVERS/$TOTAL_SERVERS"
    echo -e "  Failed (unexpected): ${RED}$FAILED_SERVERS${NC}"
    if [ $KNOWN_ISSUES -gt 0 ]; then
        echo -e "  Known issues: $KNOWN_ISSUES (expected)"
    fi
    echo ""
    echo -e "${YELLOW}Troubleshooting steps:${NC}"
    echo "  1. Check debug logs: tail /tmp/*-mcp-debug.log"
    echo "  2. Verify credentials: Check 1Password secrets are loaded"
    echo "  3. Test launch scripts: bash scripts/launch-<server>-mcp.sh"
    echo "  4. See runbook: .claude/memory/patterns/mcp-troubleshooting-runbook.md"
    echo ""
    exit 1
fi
