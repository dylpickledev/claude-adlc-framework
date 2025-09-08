#!/bin/bash

# D&A Agent Hub - Interactive Setup Script
# One-command setup: git clone -> ./setup-interactive.sh -> productive in 60 seconds

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CLAUDE_CONFIG_DIR="$HOME/.claude"
ENV_FILE="$SCRIPT_DIR/.env"

# Logging functions
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }
log_step() { echo -e "\n${BOLD}${CYAN}=== $1 ===${NC}"; }

# Interactive prompts
prompt_required() {
    local var_name="$1"
    local description="$2"
    local help_url="$3"
    local current_value="${!var_name}"
    
    echo -e "\n${BOLD}$description${NC}"
    if [ -n "$help_url" ]; then
        echo -e "${CYAN}Get this at: $help_url${NC}"
    fi
    
    if [ -n "$current_value" ] && [ "$current_value" != "your_${var_name,,}_here" ]; then
        echo -e "Current value: ${YELLOW}[HIDDEN]${NC}"
        read -p "Keep current value? [Y/n]: " keep_current
        if [[ $keep_current =~ ^[Nn]$ ]]; then
            read -p "Enter new value: " new_value
            export "$var_name"="$new_value"
        fi
    else
        read -p "Enter value: " new_value
        export "$var_name"="$new_value"
    fi
}

prompt_optional() {
    local var_name="$1"
    local description="$2"
    local default="$3"
    local current_value="${!var_name}"
    
    echo -e "\n${description} (optional)"
    if [ -n "$current_value" ] && [ "$current_value" != "$default" ]; then
        read -p "Current: $current_value. Change? [y/N]: " change
        if [[ $change =~ ^[Yy]$ ]]; then
            read -p "New value [$default]: " new_value
            export "$var_name"="${new_value:-$default}"
        fi
    else
        read -p "Enter value [$default]: " new_value
        export "$var_name"="${new_value:-$default}"
    fi
}

# Environment detection
detect_environment() {
    log_step "Detecting Your Environment"
    
    # Detect dbt projects
    echo "Scanning for dbt projects..."
    DBT_PROJECTS=$(find "$HOME" -name "dbt_project.yml" -not -path "*/venv/*" -not -path "*/node_modules/*" 2>/dev/null | head -5)
    if [ -n "$DBT_PROJECTS" ]; then
        log_success "Found dbt projects:"
        echo "$DBT_PROJECTS" | while read project; do
            echo "  - $(dirname "$project")"
        done
        DETECTED_DBT_PATH=$(dirname $(echo "$DBT_PROJECTS" | head -1))
    else
        log_warning "No dbt projects found"
    fi
    
    # Detect git repositories
    echo "Scanning for git repositories..."
    GIT_REPOS=$(find "$HOME" -name ".git" -type d -not -path "*/.*/*" 2>/dev/null | head -10)
    REPO_COUNT=$(echo "$GIT_REPOS" | wc -l)
    if [ -n "$GIT_REPOS" ]; then
        log_success "Found $REPO_COUNT git repositories"
    fi
    
    # Check for common tools and prerequisites
    echo "Checking for installed tools..."
    DETECTED_TOOLS=""
    MISSING_TOOLS=()
    
    # Required tools
    if ! command -v python3 >/dev/null 2>&1; then
        MISSING_TOOLS+=("python3")
    else
        DETECTED_TOOLS+="python3 "
    fi
    
    if ! command -v git >/dev/null 2>&1; then
        MISSING_TOOLS+=("git")
    else
        DETECTED_TOOLS+="git "
    fi
    
    if ! command -v claude >/dev/null 2>&1; then
        MISSING_TOOLS+=("claude")
    else
        DETECTED_TOOLS+="claude "
    fi
    
    # Optional tools
    command -v dbt >/dev/null 2>&1 && DETECTED_TOOLS+="dbt "
    command -v snowsql >/dev/null 2>&1 && DETECTED_TOOLS+="snowsql "
    command -v psql >/dev/null 2>&1 && DETECTED_TOOLS+="postgresql "
    
    if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
        log_error "Missing required tools: ${MISSING_TOOLS[*]}"
        echo "Please install missing tools and run setup again"
        exit 1
    fi
    
    if [ -n "$DETECTED_TOOLS" ]; then
        log_success "Found tools: $DETECTED_TOOLS"
    fi
}

