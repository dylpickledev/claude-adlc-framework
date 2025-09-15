#!/bin/bash

# D&A Agent Hub - Interactive Setup Script
# One-command setup: git clone -> ./setup.sh -> productive in 60 seconds

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
REPOS_CONFIG_FILE="$SCRIPT_DIR/config/repositories.json"

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
    log_step "Verifying Prerequisites"
    
    # Check for required tools only
    echo "Checking for required tools..."
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
    
    if ! command -v gh >/dev/null 2>&1; then
        MISSING_TOOLS+=("gh (GitHub CLI)")
    else
        DETECTED_TOOLS+="gh "
    fi
    
    if ! command -v claude >/dev/null 2>&1; then
        MISSING_TOOLS+=("claude")
    else
        DETECTED_TOOLS+="claude "
    fi
    
    # Optional tools (just report, don't scan filesystem)
    command -v dbt >/dev/null 2>&1 && DETECTED_TOOLS+="dbt "
    command -v snowsql >/dev/null 2>&1 && DETECTED_TOOLS+="snowsql "
    command -v psql >/dev/null 2>&1 && DETECTED_TOOLS+="postgresql "
    
    if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
        log_error "Missing required tools: ${MISSING_TOOLS[*]}"
        echo "Please install missing tools and run setup again"
        exit 1
    fi
    
    log_success "Found required tools: $DETECTED_TOOLS"
    log_info "All repositories will be cloned from configuration - no filesystem scanning needed"
}

# Load existing environment
load_existing_env() {
    if [ -f "$ENV_FILE" ]; then
        log_info "Loading existing environment configuration..."
        source "$ENV_FILE"
    fi
}

