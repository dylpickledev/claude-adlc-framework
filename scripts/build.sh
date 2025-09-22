#!/bin/bash

# build.sh - Execute ideas as full projects
# Usage: ./scripts/build.sh [idea-name]
# Replaces: /promote, /start_project, /specify, /plan, /tasks commands

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure we're in the repo root
cd "$REPO_ROOT"

# Input validation
if [ $# -eq 0 ]; then
    echo "Usage: ./scripts/build.sh [idea-name]"
    echo ""
    echo "Available ideas:"

    # Show organized ideas
    if [ -d "ideas/organized" ]; then
        for category_dir in ideas/organized/*/; do
            if [ -d "$category_dir" ]; then
                category=$(basename "$category_dir")
                echo "  📁 $category:"
                for idea_file in "$category_dir"*.md; do
                    if [ -f "$idea_file" ]; then
                        idea_name=$(basename "$idea_file" .md)
                        echo "    - $idea_name"
                    fi
                done
            fi
        done
    fi

    # Show pipeline ideas
    if [ -d "ideas/pipeline" ] && [ -n "$(find ideas/pipeline -name "*.md" 2>/dev/null)" ]; then
        echo "  🚀 Pipeline (ready to build):"
        for idea_file in ideas/pipeline/*.md; do
            if [ -f "$idea_file" ]; then
                idea_name=$(basename "$idea_file" .md)
                echo "    - $idea_name"
            fi
        done
    fi

    exit 1
fi

IDEA_NAME="$1"

echo "🔧 Building project for idea: $IDEA_NAME"

# Find the idea file in organized or pipeline directories
IDEA_FILE=""
if [ -f "ideas/pipeline/${IDEA_NAME}.md" ]; then
    IDEA_FILE="ideas/pipeline/${IDEA_NAME}.md"
    echo "📋 Found idea in pipeline: $IDEA_FILE"
elif [ -d "ideas/organized" ]; then
    # Search in organized categories
    for category_dir in ideas/organized/*/; do
        if [ -f "${category_dir}${IDEA_NAME}.md" ]; then
            IDEA_FILE="${category_dir}${IDEA_NAME}.md"
            echo "📋 Found idea in organized: $IDEA_FILE"
            break
        fi
    done
fi

if [ -z "$IDEA_FILE" ]; then
    echo "❌ Idea '$IDEA_NAME' not found."
    echo "💡 Available ideas are listed above. Make sure to use exact name."
    exit 1
fi

# First, promote the idea to pipeline if it's not already there
if [[ "$IDEA_FILE" != *"pipeline"* ]]; then
    echo "📦 Promoting idea to pipeline..."
    if [ -f "$SCRIPT_DIR/ideate-promote.sh" ]; then
        bash "$SCRIPT_DIR/ideate-promote.sh" "$IDEA_NAME" "project"
        IDEA_FILE="ideas/pipeline/${IDEA_NAME}.md"
    else
        echo "Warning: ideate-promote.sh not found, using idea file directly"
    fi
fi

# Create project using existing work-init.sh
echo "🏗️  Creating project structure..."

# Use the idea name as project description for work-init.sh
PROJECT_NAME="feature-$(echo "$IDEA_NAME" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"

if [ -f "$SCRIPT_DIR/work-init.sh" ]; then
    bash "$SCRIPT_DIR/work-init.sh" "feature" "$IDEA_NAME"
    echo "✅ Project structure created"
else
    echo "Warning: work-init.sh not found, creating basic structure"

    # Create basic project structure
    mkdir -p "projects/active/$PROJECT_NAME"

    # Copy idea content to project spec
    cat > "projects/active/$PROJECT_NAME/spec.md" << EOF
# $IDEA_NAME

## Original Idea
$(cat "$IDEA_FILE")

## Implementation Plan
[To be filled in with technical details]

## Success Criteria
[To be defined]
EOF

    echo "✅ Basic project structure created"
fi

# Move idea to archive with project link
echo "📚 Archiving idea with project reference..."
mkdir -p ideas/archive

# Create archived idea with project reference
cat > "ideas/archive/${IDEA_NAME}.md" << EOF
# $IDEA_NAME (BUILT)

## Status
✅ **BUILT** - Promoted to project: $PROJECT_NAME

## Original Idea
$(cat "$IDEA_FILE")

## Project Details
- **Project Directory**: projects/active/$PROJECT_NAME/
- **Build Date**: $(date)
- **Status**: In Development

## Links
- [Project Files](../projects/active/$PROJECT_NAME/)
- [Project Spec](../projects/active/$PROJECT_NAME/spec.md)
EOF

# Remove from pipeline/organized
rm -f "$IDEA_FILE"

echo ""
echo "✅ Idea successfully built into project!"
echo "📁 Project location: projects/active/$PROJECT_NAME/"
echo ""
echo "🎯 Next steps:"
echo "   1. Review project spec: projects/active/$PROJECT_NAME/spec.md"
echo "   2. Begin development work"
echo "   3. When complete: ./scripts/finish.sh $PROJECT_NAME"