# Load existing environment
load_existing_env() {
    if [ -f "$ENV_FILE" ]; then
        log_info "Loading existing environment configuration..."
        source "$ENV_FILE"
    fi
}

# Interactive credential collection
collect_credentials() {
    log_step "Credential Configuration"
    
    echo "I'll ask for credentials for tools you want to use. Skip any you don't need."
    
    # dbt Cloud
    read -p "Configure dbt Cloud integration? [Y/n]: " setup_dbt
    if [[ ! $setup_dbt =~ ^[Nn]$ ]]; then
        prompt_required "DBT_CLOUD_API_TOKEN" "dbt Cloud API Token" "https://cloud.getdbt.com/#/profile/api/"
        prompt_required "DBT_CLOUD_ACCOUNT_ID" "dbt Cloud Account ID" "https://cloud.getdbt.com (check URL: /accounts/[ID]/)"
    fi
    
    # Snowflake
    read -p "Configure Snowflake integration? [Y/n]: " setup_snowflake
    if [[ ! $setup_snowflake =~ ^[Nn]$ ]]; then
        prompt_required "SNOWFLAKE_ACCOUNT" "Snowflake Account (format: org-account.region)" ""
        prompt_required "SNOWFLAKE_USER" "Snowflake Username" ""
        prompt_required "SNOWFLAKE_PASSWORD" "Snowflake Password" ""
        prompt_optional "SNOWFLAKE_WAREHOUSE" "Snowflake Warehouse" "COMPUTE_WH"
        prompt_optional "SNOWFLAKE_DATABASE" "Snowflake Database" "ANALYTICS"
        prompt_optional "SNOWFLAKE_SCHEMA" "Snowflake Schema" "PUBLIC"
        prompt_optional "SNOWFLAKE_ROLE" "Snowflake Role" "ANALYST"
    fi
    
    # Freshservice
    read -p "Configure Freshservice integration? [y/N]: " setup_freshservice
    if [[ $setup_freshservice =~ ^[Yy]$ ]]; then
        prompt_required "FRESHSERVICE_APIKEY" "Freshservice API Key" "https://your-domain.freshservice.com/admin/api_keys"
        prompt_required "FRESHSERVICE_DOMAIN" "Freshservice Domain (e.g., company.freshservice.com)" ""
    fi
    
    # GitHub
    read -p "Configure GitHub integration? [y/N]: " setup_github
    if [[ $setup_github =~ ^[Yy]$ ]]; then
        prompt_required "GITHUB_PERSONAL_ACCESS_TOKEN" "GitHub Personal Access Token" "https://github.com/settings/tokens"
    fi
}

