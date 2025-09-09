#!/usr/bin/env bash
# Check data analytics task prerequisites and return available documents
# Returns project directory and list of available design documents
# Usage: ./check-data-task-prerequisites.sh [--json]

set -e

JSON_MODE=false
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json]"; exit 0 ;;
    esac
done

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

# Check for required files
REQUIRED_FILES=("spec.md" "plan.md")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$PROJECT_DIR/$file" ]; then
        echo "Error: Required file $file not found in $PROJECT_DIR" >&2
        echo "Make sure to run /specify and /plan commands first." >&2
        exit 1
    fi
done

# Build list of available documents
AVAILABLE_DOCS=()

# Always include core documents
AVAILABLE_DOCS+=("plan.md")

# Check for optional documents
if [ -f "$PROJECT_DIR/data-model.md" ]; then
    AVAILABLE_DOCS+=("data-model.md")
fi

if [ -f "$PROJECT_DIR/research.md" ]; then
    AVAILABLE_DOCS+=("research.md")
fi

if [ -f "$PROJECT_DIR/quickstart.md" ]; then
    AVAILABLE_DOCS+=("quickstart.md")
fi

# Check for contracts directory and files
if [ -d "$PROJECT_DIR/contracts" ]; then
    CONTRACT_FILES=($(find "$PROJECT_DIR/contracts" -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.sql" 2>/dev/null | sort))
    if [ ${#CONTRACT_FILES[@]} -gt 0 ]; then
        for file in "${CONTRACT_FILES[@]}"; do
            # Make path relative to project directory
            REL_PATH=${file#$PROJECT_DIR/}
            AVAILABLE_DOCS+=("$REL_PATH")
        done
    fi
fi

# Update task coordination file
cat > "$PROJECT_DIR/tasks/current-task.md" << EOF
# Current Task Context

**Project**: $(basename "$PROJECT_DIR")  
**Branch**: $CURRENT_BRANCH  
**Status**: Task Generation Phase  
**Next Step**: Complete /tasks command

## Task Assignment

**Current Owner**: Parent Agent  
**Phase**: Task Breakdown and Assignment  

## Available Documents

$(for doc in "${AVAILABLE_DOCS[@]}"; do echo "- **$doc**: \`$PROJECT_DIR/$doc\`"; done)

## Context for Sub-Agents

When assigned to this project, sub-agents should:
1. Read available design documents listed above
2. Execute assigned tasks from: \`$PROJECT_DIR/tasks.md\`
3. Document findings in: \`$PROJECT_DIR/findings/[tool]-findings.md\`
4. Update task status in tasks.md

## Cross-Tool Integration Points

- **dbt → Snowflake**: Schema and model coordination
- **Snowflake → Tableau**: Data source optimization  
- **Orchestra → All**: Pipeline scheduling and monitoring
- **Business Context → All**: Stakeholder requirements and validation

---
*Updated: $(date '+%Y-%m-%d %H:%M:%S')*
EOF

# Prepare JSON array of available docs
JSON_DOCS="["
for i in "${!AVAILABLE_DOCS[@]}"; do
    if [ $i -gt 0 ]; then
        JSON_DOCS+=","
    fi
    JSON_DOCS+="\"${AVAILABLE_DOCS[$i]}\""
done
JSON_DOCS+="]"

if $JSON_MODE; then
    printf '{"PROJECT_DIR":"%s","AVAILABLE_DOCS":%s,"BRANCH":"%s"}\n' \
        "$PROJECT_DIR" "$JSON_DOCS" "$CURRENT_BRANCH"
else
    # Output for LLM use
    echo "PROJECT_DIR: $PROJECT_DIR"
    echo "AVAILABLE_DOCS: ${AVAILABLE_DOCS[*]}"
    echo "BRANCH: $CURRENT_BRANCH"
fi