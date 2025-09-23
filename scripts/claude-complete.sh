#!/bin/bash

# claude-complete.sh - Claude-powered project completion script
# This script is designed to be run by GitHub Actions or manually
# to complete projects with AI assistance

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${BLUE}🤖 $1${NC}"
}

# Usage function
usage() {
    echo "Usage: $0 [project-name]"
    echo ""
    echo "Claude-powered project completion script"
    echo ""
    echo "Arguments:"
    echo "  project-name    Name of the project to complete (optional, auto-detected if in project branch)"
    echo ""
    echo "Environment Variables:"
    echo "  CLAUDE_API_KEY  Anthropic API key (required)"
    echo "  PROJECT_DIR     Override project directory detection"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Auto-detect project from current branch"
    echo "  $0 feature-analytics-dashboard       # Complete specific project"
    echo ""
    exit 1
}

# Check dependencies
check_dependencies() {
    print_info "Checking dependencies..."

    # Check for git
    if ! command -v git &> /dev/null; then
        print_error "Git is required but not installed"
        exit 1
    fi

    # Check for Claude CLI or curl
    if command -v claude &> /dev/null; then
        CLAUDE_METHOD="cli"
        print_info "Using Claude CLI"
    elif command -v curl &> /dev/null; then
        CLAUDE_METHOD="api"
        print_info "Using Claude API via curl"
    else
        print_error "Neither Claude CLI nor curl found. Please install one."
        exit 1
    fi

    # Check for API key
    if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$CLAUDE_API_KEY" ]; then
        print_error "ANTHROPIC_API_KEY or CLAUDE_API_KEY environment variable required"
        exit 1
    fi

    print_status "Dependencies verified"
}

# Auto-detect project information
detect_project() {
    local project_name="$1"
    local project_dir=""
    local current_branch=""

    print_info "Detecting project information..."

    # Get current branch
    if git rev-parse --git-dir > /dev/null 2>&1; then
        current_branch=$(git rev-parse --abbrev-ref HEAD)
        print_info "Current branch: $current_branch"
    else
        print_error "Not in a git repository"
        exit 1
    fi

    # Determine project name and directory
    if [ -n "$project_name" ]; then
        # Use provided project name
        project_dir="projects/active/$project_name"
    elif [ -n "$PROJECT_DIR" ]; then
        # Use environment variable
        project_dir="$PROJECT_DIR"
        project_name=$(basename "$project_dir")
    else
        # Auto-detect from branch name or current directory
        if [[ "$current_branch" =~ ^(feature|fix|research)- ]]; then
            project_name="$current_branch"
            project_dir="projects/active/$current_branch"
        else
            # Search for project directories matching current branch
            project_dir=$(find projects/active -maxdepth 1 -type d -name "*$current_branch*" 2>/dev/null | head -1)
            if [ -n "$project_dir" ]; then
                project_name=$(basename "$project_dir")
            fi
        fi
    fi

    # Validate project directory exists
    if [ ! -d "$project_dir" ]; then
        print_error "Project directory not found: $project_dir"
        print_info "Available projects:"
        ls -la projects/active/ 2>/dev/null || print_info "No active projects found"
        exit 1
    fi

    echo "$project_dir|$project_name|$current_branch"
}

# Load project context
load_project_context() {
    local project_dir="$1"
    local spec_content=""
    local context_content=""
    local readme_content=""

    print_info "Loading project context from $project_dir..."

    # Load specification
    if [ -f "$project_dir/spec.md" ]; then
        spec_content=$(cat "$project_dir/spec.md")
        print_info "Loaded project specification"
    fi

    # Load context
    if [ -f "$project_dir/context.md" ]; then
        context_content=$(cat "$project_dir/context.md")
        print_info "Loaded project context"
    fi

    # Load README
    if [ -f "$project_dir/README.md" ]; then
        readme_content=$(cat "$project_dir/README.md")
        print_info "Loaded project README"
    fi

    # Combine all context
    local full_context=""
    if [ -n "$spec_content" ]; then
        full_context="## Project Specification\n$spec_content\n\n"
    fi
    if [ -n "$context_content" ]; then
        full_context="${full_context}## Project Context\n$context_content\n\n"
    fi
    if [ -n "$readme_content" ]; then
        full_context="${full_context}## Project README\n$readme_content\n\n"
    fi

    echo -e "$full_context"
}

