#!/bin/bash

# work-init.sh - Initialize a new work project
# Usage: ./scripts/work-init.sh <type> "<description>"
# Example: ./scripts/work-init.sh feature "snowflake optimization"

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validate arguments
if [ $# -ne 2 ]; then
    echo -e "${RED}Error: Invalid arguments${NC}"
    echo "Usage: $0 <type> \"<description>\""
    echo "Types: feature, fix, research, refactor, docs"
    echo "Example: $0 feature \"snowflake optimization\""
    exit 1
fi

PROJECT_TYPE="$1"
DESCRIPTION="$2"

# Validate project type
case "$PROJECT_TYPE" in
    feature|fix|research|refactor|docs)
        ;;
    *)
        echo -e "${RED}Error: Invalid project type '$PROJECT_TYPE'${NC}"
        echo "Valid types: feature, fix, research, refactor, docs"
        exit 1
        ;;
esac

# Generate project folder name
CLEAN_DESC=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g' | tr ' ' '-' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
PROJECT_NAME="${PROJECT_TYPE}-${CLEAN_DESC}"
PROJECT_DIR="projects/active/$PROJECT_NAME"

# Check if project already exists
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${RED}Error: Project '$PROJECT_NAME' already exists${NC}"
    exit 1
fi

# Get current branch and ensure we're on main
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${YELLOW}Warning: Not on main branch (currently on: $CURRENT_BRANCH)${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Create project directory
mkdir -p "$PROJECT_DIR"

# Generate README.md
cat > "$PROJECT_DIR/README.md" << EOF
# $PROJECT_TYPE: $DESCRIPTION

**Created:** $(date '+%Y-%m-%d %H:%M:%S')  
**Type:** $PROJECT_TYPE  
**Base Branch:** $CURRENT_BRANCH  
**Work Branch:** $PROJECT_NAME

## Objective

$DESCRIPTION

## Tasks

- [ ] Initial analysis
- [ ] Implementation plan
- [ ] Testing strategy
- [ ] Documentation updates

## Research Notes

<!-- Use this section for research findings, links, and context -->

## Related PRs & Issues

<!-- Link to related work across repositories -->
- da-agent-hub: 
- dbt_cloud: 
- other repos: 

## Files Changed

<!-- Track important file changes during development -->

## Testing

<!-- Document testing approach and results -->

## Completion Checklist

- [ ] All code changes implemented
- [ ] Tests passing
- [ ] Documentation updated
- [ ] PRs created in target repositories
- [ ] Knowledge extracted to permanent storage

---

*Use \`./scripts/work-complete.sh $PROJECT_NAME\` when ready to complete this work.*
EOF

# Create work branch
echo -e "${GREEN}Creating work branch: $PROJECT_NAME${NC}"
git checkout -b "$PROJECT_NAME"

# Stage the README
git add "$PROJECT_DIR/README.md"

echo
echo -e "${GREEN}✅ Work project initialized successfully!${NC}"
echo "Project: $PROJECT_NAME"
echo "Directory: $PROJECT_DIR"
echo "Branch: $PROJECT_NAME"
echo
echo "Next steps:"
echo "1. Edit $PROJECT_DIR/README.md to refine your objectives"
echo "2. Start working on your tasks"
echo "3. Use the project folder to organize related files"
echo "4. Run './scripts/work-complete.sh $PROJECT_NAME' when finished"