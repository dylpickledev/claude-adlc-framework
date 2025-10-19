#!/bin/bash

# monitor.sh - List all active tmux sessions for DA Agent Hub projects
# Usage: ./scripts/monitor.sh

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📱 Active DA Agent Hub Sessions${NC}"
echo ""

if ! command -v tmux &> /dev/null; then
    echo "❌ tmux not installed"
    exit 1
fi

# Get all tmux sessions
SESSIONS=$(tmux list-sessions 2>/dev/null)

if [ -z "$SESSIONS" ]; then
    echo "No active tmux sessions found"
    echo ""
    echo -e "${YELLOW}💡 Create a session:${NC}"
    echo "   /start [issue#|\"idea text\"]"
    exit 0
fi

echo -e "${GREEN}Active sessions:${NC}"
echo "$SESSIONS" | while IFS= read -r line; do
    SESSION_NAME=$(echo "$line" | cut -d: -f1)
    SESSION_INFO=$(echo "$line" | cut -d: -f2-)

    # Highlight feature sessions
    if [[ "$SESSION_NAME" == feature-* ]]; then
        echo -e "  ${GREEN}●${NC} $SESSION_NAME $SESSION_INFO"
    else
        echo -e "  ${BLUE}○${NC} $SESSION_NAME $SESSION_INFO"
    fi
done

echo ""
echo -e "${YELLOW}📱 Connect from iPhone:${NC}"
echo "   ssh dylanmorrish@macbook-fair"
echo "   tmux attach -t <session-name>"
echo ""
echo -e "${YELLOW}💻 Connect locally:${NC}"
echo "   tmux attach -t <session-name>"
echo ""