# Create completion prompt
create_completion_prompt() {
    local project_name="$1"
    local current_branch="$2"
    local project_context="$3"

    cat << EOF
# Automated Project Completion Request

You are Claude, invoked to complete a da-agent-hub project that needs finishing touches before merge.

## Project Information
- **Project Name**: $project_name
- **Current Branch**: $current_branch
- **Execution Context**: Automated completion via claude-complete.sh script
- **Goal**: Complete project to production-ready status

## Project Context
$project_context

## Your Task

Please complete this project by following these steps:

### 1. Current State Analysis
- Review what has been implemented so far
- Identify any existing files, scripts, or documentation
- Understand the project's scope and objectives

### 2. Gap Identification
- Determine what functionality is missing or incomplete
- Identify documentation gaps
- Check for error handling and edge cases
- Assess integration with da-agent-hub workflows

### 3. Implementation Completion
- Add any missing core functionality
- Implement proper error handling
- Create comprehensive documentation
- Add usage examples and testing instructions
- Ensure integration with existing tools and workflows

### 4. Quality Assurance
- Verify all code follows da-agent-hub conventions
- Ensure proper file permissions and executable scripts
- Test integration with existing commands and tools
- Validate documentation completeness and accuracy

### 5. Final Polish
- Clean up any rough edges in implementation
- Optimize for performance and user experience
- Ensure consistent formatting and style
- Add any helpful comments or explanations

## Completion Criteria

The project should be considered complete when:
- ✅ All core functionality is implemented and tested
- ✅ Comprehensive documentation with usage examples
- ✅ Proper error handling and edge case coverage
- ✅ Integration with da-agent-hub ADLC workflow
- ✅ Ready for merge to main branch without additional work

## Available Tools and Context

You have access to:
- All da-agent-hub scripts in \`scripts/\` directory
- Specialist agents (dbt-expert, snowflake-expert, etc.)
- Project management tools and workflows
- Git operations and branch management
- File system operations for implementation

## Output Format

Please provide:
1. **Analysis Summary**: What you found and what needs completion
2. **Implementation Plan**: Step-by-step completion approach
3. **Execution**: Actual implementation of missing pieces
4. **Validation**: Testing and verification of completed work
5. **Documentation**: Final documentation and usage guidance

Begin with your analysis and proceed with completion.
EOF
}

# Execute Claude completion
execute_claude_completion() {
    local prompt="$1"
    local temp_file=$(mktemp)

    print_header "Executing Claude project completion..."

    # Write prompt to temporary file
    echo "$prompt" > "$temp_file"

    if [ "$CLAUDE_METHOD" = "cli" ]; then
        # Use Claude CLI
        print_info "Invoking Claude CLI for project completion..."
        claude < "$temp_file"
    else
        # Use Claude API directly
        print_info "Invoking Claude API for project completion..."

        local api_key="${ANTHROPIC_API_KEY:-$CLAUDE_API_KEY}"
        # Create properly escaped JSON payload
        local content=$(cat "$temp_file" | python3 -c "import sys, json; print(json.dumps(sys.stdin.read()))")
        local response=$(curl -s -X POST https://api.anthropic.com/v1/messages \
            -H "Content-Type: application/json" \
            -H "X-API-Key: $api_key" \
            -H "anthropic-version: 2023-06-01" \
            -d '{
                "model": "claude-3-5-sonnet",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": '"$content"'
                    }
                ]
            }')

        # Extract and display response
        echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['content'][0]['text'])" 2>/dev/null || {
            print_error "Failed to parse Claude API response"
            echo "Raw response: $response"
            rm -f "$temp_file"
            exit 1
        }
    fi

    # Clean up
    rm -f "$temp_file"
    print_status "Claude completion execution finished"
}

# Main execution
main() {
    local project_name="$1"

    print_header "Starting Claude-powered project completion..."

    # Check dependencies
    check_dependencies

    # Detect project information
    local project_info
    project_info=$(detect_project "$project_name")
    local project_dir=$(echo "$project_info" | cut -d'|' -f1)
    local detected_project_name=$(echo "$project_info" | cut -d'|' -f2)
    local current_branch=$(echo "$project_info" | cut -d'|' -f3)

    print_status "Project detected: $detected_project_name"
    print_info "Project directory: $project_dir"
    print_info "Current branch: $current_branch"

    # Load project context
    local project_context
    project_context=$(load_project_context "$project_dir")

    # Create completion prompt
    local completion_prompt
    completion_prompt=$(create_completion_prompt "$detected_project_name" "$current_branch" "$project_context")

    # Execute Claude completion
    execute_claude_completion "$completion_prompt"

    print_status "🎯 Claude project completion workflow finished!"
    print_info "Review the output above for implementation details and next steps."
}

# Handle command line arguments
case "${1:-}" in
    -h|--help)
        usage
        ;;
    *)
        main "$@"
        ;;
esac