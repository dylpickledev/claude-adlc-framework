#!/bin/bash

# ideate-organize.sh - Trigger AI organization of inbox ideas
# Usage: ./scripts/ideate-organize.sh

set -e

# Configuration
IDEAS_DIR="ideas"
INBOX_DIR="$IDEAS_DIR/inbox"
ORGANIZED_DIR="$IDEAS_DIR/organized"
ARCHIVE_DIR="$IDEAS_DIR/archive"

# Ensure directories exist
mkdir -p "$INBOX_DIR" "$ORGANIZED_DIR" "$ARCHIVE_DIR"

# Check if there are ideas to organize
INBOX_COUNT=$(find "$INBOX_DIR" -name "*.md" 2>/dev/null | wc -l)

if [ "$INBOX_COUNT" -eq 0 ]; then
    echo "📭 No ideas found in inbox to organize"
    echo "💡 Use 'claude /ideate \"concept\"' to capture ideas first"
    exit 0
fi

echo "🧠 Found $INBOX_COUNT ideas in inbox"
echo "🔄 Triggering AI organization process..."

# List ideas for reference
echo ""
echo "📋 Ideas to be organized:"
find "$INBOX_DIR" -name "*.md" -exec basename {} \; | sort

echo ""
echo "🤖 Now run: claude /organize"
echo ""
echo "This will:"
echo "  - Analyze all inbox ideas for common themes"
echo "  - Create clustered groups in $ORGANIZED_DIR"
echo "  - Generate priority and complexity assessments"
echo "  - Recommend specialist agent analysis"
echo "  - Move processed ideas to archive with references"
echo ""
echo "⏳ AI organization may take a few minutes for large idea sets"