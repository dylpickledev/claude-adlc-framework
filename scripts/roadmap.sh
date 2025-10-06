#!/bin/bash

# roadmap.sh - Strategic planning and prioritization using GitHub Issues
# Usage: ./scripts/roadmap.sh [timeframe]
# Analyzes GitHub issues with 'idea' label for strategic planning

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure we're in the repo root
cd "$REPO_ROOT"

# Default to quarterly if no timeframe specified
TIMEFRAME="${1:-quarterly}"

echo "🗺️  Creating $TIMEFRAME roadmap from GitHub issues..."

# Ensure roadmaps directory exists
mkdir -p docs/roadmaps

# Get current date for filename
DATE=$(date +%Y-%m)
ROADMAP_FILE="docs/roadmaps/${TIMEFRAME}-${DATE}.md"

# Check if we have ideas in GitHub issues
IDEA_COUNT=$(gh issue list --label idea --state open --json number | jq '. | length')

if [ "$IDEA_COUNT" -eq 0 ]; then
    echo "⚠️  No open ideas found in GitHub issues."
    echo "💡 Try running: ./scripts/capture.sh \"[your idea]\" first"
    exit 1
fi

echo "📊 Found $IDEA_COUNT open ideas to analyze..."

# Create roadmap template
cat > "$ROADMAP_FILE" << 'EOF'
# ${TIMEFRAME^} Roadmap - $(date +"%B %Y")

## Overview
Strategic planning session for ${TIMEFRAME} execution priorities.

## Ideas Analysis

### Available Ideas (from GitHub Issues)
EOF

# Update template variables
sed -i '' "s/\${TIMEFRAME^}/${TIMEFRAME^}/g" "$ROADMAP_FILE"
sed -i '' "s/\$(date +\"%B %Y\")/$(date +"%B %Y")/g" "$ROADMAP_FILE"

# Fetch and categorize ideas
echo "" >> "$ROADMAP_FILE"
echo "#### BI/Analytics Ideas" >> "$ROADMAP_FILE"
gh issue list --label idea --label bi-analytics --state open --json number,title,url --jq '.[] | "- [#\(.number)](\(.url)): \(.title)"' >> "$ROADMAP_FILE" || echo "_None_" >> "$ROADMAP_FILE"

echo "" >> "$ROADMAP_FILE"
echo "#### Data Engineering Ideas" >> "$ROADMAP_FILE"
gh issue list --label idea --label data-engineering --state open --json number,title,url --jq '.[] | "- [#\(.number)](\(.url)): \(.title)"' >> "$ROADMAP_FILE" || echo "_None_" >> "$ROADMAP_FILE"

echo "" >> "$ROADMAP_FILE"
echo "#### Analytics Engineering Ideas" >> "$ROADMAP_FILE"
gh issue list --label idea --label analytics-engineering --state open --json number,title,url --jq '.[] | "- [#\(.number)](\(.url)): \(.title)"' >> "$ROADMAP_FILE" || echo "_None_" >> "$ROADMAP_FILE"

echo "" >> "$ROADMAP_FILE"
echo "#### Architecture Ideas" >> "$ROADMAP_FILE"
gh issue list --label idea --label architecture --state open --json number,title,url --jq '.[] | "- [#\(.number)](\(.url)): \(.title)"' >> "$ROADMAP_FILE" || echo "_None_" >> "$ROADMAP_FILE"

echo "" >> "$ROADMAP_FILE"
echo "#### UI Development Ideas" >> "$ROADMAP_FILE"
gh issue list --label idea --label ui-development --state open --json number,title,url --jq '.[] | "- [#\(.number)](\(.url)): \(.title)"' >> "$ROADMAP_FILE" || echo "_None_" >> "$ROADMAP_FILE"

echo "" >> "$ROADMAP_FILE"
echo "#### General Ideas" >> "$ROADMAP_FILE"
gh issue list --label idea --label general --state open --json number,title,url --jq '.[] | "- [#\(.number)](\(.url)): \(.title)"' >> "$ROADMAP_FILE" || echo "_None_" >> "$ROADMAP_FILE"

# Add prioritization framework
cat >> "$ROADMAP_FILE" << EOF

## Prioritization Framework

### Impact vs Effort Analysis
Use this matrix to evaluate each idea:

| Issue # | Title | Impact (1-5) | Effort (1-5) | Priority Score | Notes |
|---------|-------|--------------|--------------|----------------|-------|
| #[number] | [title] | [rating] | [rating] | [calculated] | [reasoning] |

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
- [ ] #[issue-number] - [brief description]

### Future Considerations
Ideas for next planning cycle:
- [ ] #[issue-number] - [brief description]

## Notes
- Planning date: $(date)
- Review date: [set future review date]
- Stakeholders: [list key stakeholders]

## Quick Actions

### View All Ideas
\`\`\`bash
gh issue list --label idea --state open
\`\`\`

### Build Top Priority
\`\`\`bash
./scripts/build.sh <issue-number>
\`\`\`
EOF

echo "✅ Roadmap created: $ROADMAP_FILE"
echo ""
echo "📋 Next steps:"
echo "   1. Review and fill in the prioritization matrix"
echo "   2. Identify top 2-3 ideas for execution"
echo "   3. Build highest priority: ./scripts/build.sh <issue-number>"
echo ""
echo "💡 Tip: Open the roadmap file to complete the prioritization analysis"
echo "🔗 View all ideas: gh issue list --label idea --state open"
