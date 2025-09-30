#!/bin/bash

# finish.sh - Complete and archive projects
# Usage: ./scripts/finish.sh [project-name]
# Replaces: ./scripts/work-complete.sh and manual cleanup workflows

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure we're in the repo root
cd "$REPO_ROOT"

# Input validation
if [ $# -eq 0 ]; then
    echo "Usage: ./scripts/finish.sh [project-name]"
    echo ""
    echo "Active projects:"

    if [ -d "projects/active" ]; then
        for project_dir in projects/active/*/; do
            if [ -d "$project_dir" ]; then
                project_name=$(basename "$project_dir")
                echo "  - $project_name"
            fi
        done
    else
        echo "  No active projects found"
    fi

    exit 1
fi

PROJECT_NAME="$1"
PROJECT_DIR="projects/active/$PROJECT_NAME"

# Validate project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project '$PROJECT_NAME' not found in projects/active/"
    echo "💡 Available projects are listed above"
    exit 1
fi

echo "🎯 Finishing project: $PROJECT_NAME"

# Use existing work-complete.sh if available
if [ -f "$SCRIPT_DIR/work-complete.sh" ]; then
    echo "📦 Using work-complete.sh for comprehensive cleanup..."
    bash "$SCRIPT_DIR/work-complete.sh" "$PROJECT_NAME"
else
    echo "📦 Performing basic project completion..."

    # Basic completion workflow
    mkdir -p projects/completed

    # Move project to completed
    mv "$PROJECT_DIR" "projects/completed/"

    # Update project status
    if [ -f "projects/completed/$PROJECT_NAME/context.md" ]; then
        echo "" >> "projects/completed/$PROJECT_NAME/context.md"
        echo "## Completion" >> "projects/completed/$PROJECT_NAME/context.md"
        echo "- **Completed**: $(date)" >> "projects/completed/$PROJECT_NAME/context.md"
        echo "- **Status**: ✅ Finished" >> "projects/completed/$PROJECT_NAME/context.md"
    fi

    echo "✅ Project moved to projects/completed/"
fi

# Check if we're on a feature branch for this project
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" == *"$PROJECT_NAME"* ]] || [[ "$CURRENT_BRANCH" == "feature-"* ]]; then
    echo ""
    echo "🔀 Git workflow options:"
    echo "   1. Create PR: gh pr create --title \"Complete $PROJECT_NAME\" --body \"Project completion\""
    echo "   2. Merge to main: git checkout main && git merge $CURRENT_BRANCH"
    echo "   3. Stay on branch: Continue working"
    echo ""
    echo "💡 Recommended: Create PR for review before merging"
fi

# Extract patterns and learnings to memory system
echo "📚 Extracting reusable patterns to memory..."
MEMORY_DIR="$REPO_ROOT/.claude/memory"
MONTH_FILE="$MEMORY_DIR/recent/$(date +%Y-%m).md"

# Ensure memory directories exist
mkdir -p "$MEMORY_DIR/patterns" "$MEMORY_DIR/recent" "$MEMORY_DIR/templates"

# Extract patterns from task findings
if [ -d "$REPO_ROOT/.claude/tasks" ]; then
    PATTERN_COUNT=0

    # Create or append to monthly file
    if [ ! -f "$MONTH_FILE" ]; then
        echo "# Patterns and Learnings - $(date +%B %Y)" > "$MONTH_FILE"
        echo "" >> "$MONTH_FILE"
    fi

    echo "" >> "$MONTH_FILE"
    echo "## From Project: $PROJECT_NAME ($(date +%Y-%m-%d))" >> "$MONTH_FILE"
    echo "" >> "$MONTH_FILE"

    # Search for pattern markers in all task findings
    for findings_file in $(find "$REPO_ROOT/.claude/tasks" -name "*.md" -type f 2>/dev/null); do
        if grep -q "PATTERN:\|SOLUTION:\|ERROR-FIX:\|ARCHITECTURE:\|INTEGRATION:" "$findings_file" 2>/dev/null; then
            echo "### $(basename $(dirname "$findings_file"))/$(basename "$findings_file")" >> "$MONTH_FILE"
            echo "" >> "$MONTH_FILE"
            grep "PATTERN:\|SOLUTION:\|ERROR-FIX:\|ARCHITECTURE:\|INTEGRATION:" "$findings_file" >> "$MONTH_FILE" 2>/dev/null
            echo "" >> "$MONTH_FILE"
            PATTERN_COUNT=$((PATTERN_COUNT + 1))
        fi
    done

    if [ $PATTERN_COUNT -gt 0 ]; then
        echo "   ✅ Extracted patterns from $PATTERN_COUNT files"
        echo "   📁 Saved to: memory/recent/$(date +%Y-%m).md"

        # Clean up task findings after extraction
        echo "   🧹 Cleaning up extracted task findings..."
        find "$REPO_ROOT/.claude/tasks" -name "*.md" -type f -delete 2>/dev/null
    else
        echo "   ℹ️  No patterns found to extract"
    fi
else
    echo "   ℹ️  No task findings directory found"
fi

# Update any related archived ideas
echo "🔗 Updating related archived ideas..."
if [ -d "ideas/archive" ]; then
    for archived_idea in ideas/archive/*.md; do
        if [ -f "$archived_idea" ] && grep -q "$PROJECT_NAME" "$archived_idea"; then
            # Update status in archived idea
            sed -i.bak "s/Status**: In Development/Status**: ✅ Completed $(date)/" "$archived_idea"
            rm -f "${archived_idea}.bak"
            echo "   Updated: $(basename "$archived_idea")"
        fi
    done
fi

echo ""
echo "✅ Project '$PROJECT_NAME' completed successfully!"
echo "📁 Location: projects/completed/$PROJECT_NAME/"
echo ""
echo "🎉 Next steps:"
echo "   - Review completed work"
echo "   - Document lessons learned"
echo "   - Plan next project: ./scripts/build.sh [idea-name]"