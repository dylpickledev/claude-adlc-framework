#!/bin/bash

# build.sh - Execute ideas as full projects from GitHub Issues
# Usage: ./scripts/build.sh <issue-number>
# Creates project structure from GitHub issue and links them together

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure we're in the repo root
cd "$REPO_ROOT"

# Input validation
if [ $# -eq 0 ]; then
    echo "Usage: ./scripts/build.sh <issue-number>"
    echo ""
    echo "Available ideas (open GitHub issues with 'idea' label):"
    echo ""
    gh issue list --label idea --state open --json number,title | jq -r '.[] | "  #\(.number): \(.title)"'
    echo ""
    echo "Example: ./scripts/build.sh 85"
    exit 1
fi

ISSUE_NUMBER="$1"

# Validate issue number is numeric
if ! [[ "$ISSUE_NUMBER" =~ ^[0-9]+$ ]]; then
    echo "❌ Error: Issue number must be numeric"
    echo "Usage: ./scripts/build.sh <issue-number>"
    exit 1
fi

echo "🔧 Building project from GitHub issue #$ISSUE_NUMBER"

# Fetch issue details
ISSUE_JSON=$(gh issue view "$ISSUE_NUMBER" --json number,title,body,labels)

if [ $? -ne 0 ]; then
    echo "❌ Error: Could not find issue #$ISSUE_NUMBER"
    exit 1
fi

ISSUE_TITLE=$(echo "$ISSUE_JSON" | jq -r '.title')
ISSUE_BODY=$(echo "$ISSUE_JSON" | jq -r '.body')
HAS_IDEA_LABEL=$(echo "$ISSUE_JSON" | jq -r '.labels[] | select(.name == "idea") | .name' | head -1)

if [ "$HAS_IDEA_LABEL" != "idea" ]; then
    echo "⚠️  Warning: Issue #$ISSUE_NUMBER doesn't have 'idea' label"
    echo "Proceeding anyway..."
fi

echo "📋 Issue: $ISSUE_TITLE"

# Create project name from issue title
PROJECT_NAME="feature-$(echo "$ISSUE_TITLE" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '-' | sed 's/-$//' | cut -c1-50)"

echo "🏗️  Creating project structure: $PROJECT_NAME"

# Create project using work-init.sh if available
if [ -f "$SCRIPT_DIR/work-init.sh" ]; then
    bash "$SCRIPT_DIR/work-init.sh" "feature" "$ISSUE_TITLE"
    PROJECT_DIR="projects/active/$PROJECT_NAME"
else
    echo "Warning: work-init.sh not found, creating basic structure"
    PROJECT_DIR="projects/active/$PROJECT_NAME"
    mkdir -p "$PROJECT_DIR/tasks"

    # Create basic project files
    cat > "$PROJECT_DIR/README.md" << EOF
# $ISSUE_TITLE

**Source**: GitHub Issue #$ISSUE_NUMBER

## Quick Links
- [GitHub Issue #$ISSUE_NUMBER](https://github.com/graniterock/da-agent-hub/issues/$ISSUE_NUMBER)
- [spec.md](./spec.md) - Project specification
- [context.md](./context.md) - Current context and state

## Status
🏗️ In Development
EOF

    cat > "$PROJECT_DIR/spec.md" << EOF
# $ISSUE_TITLE

**Source**: GitHub Issue [#$ISSUE_NUMBER](https://github.com/graniterock/da-agent-hub/issues/$ISSUE_NUMBER)

## Original Idea
$ISSUE_BODY

## Implementation Plan
[To be filled in with technical details]

## Success Criteria
[To be defined based on requirements]

## Related Issues
- Source: #$ISSUE_NUMBER
EOF

    cat > "$PROJECT_DIR/context.md" << EOF
# Project Context: $ISSUE_TITLE

**Current Branch**: \$(git branch --show-current)
**Source Issue**: #$ISSUE_NUMBER
**Created**: $(date)

## Current Focus
[What you're working on right now]

## Blockers
[Any issues preventing progress]

## Next Steps
1. Review spec.md and refine requirements
2. Begin implementation
3. Update issue #$ISSUE_NUMBER with progress
EOF
fi

echo "✅ Project structure created"

# Add comment to GitHub issue linking to project
echo "🔗 Linking project to GitHub issue..."
gh issue comment "$ISSUE_NUMBER" --body "🏗️ **Project Created**

This idea has been promoted to an active project:
- **Project**: \`$PROJECT_NAME\`
- **Location**: \`projects/active/$PROJECT_NAME/\`
- **Status**: In Development

The project will remain linked to this issue. This issue will be closed when the project is completed via \`./scripts/finish.sh\`"

# Add 'in-progress' label to issue
gh issue edit "$ISSUE_NUMBER" --add-label "in-progress"

echo ""
echo "✅ Project successfully created from issue #$ISSUE_NUMBER!"
echo "📁 Project location: $PROJECT_DIR/"
echo "🔗 Linked to: https://github.com/graniterock/da-agent-hub/issues/$ISSUE_NUMBER"
echo ""
echo "🎯 Next steps:"
echo "   1. Review project spec: $PROJECT_DIR/spec.md"
echo "   2. Begin development work"
echo "   3. Update issue #$ISSUE_NUMBER with progress comments"
echo "   4. When complete: ./scripts/finish.sh $PROJECT_NAME"
