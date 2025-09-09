#!/usr/bin/env bash
# Create a new data analytics project with branch, directory structure, and templates
# Usage: ./create-new-project.sh "feature description"
#        ./create-new-project.sh --json "feature description"

set -e

JSON_MODE=false

# Collect non-flag args
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --help|-h)
            echo "Usage: $0 [--json] <project_description>"; exit 0 ;;
        *)
            ARGS+=("$arg") ;;
    esac
done

PROJECT_DESCRIPTION="${ARGS[*]}"
if [ -z "$PROJECT_DESCRIPTION" ]; then
        echo "Usage: $0 [--json] <project_description>" >&2
        exit 1
fi

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
PROJECTS_DIR="$REPO_ROOT/projects"

# Create projects directory if it doesn't exist
mkdir -p "$PROJECTS_DIR"

# Find the highest numbered project directory
HIGHEST=0
if [ -d "$PROJECTS_DIR" ]; then
    for dir in "$PROJECTS_DIR"/*; do
        if [ -d "$dir" ]; then
            dirname=$(basename "$dir")
            number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
            number=$((10#$number))
            if [ "$number" -gt "$HIGHEST" ]; then
                HIGHEST=$number
            fi
        fi
    done
fi

# Generate next project number with zero padding
NEXT=$((HIGHEST + 1))
PROJECT_NUM=$(printf "%03d" "$NEXT")

# Create branch name from description
BRANCH_NAME=$(echo "$PROJECT_DESCRIPTION" | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/[^a-z0-9]/-/g' | \
    sed 's/-\+/-/g' | \
    sed 's/^-//' | \
    sed 's/-$//')

# Extract 2-3 meaningful words for data projects
WORDS=$(echo "$BRANCH_NAME" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')

# Add data project prefix
if [[ "$BRANCH_NAME" == *"dashboard"* || "$BRANCH_NAME" == *"report"* || "$BRANCH_NAME" == *"tableau"* ]]; then
    PREFIX="dashboard"
elif [[ "$BRANCH_NAME" == *"pipeline"* || "$BRANCH_NAME" == *"etl"* || "$BRANCH_NAME" == *"orchestra"* ]]; then
    PREFIX="pipeline"
elif [[ "$BRANCH_NAME" == *"model"* || "$BRANCH_NAME" == *"dbt"* || "$BRANCH_NAME" == *"transform"* ]]; then
    PREFIX="model"
else
    PREFIX="data"
fi

# Final branch name
BRANCH_NAME="${PREFIX}/${PROJECT_NUM}-${WORDS}"

# Create and switch to new branch
git checkout -b "$BRANCH_NAME"

# Create project directory structure
PROJECT_DIR="$PROJECTS_DIR/$PROJECT_NUM-${WORDS}"
mkdir -p "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/tasks"
mkdir -p "$PROJECT_DIR/contracts"
mkdir -p "$PROJECT_DIR/findings"

# Copy data-specific template if it exists
TEMPLATE="$REPO_ROOT/templates/data-spec-template.md"
SPEC_FILE="$PROJECT_DIR/spec.md"

if [ -f "$TEMPLATE" ]; then
    cp "$TEMPLATE" "$SPEC_FILE"
    # Update placeholders in the copied file - escape forward slashes
    ESCAPED_BRANCH=$(echo "$BRANCH_NAME" | sed 's/\//\\\//g')
    ESCAPED_DESCRIPTION=$(echo "$PROJECT_DESCRIPTION" | sed 's/\//\\\//g')
    sed -i.bak "s/\[FEATURE NAME\]/$ESCAPED_DESCRIPTION/g" "$SPEC_FILE"
    sed -i.bak "s/\[###-feature-name\]/$ESCAPED_BRANCH/g" "$SPEC_FILE"
    sed -i.bak "s/\[DATE\]/$(date '+%Y-%m-%d')/g" "$SPEC_FILE"
    sed -i.bak "s/\$ARGUMENTS/$ESCAPED_DESCRIPTION/g" "$SPEC_FILE"
    rm "$SPEC_FILE.bak"
else
    echo "Warning: Template not found at $TEMPLATE" >&2
    touch "$SPEC_FILE"
fi

# Create initial task coordination file
cat > "$PROJECT_DIR/tasks/current-task.md" << EOF
# Current Task Context

**Project**: $PROJECT_DESCRIPTION  
**Branch**: $BRANCH_NAME  
**Status**: Specification Phase  
**Next Step**: Complete /specify command

## Task Assignment

**Current Owner**: Parent Agent  
**Phase**: Specification Creation  

## Context for Sub-Agents

When assigned to this project, sub-agents should:
1. Read the project spec from: \`$SPEC_FILE\`
2. Create findings in: \`$PROJECT_DIR/findings/[tool]-findings.md\`
3. Update task status in this file

## Cross-Tool Integration Points

- **dbt → Snowflake**: Schema and model coordination
- **Snowflake → Tableau**: Data source optimization  
- **Orchestra → All**: Pipeline scheduling and monitoring
- **Business Context → All**: Stakeholder requirements

---
*Updated: $(date '+%Y-%m-%d %H:%M:%S')*
EOF

if $JSON_MODE; then
    printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","PROJECT_NUM":"%s","PROJECT_DIR":"%s"}\n' \
        "$BRANCH_NAME" "$SPEC_FILE" "$PROJECT_NUM" "$PROJECT_DIR"
else
    # Output results for the LLM to use
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "SPEC_FILE: $SPEC_FILE"
    echo "PROJECT_NUM: $PROJECT_NUM"
    echo "PROJECT_DIR: $PROJECT_DIR"
fi