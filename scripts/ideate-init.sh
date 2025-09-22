#!/bin/bash

# ideate-init.sh - Rapid idea capture script
# Usage: ./scripts/ideate-init.sh "concept description"

set -e

# Configuration
IDEAS_DIR="ideas"
INBOX_DIR="$IDEAS_DIR/inbox"
TIMESTAMP=$(date +"%Y-%m-%d-%H%M")

# Ensure directories exist
mkdir -p "$INBOX_DIR"

# Check if concept provided
if [ $# -eq 0 ]; then
    echo "❌ Error: Please provide an idea concept"
    echo "Usage: $0 \"your idea description\""
    exit 1
fi

CONCEPT="$1"

# Generate filename from concept
# Remove special characters, convert to lowercase, limit length
KEYWORD_SUMMARY=$(echo "$CONCEPT" | \
    sed 's/[^a-zA-Z0-9 ]//g' | \
    tr '[:upper:]' '[:lower:]' | \
    tr ' ' '-' | \
    cut -c1-50 | \
    sed 's/-$//')

FILENAME="$TIMESTAMP-$KEYWORD_SUMMARY.md"
FILEPATH="$INBOX_DIR/$FILENAME"

# Extract basic info from concept
CORE_CONCEPT=$(echo "$CONCEPT" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

# Determine rough type based on keywords
TYPE="Mixed"
if echo "$CONCEPT" | grep -qi -E "(dashboard|tableau|report|visualization|chart)"; then
    TYPE="Visualization"
elif echo "$CONCEPT" | grep -qi -E "(model|dbt|sql|transformation|schema)"; then
    TYPE="Data Modeling"
elif echo "$CONCEPT" | grep -qi -E "(pipeline|orchestration|airflow|prefect|schedule)"; then
    TYPE="Pipeline/Orchestration"
elif echo "$CONCEPT" | grep -qi -E "(quality|testing|validation|monitoring)"; then
    TYPE="Data Quality"
elif echo "$CONCEPT" | grep -qi -E "(performance|optimization|cost|efficiency)"; then
    TYPE="Performance"
elif echo "$CONCEPT" | grep -qi -E "(analytics|analysis|insight|metric)"; then
    TYPE="Analytics"
elif echo "$CONCEPT" | grep -qi -E "(customer|user|behavior|segment)"; then
    TYPE="Customer Analytics"
elif echo "$CONCEPT" | grep -qi -E "(platform|architecture|system|infrastructure)"; then
    TYPE="Strategic/Platform"
fi

# Create idea file
cat > "$FILEPATH" << EOF
# $CORE_CONCEPT

**Captured**: $TIMESTAMP
**Type**: $TYPE
**Status**: inbox

## Raw Idea
$CONCEPT

## Initial Analysis
**Problem Context**: [To be analyzed during organization]
**Potential Scope**: [To be assessed by AI]
**Related Areas**: [To be determined by clustering]

## Next Steps
- [ ] Include in next /organize session
- [ ] Technical analysis needed from: [relevant agents if obvious]
- [ ] Stakeholder input needed from: [if cross-departmental]

---
*Captured via ideate-init.sh script*
EOF

# Output success message
echo "💡 Idea captured: $CORE_CONCEPT"
echo "📁 Saved to: $FILEPATH"
echo "🔄 Run 'claude /organize' to cluster with related ideas"

# Optional: Add to git if in a git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    git add "$FILEPATH"
    echo "📝 Added to git staging area"
fi