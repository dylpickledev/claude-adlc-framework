#!/bin/bash

# roadmap.sh - Strategic planning and prioritization
# Usage: ./scripts/roadmap.sh [timeframe]
# Replaces: /quarterly and manual prioritization workflows

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure we're in the repo root
cd "$REPO_ROOT"

# Default to quarterly if no timeframe specified
TIMEFRAME="${1:-quarterly}"

echo "🗺️  Creating $TIMEFRAME roadmap..."

# Ensure roadmaps directory exists
mkdir -p ideas/roadmaps

# Get current date for filename
DATE=$(date +%Y-%m)
ROADMAP_FILE="ideas/roadmaps/${TIMEFRAME}-${DATE}.md"

# Check if we have organized ideas to work with
if [ ! -d "ideas/organized" ] || [ -z "$(find ideas/organized -name "*.md" 2>/dev/null)" ]; then
    echo "⚠️  No organized ideas found."
    echo "💡 Try running: ./scripts/capture.sh \"[your idea]\" first"
    exit 1
fi

# Create roadmap template
cat > "$ROADMAP_FILE" << EOF
# ${TIMEFRAME^} Roadmap - $(date +"%B %Y")

## Overview
Strategic planning session for ${TIMEFRAME} execution priorities.

## Ideas Analysis

### Available Ideas
EOF

# List organized ideas with basic analysis
echo "Analyzing organized ideas..."
for category_dir in ideas/organized/*/; do
    if [ -d "$category_dir" ]; then
        category=$(basename "$category_dir")
        echo "" >> "$ROADMAP_FILE"
        echo "#### $category" >> "$ROADMAP_FILE"

        for idea_file in "$category_dir"*.md; do
            if [ -f "$idea_file" ]; then
                idea_name=$(basename "$idea_file" .md)
                # Extract first line as summary
                summary=$(head -n 1 "$idea_file" | sed 's/^# *//')
                echo "- **$idea_name**: $summary" >> "$ROADMAP_FILE"
            fi
        done
    fi
done

# Add prioritization framework
cat >> "$ROADMAP_FILE" << EOF

## Prioritization Framework

### Impact vs Effort Analysis
Use this matrix to evaluate each idea:

| Idea | Impact (1-5) | Effort (1-5) | Priority Score | Notes |
|------|-------------|-------------|----------------|-------|
| [idea-name] | [rating] | [rating] | [calculated] | [reasoning] |

### Priority Categories
- **High Priority**: High impact, low-medium effort (quick wins + strategic)
- **Medium Priority**: Medium impact, any effort OR high impact, high effort
- **Low Priority**: Low impact, any effort OR parking lot items

### Dependencies & Sequencing
- List any dependencies between ideas
- Identify which ideas should be tackled first
- Note any blockers or prerequisites

## Execution Plan

### ${TIMEFRAME^} Goals
1. [Primary goal from high priority items]
2. [Secondary goal]
3. [Tertiary goal]

### Ready to Build
Ideas that are ready for immediate execution:
- [ ] [idea-name] - [brief description]

### Future Considerations
Ideas for next planning cycle:
- [ ] [idea-name] - [brief description]

## Notes
- Planning date: $(date)
- Review date: [set future review date]
- Stakeholders: [list key stakeholders]
EOF

echo "✅ Roadmap created: $ROADMAP_FILE"
echo ""
echo "📋 Next steps:"
echo "   1. Review and fill in the prioritization matrix"
echo "   2. Identify top 2-3 ideas for execution"
echo "   3. Build highest priority: ./scripts/build.sh [idea-name]"
echo ""
echo "💡 Tip: Open the roadmap file to complete the prioritization analysis"