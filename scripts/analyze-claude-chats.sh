#!/bin/bash

# analyze-claude-chats.sh - User-agnostic Claude chat analysis for agent training
# Usage: ./scripts/analyze-claude-chats.sh [options]
# Automatically detects Claude project directory based on current repository path

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure we're in the repo root
cd "$REPO_ROOT"

# Auto-detect Claude project directory
REPO_PATH="$REPO_ROOT"
CLAUDE_PROJECT_DIR="$HOME/.claude/projects/$(echo "$REPO_PATH" | sed 's/\//-/g')"

echo "🔍 DA Agent Hub - Claude Chat Analysis"
echo "Repository: $REPO_PATH"
echo "Expected Claude directory: $CLAUDE_PROJECT_DIR"
echo ""

# Check if Claude is installed
if [ ! -d "$HOME/.claude" ]; then
    echo "❌ Claude Code not found at ~/.claude"
    echo "💡 Install Claude Code to enable chat analysis and agent training"
    exit 1
fi

# Check if project directory exists
if [ ! -d "$CLAUDE_PROJECT_DIR" ]; then
    echo "❌ No Claude conversations found for this repository"
    echo "💡 Use Claude Code in this repository to generate training data"
    echo "Expected location: $CLAUDE_PROJECT_DIR"
    exit 1
fi

# Count conversations
CHAT_COUNT=$(ls "$CLAUDE_PROJECT_DIR"/*.jsonl 2>/dev/null | wc -l | tr -d ' ')

if [ "$CHAT_COUNT" -eq 0 ]; then
    echo "❌ No conversation files found in Claude project directory"
    echo "💡 Continue using Claude Code to build training data"
    exit 1
fi

echo "✅ Found $CHAT_COUNT Claude conversations for analysis"
echo ""

# Check if Python analyzer exists
PYTHON_ANALYZER="$SCRIPT_DIR/analyze_chats.py"
if [ ! -f "$PYTHON_ANALYZER" ]; then
    echo "❌ Python analyzer not found: $PYTHON_ANALYZER"
    echo "💡 Run this script from the da-agent-hub repository root"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "knowledge/da-agent-hub/training/analysis-results"

# Run Python analysis
echo "🔬 Analyzing conversations for agent training insights..."
python3 "$PYTHON_ANALYZER" "$CLAUDE_PROJECT_DIR" "$REPO_ROOT"

echo ""
echo "✅ Chat analysis complete!"
echo "📊 Results stored in: knowledge/da-agent-hub/training/analysis-results/"
echo "🎯 Use insights to improve agent effectiveness with separate PRs"