# Test connections
test_connections() {
    log_step "Testing Connections"
    
    # Test dbt Cloud
    if [ -n "$DBT_CLOUD_API_TOKEN" ] && [ -n "$DBT_CLOUD_ACCOUNT_ID" ]; then
        echo "Testing dbt Cloud connection..."
        if curl -s -f -H "Authorization: Token $DBT_CLOUD_API_TOKEN" \
            "https://cloud.getdbt.com/api/v2/accounts/$DBT_CLOUD_ACCOUNT_ID/" >/dev/null; then
            log_success "dbt Cloud connection successful"
        else
            log_warning "dbt Cloud connection failed - check your credentials"
        fi
    fi
    
    # Test Snowflake (basic format check)
    if [ -n "$SNOWFLAKE_ACCOUNT" ] && [ -n "$SNOWFLAKE_USER" ]; then
        echo "Validating Snowflake configuration..."
        if [[ $SNOWFLAKE_ACCOUNT =~ ^[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+$ ]]; then
            log_success "Snowflake account format looks correct"
        else
            log_warning "Snowflake account should be in format: org-account.region"
        fi
    fi
}

# Generate environment file
generate_env_file() {
    log_step "Generating Environment File"
    
    cat > "$ENV_FILE" << EOF
# D&A Agent Hub Environment Configuration
# Generated by interactive setup on $(date)

EOF
    
    # Add dbt configuration if provided
    if [ -n "$DBT_CLOUD_API_TOKEN" ]; then
        cat >> "$ENV_FILE" << EOF
# dbt Cloud Configuration
DBT_CLOUD_API_TOKEN=${DBT_CLOUD_API_TOKEN}
DBT_CLOUD_ACCOUNT_ID=${DBT_CLOUD_ACCOUNT_ID}

EOF
    fi
    
    # Add Snowflake configuration if provided
    if [ -n "$SNOWFLAKE_ACCOUNT" ]; then
        cat >> "$ENV_FILE" << EOF
# Snowflake Configuration
SNOWFLAKE_ACCOUNT=${SNOWFLAKE_ACCOUNT}
SNOWFLAKE_USER=${SNOWFLAKE_USER}
SNOWFLAKE_PASSWORD=${SNOWFLAKE_PASSWORD}
SNOWFLAKE_WAREHOUSE=${SNOWFLAKE_WAREHOUSE:-COMPUTE_WH}
SNOWFLAKE_DATABASE=${SNOWFLAKE_DATABASE:-ANALYTICS}
SNOWFLAKE_SCHEMA=${SNOWFLAKE_SCHEMA:-PUBLIC}
SNOWFLAKE_ROLE=${SNOWFLAKE_ROLE:-ANALYST}

EOF
    fi
    
    # Add GitHub configuration if provided
    if [ -n "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
        cat >> "$ENV_FILE" << EOF
# GitHub Configuration
GITHUB_PERSONAL_ACCESS_TOKEN=${GITHUB_PERSONAL_ACCESS_TOKEN}

EOF
    fi
    
    # Add Freshservice configuration if provided
    if [ -n "$FRESHSERVICE_APIKEY" ]; then
        cat >> "$ENV_FILE" << EOF
# Freshservice Configuration
FRESHSERVICE_APIKEY=${FRESHSERVICE_APIKEY}
FRESHSERVICE_DOMAIN=${FRESHSERVICE_DOMAIN}

EOF
    fi
    
    log_success "Environment file created at $ENV_FILE"
}

# Auto-setup repositories
setup_repositories() {
    log_step "Setting Up Repository Workspace"
    
    mkdir -p repos
    
    if [ -n "$DETECTED_DBT_PATH" ]; then
        ln -sf "$DETECTED_DBT_PATH" repos/dbt 2>/dev/null || true
        log_success "Linked dbt project: $DETECTED_DBT_PATH -> repos/dbt"
    fi
    
    # Link other common repositories found nearby
    if [ -n "$GIT_REPOS" ]; then
        echo "$GIT_REPOS" | while read git_dir; do
            repo_path=$(dirname "$git_dir")
            repo_name=$(basename "$repo_path")
            
            # Skip if already linked or if it's this repo
            if [ "$repo_path" != "$SCRIPT_DIR" ] && [ ! -e "repos/$repo_name" ]; then
                ln -sf "$repo_path" "repos/$repo_name" 2>/dev/null || true
            fi
        done
        log_success "Repository workspace configured"
    fi
}

# Setup technical components
setup_technical() {
    log_step "Installing Technical Components"
    
    # Python environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_success "Created Python virtual environment"
    fi
    
    source venv/bin/activate
    pip install --upgrade pip >/dev/null 2>&1
    
    # Install uvx if needed
    if ! command -v uvx >/dev/null 2>&1; then
        pip install uvx >/dev/null 2>&1
        log_success "Installed uvx for MCP packages"
    fi
    
    # Setup agents
    mkdir -p ~/.claude/agents
    if [ -d ".claude/agents" ]; then
        cp .claude/agents/*.md ~/.claude/agents/ 2>/dev/null || true
        log_success "Copied agents to ~/.claude/agents"
    fi
    
    # Copy Claude configuration
    if [ -f "CLAUDE.md" ]; then
        cp "CLAUDE.md" ~/.claude/CLAUDE.md
        log_success "Updated Claude configuration"
    fi
    
    # Setup developer customization framework
    setup_developer_customization
    
    # Create comprehensive gitignore
    create_comprehensive_gitignore
}

# Setup developer customization framework
setup_developer_customization() {
    echo "Setting up developer customization framework..."
    
    # Create developer directory structure
    mkdir -p developer/{scripts,configs,knowledge}
    
    # Create customization template if it doesn't exist
    if [ ! -f "developer/customize.sh" ]; then
        cat > developer/customize.sh << 'EOF'
#!/bin/bash

# Developer Customization Script
# Add your personal configuration here

# Example: Custom repository symlinks
setup_personal_repos() {
    echo "Setting up personal repository symlinks..."
    # ln -sf /path/to/your/dbt/project repos/dbt
    # ln -sf /path/to/your/dlthub/project repos/dlthub
}

# Example: Custom environment variables
setup_personal_env() {
    echo "Setting up personal environment..."
    # Additional environment setup
}

# Example: Custom MCP servers
setup_personal_mcp() {
    echo "Setting up personal MCP servers..."
    # Additional MCP server configuration
}

# Run customizations
main() {
    setup_personal_repos
    setup_personal_env
    setup_personal_mcp
    echo "Personal customization completed"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
EOF
        chmod +x developer/customize.sh
    fi
    
    # Create README if it doesn't exist
    if [ ! -f "developer/README.md" ]; then
        cat > developer/README.md << 'EOF'
# Developer Customization

This directory contains your personal customizations that won't be committed to the shared repository.

## Files

- `customize.sh` - Your personal setup script
- `scripts/` - Custom scripts
- `configs/` - Personal configuration files
- `knowledge/` - Personal knowledge base files

## Usage

1. Edit `customize.sh` to add your repository paths and custom configuration
2. Run `./developer/customize.sh` after running the main setup
3. Add any personal files to this directory

## Git Ignore

This entire directory is ignored by git to keep personal configurations private.
EOF
    fi
}

# Create comprehensive gitignore
create_comprehensive_gitignore() {
    echo "Creating comprehensive .gitignore..."
    
    cat > .gitignore << 'EOF'
# Environment files
.env
*.env

# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node.js (for ClickUp MCP)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Developer customizations
developer/

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
.tmp/

# Repository symlinks (will be recreated)
repos/*

# Claude local configurations
.claude/mcp.local.json
.claude/settings.local.json
EOF
}

# Setup MCP servers
setup_mcp_servers() {
    log_step "Configuring MCP Servers"
    
    if [ -f "scripts/manage-mcp.py" ]; then
        python scripts/manage-mcp.py add >/dev/null 2>&1
        log_success "MCP servers configured"
    else
        log_warning "MCP management script not found"
    fi
}

# Final validation
final_validation() {
    log_step "Final Validation"
    
    # Check that Claude can be restarted
    echo "Checking Claude CLI..."
    if command -v claude >/dev/null 2>&1; then
        log_success "Claude CLI available"
    else
        log_warning "Claude CLI not found - you may need to install it"
    fi
    
    # Check MCP configuration
    if [ -f ~/.claude/mcp.json ]; then
        log_success "MCP configuration file exists"
    else
        log_warning "MCP configuration not found"
    fi
    
    # Check environment
    if [ -f "$ENV_FILE" ]; then
        log_success "Environment configuration ready"
    fi
    
    # Count configured integrations
    INTEGRATION_COUNT=0
    [ -n "$DBT_CLOUD_API_TOKEN" ] && ((INTEGRATION_COUNT++))
    [ -n "$SNOWFLAKE_ACCOUNT" ] && ((INTEGRATION_COUNT++))
    [ -n "$FRESHSERVICE_APIKEY" ] && ((INTEGRATION_COUNT++))
    [ -n "$GITHUB_PERSONAL_ACCESS_TOKEN" ] && ((INTEGRATION_COUNT++))
    
    log_success "Setup complete with $INTEGRATION_COUNT integrations configured"
}

# Main setup process
main() {
    echo -e "${BOLD}${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════════════════════╗"
    echo "║                        D&A Agent Hub Interactive Setup                        ║"
    echo "║                    One command → Productive in 60 seconds                     ║"
    echo "╚════════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
    
    detect_environment
    load_existing_env
    collect_credentials
    test_connections
    generate_env_file
    setup_repositories
    setup_technical
    setup_mcp_servers
    final_validation
    
    echo -e "\n${BOLD}${GREEN}🎉 Setup Complete!${NC}\n"
    echo -e "${BOLD}Next Steps:${NC}"
    echo -e "  1. ${CYAN}claude restart${NC} - Restart Claude to load MCP servers"
    echo -e "  2. ${CYAN}./setup.sh --status${NC} - Check system status"
    echo -e "  3. ${CYAN}./developer/customize.sh${NC} - Add your personal repository paths"
    echo -e "  4. ${CYAN}Ask me: \"What dbt models need optimization?\"${NC}\n"
    
    echo -e "${BOLD}Available Slash Commands:${NC}"
    echo -e "  ${CYAN}/setup${NC} - Run this interactive setup again"
    echo -e "  ${CYAN}/coordinate-agents${NC} - Coordinate multiple expert agents"
    echo -e "  ${CYAN}/sherlock${NC} - Investigate data quality issues"
    echo -e "  ${CYAN}/status${NC} - Check system and integration status\n"
    
    if [ -f "scripts/manage-mcp.py" ]; then
        echo -e "${BOLD}Additional Tools:${NC}"
        echo -e "  ${CYAN}python scripts/manage-mcp.py [add|remove|list|status]${NC} - Manage MCP servers"
        echo -e "  ${CYAN}scripts/test-setup.sh${NC} - Validate configuration\n"
    fi
    
    echo -e "You can now start asking questions about your data stack!"
}

# Handle command line arguments
if [ "$1" = "--status" ]; then
    log_step "D&A Agent Hub Status"
    
    # Environment check
    if [ -f "$ENV_FILE" ]; then
        log_success "Environment configured"
        echo "  Configured integrations:"
        grep -v '^#' "$ENV_FILE" | grep -v '^$' | cut -d'=' -f1 | sed 's/^/    - /'
    else
        log_warning "No environment file found"
    fi
    
    # Repository check
    if [ -d "repos" ]; then
        REPO_COUNT=$(ls -la repos/ 2>/dev/null | grep '^l' | wc -l)
        log_success "Repository workspace: $REPO_COUNT repositories linked"
    else
        log_warning "Repository workspace not configured"
    fi
    
    # MCP check
    if [ -f ~/.claude/mcp.json ]; then
        log_success "MCP servers configured"
    else
        log_warning "MCP servers not configured"
    fi
    
    # Agent check
    if [ -d ~/.claude/agents ]; then
        AGENT_COUNT=$(ls ~/.claude/agents/*.md 2>/dev/null | wc -l)
        log_success "Agents available: $AGENT_COUNT"
    else
        log_warning "No agents configured"
    fi
    
    exit 0
elif [ "$1" = "--help" ]; then
    echo "D&A Agent Hub Setup"
    echo ""
    echo "Usage:"
    echo "  ./setup-interactive.sh        Run interactive setup"
    echo "  ./setup-interactive.sh --status    Show current status"
    echo "  ./setup-interactive.sh --help      Show this help"
    exit 0
fi

# Run main setup if no arguments or unrecognized arguments
main "$@"