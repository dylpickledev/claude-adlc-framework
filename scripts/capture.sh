#!/bin/bash

# capture.sh - Intelligent idea capture with auto-organization
# Usage: ./scripts/capture.sh "idea description"
# Replaces: /ideate, /organize, /quarterly commands

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure we're in the repo root
cd "$REPO_ROOT"

# Input validation
if [ $# -eq 0 ]; then
    echo "Usage: ./scripts/capture.sh \"[idea description]\""
    echo "Example: ./scripts/capture.sh \"Build customer analytics dashboard\""
    exit 1
fi

IDEA="$1"

echo "🧠 Capturing idea: $IDEA"

# Use existing ideate-init.sh for the capture
if [ -f "$SCRIPT_DIR/ideate-init.sh" ]; then
    bash "$SCRIPT_DIR/ideate-init.sh" "$IDEA"
else
    echo "Error: ideate-init.sh not found"
    exit 1
fi

# Auto-organize if inbox has multiple ideas (3+ files)
INBOX_COUNT=$(find ideas/inbox -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

if [ "$INBOX_COUNT" -ge 3 ]; then
    echo ""
    echo "📊 Auto-organizing ideas (found $INBOX_COUNT ideas in inbox)..."

    if [ -f "$SCRIPT_DIR/ideate-organize.sh" ]; then
        bash "$SCRIPT_DIR/ideate-organize.sh"
        echo "✅ Ideas organized into themes"
    else
        echo "Warning: ideate-organize.sh not found, skipping auto-organization"
    fi
fi

echo ""
echo "✅ Idea captured successfully!"
echo "💡 Next steps:"
echo "   - Add more ideas: ./scripts/capture.sh \"[another idea]\""
echo "   - Plan roadmap: ./scripts/roadmap.sh [quarterly|sprint|annual]"
echo "   - Build top priority: ./scripts/build.sh [idea-name]"