# Interactive credential collection - focus on dbt only
collect_credentials() {
    log_step "Credential Configuration"
    
    # Check if dbt credentials already exist
    if [ -n "$DBT_CLOUD_API_TOKEN" ] && [ -n "$DBT_CLOUD_ACCOUNT_ID" ]; then
        log_success "dbt Cloud credentials already configured"
        return 0
    fi
    
    echo "Setting up minimal dbt configuration for D&A Agent Hub..."
    
    # dbt Cloud - required for basic functionality
    prompt_required "DBT_CLOUD_API_TOKEN" "dbt Cloud API Token" "https://cloud.getdbt.com/#/profile/api/"
    prompt_required "DBT_CLOUD_ACCOUNT_ID" "dbt Cloud Account ID" "https://cloud.getdbt.com (check URL: /accounts/[ID]/)"
    
    log_info "Additional integrations can be added later by re-running setup"
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

# Generate environment file - minimal dbt setup
generate_env_file() {
    log_step "Generating Environment File"
    
    # Only update .env if dbt credentials are missing
    if [ -f "$ENV_FILE" ] && grep -q "DBT_CLOUD_API_TOKEN" "$ENV_FILE"; then
        log_success "Environment file already exists with dbt configuration"
        return 0
    fi
    
    # Create or append minimal dbt configuration
    if [ ! -f "$ENV_FILE" ]; then
        cat > "$ENV_FILE" << EOF
# D&A Agent Hub Environment Configuration
# Generated by interactive setup on $(date)

EOF
    fi
    
    # Add dbt configuration if provided
    if [ -n "$DBT_CLOUD_API_TOKEN" ]; then
        cat >> "$ENV_FILE" << EOF
# dbt Cloud Configuration
DBT_CLOUD_API_TOKEN=${DBT_CLOUD_API_TOKEN}
DBT_CLOUD_ACCOUNT_ID=${DBT_CLOUD_ACCOUNT_ID}
DBT_PROJECT_DIR=~/da-agent-hub/repos/dbt_cloud

EOF
        log_success "dbt configuration added to $ENV_FILE"
    fi
}

# Check if repository configuration exists and is valid
check_repos_config() {
    if [ ! -f "$REPOS_CONFIG_FILE" ]; then
        log_warning "Repository configuration file not found at $REPOS_CONFIG_FILE"
        return 1
    fi
    
    # Test JSON validity
    if ! python3 -c "import json; json.load(open('$REPOS_CONFIG_FILE'))" >/dev/null 2>&1; then
        log_error "Invalid JSON format in repository configuration file"
        return 1
    fi
    
    return 0
}

# Clone repositories from configuration
clone_repositories() {
    log_step "Cloning All Configured Repositories"
    
    if ! check_repos_config; then
        log_warning "Skipping repository cloning due to configuration issues"
        return 0
    fi
    
    # Check GitHub CLI authentication
    local gh_available=false
    if gh auth status >/dev/null 2>&1; then
        gh_available=true
        log_success "GitHub CLI authenticated - using gh repo clone"
    else
        log_warning "GitHub CLI not authenticated - some repositories may be inaccessible"
        log_info "Run 'gh auth login' to authenticate with GitHub"
    fi
    
    # Show what repositories will be cloned
    log_info "Repositories and knowledge sources to be cloned:"
    python3 -c "
import json

with open('$REPOS_CONFIG_FILE', 'r') as f:
    config = json.load(f)

repos = config.get('repos', {})
knowledge = config.get('knowledge', {})

if repos:
    print('  Code Repositories:')
    for repo_name, repo_config in repos.items():
        branch = repo_config.get('branch', 'main')
        print(f'    - {repo_name} ({branch} branch)')

if knowledge:
    print('  Knowledge Sources:')
    for kb_name, kb_config in knowledge.items():
        branch = kb_config.get('branch', 'main')
        print(f'    - {kb_name} ({branch} branch)')
"
    
    # Create directories
    mkdir -p repos knowledge
    
    # Parse repository configuration and clone
    GH_AVAILABLE="$gh_available" python3 -c "
import json
import subprocess
import os
import sys

def run_command(cmd, description):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f'✓ {description}')
            return True
        else:
            print(f'✗ {description}: {result.stderr.strip()}')
            return False
    except Exception as e:
        print(f'✗ {description}: {e}')
        return False

try:
    with open('$REPOS_CONFIG_FILE', 'r') as f:
        config = json.load(f)
    
    repos = config.get('repos', {})
    knowledge = config.get('knowledge', {})
    settings = config.get('settings', {})
    
    cloned_count = 0
    skipped_count = 0
    failed_count = 0
    
    # Process repos (clone to repos/)
    for repo_name, repo_config in repos.items():
        repo_path = f'repos/{repo_name}'
        
        # Skip if directory already exists and update_existing is False
        if os.path.exists(repo_path):
            if settings.get('update_existing', True):
                print(f'ℹ Updating existing repository: {repo_name}')
                if run_command(f'cd {repo_path} && git fetch --all', f'Fetch updates for {repo_name}'):
                    branch = repo_config.get('branch', 'main')
                    run_command(f'cd {repo_path} && git checkout {branch} && git pull origin {branch}', f'Update {repo_name} to latest {branch}')
                    cloned_count += 1
                else:
                    failed_count += 1
            else:
                print(f'⏭ Skipping existing repository: {repo_name}')
                skipped_count += 1
            continue
        
        # Clone repository using gh CLI or git fallback
        url = repo_config.get('url')
        branch = repo_config.get('branch', 'main')
        
        # Extract repo path from URL for gh CLI
        repo_identifier = ''
        if 'github.com' in url:
            # Extract owner/repo from URL (e.g., https://github.com/owner/repo.git -> owner/repo)
            parts = url.replace('https://github.com/', '').replace('git@github.com:', '').replace('.git', '')
            repo_identifier = parts
        
        # Use gh CLI for GitHub repositories if available
        gh_available = os.environ.get('GH_AVAILABLE', 'false')
        if repo_identifier and gh_available == 'true':
            clone_cmd = f'gh repo clone {repo_identifier} {repo_path} -- --branch {branch}'
            if run_command(clone_cmd, f'Clone {repo_name} ({branch} branch) via gh CLI'):
                cloned_count += 1
            else:
                # Fallback to git clone
                clone_cmd = f'git clone -b {branch} {url} {repo_path}'
                if run_command(clone_cmd, f'Fallback clone {repo_name} ({branch} branch)'):
                    cloned_count += 1
                else:
                    failed_count += 1
        else:
            # Use regular git clone for non-GitHub or when gh not available
            clone_cmd = f'git clone -b {branch} {url} {repo_path}'
            if run_command(clone_cmd, f'Clone {repo_name} ({branch} branch)'):
                cloned_count += 1
            else:
                failed_count += 1
    
    # Process knowledge sources (clone to knowledge/)
    for kb_name, kb_config in knowledge.items():
        kb_path = f'knowledge/{kb_name}'
        
        # Skip if directory already exists and update_existing is False
        if os.path.exists(kb_path):
            if settings.get('update_existing', True):
                print(f'ℹ Updating existing knowledge source: {kb_name}')
                if run_command(f'cd {kb_path} && git fetch --all', f'Fetch updates for {kb_name}'):
                    branch = kb_config.get('branch', 'main')
                    run_command(f'cd {kb_path} && git checkout {branch} && git pull origin {branch}', f'Update {kb_name} to latest {branch}')
                    cloned_count += 1
                else:
                    failed_count += 1
            else:
                print(f'⏭ Skipping existing knowledge source: {kb_name}')
                skipped_count += 1
            continue
        
        # Clone knowledge source using gh CLI or git fallback
        url = kb_config.get('url')
        branch = kb_config.get('branch', 'main')
        
        # Extract repo path from URL for gh CLI
        repo_identifier = ''
        if 'github.com' in url:
            # Extract owner/repo from URL (e.g., https://github.com/owner/repo.git -> owner/repo)
            parts = url.replace('https://github.com/', '').replace('git@github.com:', '').replace('.git', '')
            repo_identifier = parts
        
        # Use gh CLI for GitHub repositories if available
        gh_available = os.environ.get('GH_AVAILABLE', 'false')
        if repo_identifier and gh_available == 'true':
            clone_cmd = f'gh repo clone {repo_identifier} {kb_path} -- --branch {branch}'
            if run_command(clone_cmd, f'Clone {kb_name} ({branch} branch) via gh CLI'):
                cloned_count += 1
            else:
                # Fallback to git clone
                clone_cmd = f'git clone -b {branch} {url} {kb_path}'
                if run_command(clone_cmd, f'Fallback clone {kb_name} ({branch} branch)'):
                    cloned_count += 1
                else:
                    failed_count += 1
        else:
            # Use regular git clone for non-GitHub or when gh not available
            clone_cmd = f'git clone -b {branch} {url} {kb_path}'
            if run_command(clone_cmd, f'Clone {kb_name} ({branch} branch)'):
                cloned_count += 1
            else:
                failed_count += 1
    
    print(f'\\nRepository cloning summary:')
    print(f'  Cloned/Updated: {cloned_count}')
    print(f'  Skipped: {skipped_count}') 
    print(f'  Failed: {failed_count}')
    
except Exception as e:
    print(f'Error processing repository configuration: {e}')
    sys.exit(1)
"
    
    log_success "Repository cloning completed"
}

