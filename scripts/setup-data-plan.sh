#!/usr/bin/env bash
# Setup data analytics implementation plan structure for current branch
# Returns paths needed for implementation plan generation
# Usage: ./setup-data-plan.sh [--json]

set -e

JSON_MODE=false
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json]"; exit 0 ;;
    esac
done

# Source common functions if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/common.sh" ]; then
    source "$SCRIPT_DIR/common.sh"
fi

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_BRANCH=$(git branch --show-current)

# Check if on data project branch
if [[ ! "$CURRENT_BRANCH" =~ ^(data|dashboard|pipeline|model)/ ]]; then
    echo "Error: Not on a data project branch. Use create-new-project.sh first." >&2
    exit 1
fi

# Extract project info from branch name
BRANCH_SUFFIX=${CURRENT_BRANCH#*/}  # Remove prefix (data/, dashboard/, etc.)
PROJECT_NUM=${BRANCH_SUFFIX%%-*}   # Extract number (001, 002, etc.)

# Find project directory
PROJECTS_DIR="$REPO_ROOT/projects"
PROJECT_DIR="$PROJECTS_DIR/$PROJECT_NUM"-*

# Use glob to find the actual directory name
PROJECT_DIR=$(ls -d $PROJECT_DIR 2>/dev/null | head -1)

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory not found for branch $CURRENT_BRANCH" >&2
    exit 1
fi

# Define paths
FEATURE_SPEC="$PROJECT_DIR/spec.md"
IMPL_PLAN="$PROJECT_DIR/plan.md"

# Check if spec exists
if [ ! -f "$FEATURE_SPEC" ]; then
    echo "Error: Specification not found at $FEATURE_SPEC" >&2
    exit 1
fi

# Create additional directories for data projects
mkdir -p "$PROJECT_DIR/contracts"
mkdir -p "$PROJECT_DIR/findings"
mkdir -p "$PROJECT_DIR/tasks"

# Copy data plan template if it exists
TEMPLATE="$REPO_ROOT/templates/data-plan-template.md"
if [ -f "$TEMPLATE" ]; then
    cp "$TEMPLATE" "$IMPL_PLAN"
    # Update placeholders in the copied file - escape forward slashes
    FEATURE_NAME=$(grep "^# Data Analytics Feature Specification:" "$FEATURE_SPEC" | sed 's/^# Data Analytics Feature Specification: //' || echo "Data Project")
    ESCAPED_BRANCH=$(echo "$CURRENT_BRANCH" | sed 's/\//\\\//g')
    ESCAPED_FEATURE=$(echo "$FEATURE_NAME" | sed 's/\//\\\//g')
    sed -i.bak "s/\[FEATURE\]/$ESCAPED_FEATURE/g" "$IMPL_PLAN"
    sed -i.bak "s/\[###-feature-name\]/$ESCAPED_BRANCH/g" "$IMPL_PLAN"
    sed -i.bak "s/\[DATE\]/$(date '+%Y-%m-%d')/g" "$IMPL_PLAN"
    sed -i.bak "s|\[link\]|spec.md|g" "$IMPL_PLAN"
    rm "$IMPL_PLAN.bak" 2>/dev/null || true
fi

# Update task coordination file
cat > "$PROJECT_DIR/tasks/current-task.md" << EOF
# Current Task Context

**Project**: $(basename "$PROJECT_DIR")  
**Branch**: $CURRENT_BRANCH  
**Status**: Planning Phase  
**Next Step**: Complete /plan command

## Task Assignment

**Current Owner**: Parent Agent  
**Phase**: Implementation Planning  

## Available Documents

- **Specification**: \`$FEATURE_SPEC\`
- **Implementation Plan**: \`$IMPL_PLAN\` (in progress)

## Context for Sub-Agents

When assigned to this project, sub-agents should:
1. Read the project spec and plan
2. Create detailed findings in: \`$PROJECT_DIR/findings/[tool]-findings.md\`
3. Update task status in this file

## Cross-Tool Integration Points

- **dbt → Snowflake**: Schema and model coordination
- **Snowflake → Tableau**: Data source optimization  
- **Orchestra → All**: Pipeline scheduling and monitoring
- **Business Context → All**: Stakeholder requirements and validation

---
*Updated: $(date '+%Y-%m-%d %H:%M:%S')*
EOF

if $JSON_MODE; then
    printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","PROJECTS_DIR":"%s","BRANCH":"%s","PROJECT_DIR":"%s"}\n' \
        "$FEATURE_SPEC" "$IMPL_PLAN" "$PROJECT_DIR" "$CURRENT_BRANCH" "$PROJECT_DIR"
else
    # Output all paths for LLM use
    echo "FEATURE_SPEC: $FEATURE_SPEC"
    echo "IMPL_PLAN: $IMPL_PLAN"
    echo "PROJECTS_DIR: $PROJECT_DIR"
    echo "BRANCH: $CURRENT_BRANCH"
    echo "PROJECT_DIR: $PROJECT_DIR"
fi