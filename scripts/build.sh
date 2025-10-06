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

# Worktree Integration (if configured)
USING_WORKTREE=false
WORKTREE_DIR=""

if [ -f ".claude/config/worktree.conf" ]; then
    source ".claude/config/worktree.conf"
    if [ "$WORKTREE_ENABLED" = "true" ] && [ -n "$WORKTREE_BASE_PATH" ]; then
        echo ""
        echo "🌿 Worktree integration enabled"

        # Create worktree for this project
        WORKTREE_DIR="$WORKTREE_BASE_PATH/$PROJECT_NAME"

        if [ -d "$WORKTREE_DIR" ]; then
            echo "⚠️  Worktree already exists: $WORKTREE_DIR"
            echo "Using existing worktree..."
            USING_WORKTREE=true
        else
            echo "Creating worktree: $WORKTREE_DIR"
            git worktree add "$WORKTREE_DIR" "$PROJECT_NAME" 2>&1

            if [ $? -eq 0 ]; then
                USING_WORKTREE=true
                echo "✅ Worktree created successfully"

                # Create VS Code workspace file
                cat > "$WORKTREE_DIR/$PROJECT_NAME.code-workspace" << WORKSPACE_EOF
{
  "folders": [
    {
      "name": "🔧 $PROJECT_NAME",
      "path": "."
    }
  ],
  "settings": {
    "git.detectWorktrees": true,
    "files.autoSave": "onFocusChange",
    "files.autoSaveDelay": 1000,
    "files.watcherExclude": {
      "**/.git/objects/**": true,
      "**/.git/subtree-cache/**": true,
      "**/.git/worktrees/**": false,
      "**/node_modules/**": true,
      "**/.venv/**": true
    },
    "terminal.integrated.cwd": "\${workspaceFolder}"
  },
  "extensions": {
    "recommendations": [
      "GitWorktrees.git-worktrees",
      "eamodio.gitlens",
      "mhutchie.git-graph"
    ]
  }
}
WORKSPACE_EOF
                echo "✅ VS Code workspace file created"
            else
                echo "⚠️  Failed to create worktree, continuing with standard workflow"
                USING_WORKTREE=false
            fi
        fi
    fi
fi

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

# Optional VS Code launch for worktree
if [ "$USING_WORKTREE" = true ]; then
    if command -v code &> /dev/null; then
        echo ""
        echo "🚀 VS Code Integration:"
        echo "   📁 Workspace: $WORKTREE_DIR/$PROJECT_NAME.code-workspace"
        echo ""
        read -p "Launch VS Code for this project? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            code "$WORKTREE_DIR/$PROJECT_NAME.code-workspace"
            echo "✅ VS Code launched!"
        fi
    fi
fi

echo ""
echo "✅ Project successfully created from issue #$ISSUE_NUMBER!"

if [ "$USING_WORKTREE" = true ]; then
    echo "📁 Project location (worktree): $WORKTREE_DIR/projects/active/$PROJECT_NAME/"
    echo "🌿 Worktree: $WORKTREE_DIR"
    echo "🎯 Branch: $PROJECT_NAME (isolated in worktree)"
else
    echo "📁 Project location: $PROJECT_DIR/"
    echo "🎯 Branch: $PROJECT_NAME (standard workflow)"
fi

echo "🔗 Linked to: https://github.com/graniterock/da-agent-hub/issues/$ISSUE_NUMBER"
echo ""
echo "🎯 Next steps:"

if [ "$USING_WORKTREE" = true ]; then
    echo "   1. Open VS Code workspace: $WORKTREE_DIR/$PROJECT_NAME.code-workspace"
    echo "   2. Review project spec: projects/active/$PROJECT_NAME/spec.md"
    echo "   3. Begin development work in isolated environment"
    echo "   4. Update issue #$ISSUE_NUMBER with progress comments"
    echo "   5. When complete: ./scripts/finish.sh $PROJECT_NAME"
else
    echo "   1. Review project spec: $PROJECT_DIR/spec.md"
    echo "   2. Begin development work"
    echo "   3. Update issue #$ISSUE_NUMBER with progress comments"
    echo "   4. When complete: ./scripts/finish.sh $PROJECT_NAME"
fi