# Setup git worktrees for parallel development
setup_worktrees() {
    log_step "Setting Up Git Worktrees"
    
    mkdir -p worktrees
    
    log_info "Worktree directory created for parallel development"
    echo "Use git worktree commands to manage parallel branches:"
    echo "  ${CYAN}git worktree add worktrees/hotfix -b hotfix/issue-name${NC}"
    echo "  ${CYAN}git worktree add worktrees/feature -b feature/feature-name${NC}"
    echo "  ${CYAN}git worktree add worktrees/experiment -b experiment/idea${NC}"
    echo ""
    echo "Management commands:"
    echo "  ${CYAN}git worktree list${NC}                    # Show all worktrees"
    echo "  ${CYAN}git worktree remove worktrees/feature${NC} # Clean up when done"
    echo "  ${CYAN}git worktree prune${NC}                   # Remove stale references"
    
    log_success "Worktree structure ready for parallel development"
}

# Auto-setup repositories
setup_repositories() {
    log_step "Setting Up Repository Workspace"
    
    mkdir -p repos
    
    # Setup worktrees
    setup_worktrees
    
    # First, try to clone repositories from configuration
    if check_repos_config; then
        log_info "Repository configuration found - attempting to clone repositories"
        clone_repositories
    else
        log_info "No repository configuration found - falling back to local detection"
    fi
    
    # Note: All repositories are cloned from configuration to their respective directories
    
    # Report final repository status
    if [ -d "repos" ]; then
        REPO_COUNT=$(ls -1 repos/ 2>/dev/null | wc -l)
        log_success "Repository workspace configured with $REPO_COUNT repositories"
        
        # List what's available
        echo "Available repositories:"
        for repo in repos/*/; do
            if [ -d "$repo" ]; then
                repo_name=$(basename "$repo")
                echo "  - $repo_name (cloned)"
            fi
        done
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
    
    # Make all shell scripts executable
    make_scripts_executable
    
    # Skip gitignore creation - using existing .gitignore
    log_info "Using existing .gitignore configuration"
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

# Example: Custom repository setup
setup_personal_repos() {
    echo "Setting up personal repository configurations..."
    # Add additional repositories or modify clone behavior
    # Custom git configuration, branch preferences, etc.
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

1. Edit `customize.sh` to add your custom repository configurations
2. Run `./developer/customize.sh` after running the main setup
3. Add any personal files to this directory

## Git Ignore

This entire directory is ignored by git to keep personal configurations private.
EOF
    fi
}

# Make all shell scripts executable
make_scripts_executable() {
    echo "Making shell scripts executable..."
    
    # Find and make executable all .sh files in the project
    find . -name "*.sh" -type f -exec chmod +x {} \;
    
    # Also handle Python scripts that should be executable
    if [ -f "scripts/manage-mcp.py" ]; then
        chmod +x scripts/manage-mcp.py
    fi
    
    log_success "Shell scripts are now executable"
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

# Cloned repositories (will be recreated by setup)
repos/*
knowledge/*

# Git worktrees (local development branches)
worktrees/

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
        REPO_COUNT=$(ls -1 repos/ 2>/dev/null | wc -l)
        log_success "Repository workspace: $REPO_COUNT repositories cloned"
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
    echo "  ./setup.sh        Run interactive setup"
    echo "  ./setup.sh --status    Show current status"
    echo "  ./setup.sh --help      Show this help"
    exit 0
fi

# Run main setup if no arguments or unrecognized arguments
main "$@"