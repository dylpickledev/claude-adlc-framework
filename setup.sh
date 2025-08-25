#!/bin/bash

# D&A Agent Hub Setup Script
# Configures Claude Code sub-agents for data stack navigation
# Supports macOS development environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CLAUDE_CONFIG_DIR="$HOME/.claude"
CLAUDE_MD_PATH="$CLAUDE_CONFIG_DIR/CLAUDE.md"
MCP_CONFIG_PATH="$CLAUDE_CONFIG_DIR/mcp.json"

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if running on macOS
    if [[ "$OSTYPE" != "darwin"* ]]; then
        log_warning "This script is optimized for macOS but will attempt to continue"
    fi
    
    # Check for required tools
    local missing_tools=()
    
    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi
    
    if ! command -v git &> /dev/null; then
        missing_tools+=("git")
    fi
    
    if ! command -v claude &> /dev/null; then
        missing_tools+=("claude")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_info "Please install missing tools and run setup again"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Create Python virtual environment
setup_python_env() {
    log_info "Setting up Python environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_success "Created Python virtual environment"
    else
        log_info "Python virtual environment already exists"
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    log_success "Python environment activated"
}

# Install MCP servers
install_mcp_servers() {
    log_info "Installing MCP servers..."
    
    # Install uvx for Python MCP packages
    if ! command -v uvx &> /dev/null; then
        log_info "Installing uvx..."
        pip install uvx
    fi
    
    log_info "uvx installed - MCP servers will be installed on-demand"
    log_success "MCP server prerequisites installed"
}

# Setup Claude configuration
setup_claude_config() {
    log_info "Setting up Claude configuration..."
    
    # Create Claude config directory
    mkdir -p "$CLAUDE_CONFIG_DIR"
    
    # Copy CLAUDE.md context file
    if [ -f "$SCRIPT_DIR/config/CLAUDE.md" ]; then
        cp "$SCRIPT_DIR/config/CLAUDE.md" "$CLAUDE_MD_PATH"
        log_success "Copied CLAUDE.md context file"
    else
        log_warning "CLAUDE.md template not found, will create basic version"
        cat > "$CLAUDE_MD_PATH" << 'EOF'
# D&A Agent Hub - Claude Code Context

This is the operational context for the D&A (Data & Analytics) Agent Hub.

## Current Project State

**Working Directory**: `${SCRIPT_DIR}`
**Setup Status**: Configured with MCP servers
**Environment**: Development environment

## Available Sub-Agents

### Business Context Agent
**Purpose**: Flexible document retrieval and business knowledge management
**Location**: `agents/business-context/`

### Tool Experts
- **dbt Expert**: `agents/dbt-expert/`
- **Orchestra Expert**: `agents/orchestra-expert/`
- **Tableau Expert**: `agents/tableau-expert/`
- **Snowflake Expert**: `agents/snowflake-expert/`
- **dlthub Expert**: `agents/dlthub-expert/`

## Usage Pattern

1. Use sub-agents as researchers and planners only
2. Store context in `.claude/tasks/` for communication
3. Parent agent implements based on sub-agent findings
4. Maintain separation between research and implementation
EOF
    fi
    
    # Setup MCP servers using Python script
    if [ -f "$SCRIPT_DIR/scripts/add-mcp-servers.py" ]; then
        python "$SCRIPT_DIR/scripts/add-mcp-servers.py"
        log_success "MCP servers configured"
    else
        log_warning "MCP server configuration script not found"
    fi
}

# Add MCP servers to Claude configuration
add_mcp_servers() {
    log_info "Configuring MCP servers..."
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        log_warning ".env file not found. MCP servers will be configured but may not connect without environment variables."
        log_info "Copy .env.template to .env and configure your credentials"
    fi
    
    # The Python script handles the actual server addition
    log_info "MCP servers will be added using the Python configuration script"
    log_success "MCP server setup completed"
}

# Setup workspace symlinks
setup_workspace() {
    log_info "Setting up workspace symlinks..."
    
    # Create workspace directory
    mkdir -p workspace
    
    # Setup repository symlinks (will be configured by user)
    cat > workspace/README.md << 'EOF'
# Workspace Directory

This directory contains symlinks to your actual repositories.

## Adding Repositories

To add a repository to your workspace:

```bash
ln -s /path/to/your/repo workspace/repo-name
```

## Recommended Structure

- `dbt/` - dbt project repository
- `dlthub/` - dlthub project repository
- `orchestration/` - Orchestra/Airflow DAGs
- `tableau/` - Tableau workbooks and scripts
- `docs/` - Documentation repository

## Customization

Edit `developer/workspace-config.sh` to automate your specific symlink setup.
EOF
    
    log_success "Workspace directory configured"
}

# Create environment template
create_env_template() {
    log_info "Creating environment template..."
    
    cat > .env.template << 'EOF'
# D&A Agent Hub Environment Configuration
# Copy this file to .env and fill in your actual values

# dbt Cloud Configuration
DBT_CLOUD_API_TOKEN=your_dbt_cloud_token_here
DBT_CLOUD_ACCOUNT_ID=your_account_id_here

# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_account.region
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_ROLE=your_role

# ClickUp Configuration
CLICKUP_CLIENT_ID=your_clickup_client_id
CLICKUP_CLIENT_SECRET=your_clickup_client_secret
CLICKUP_TEAM_ID=your_team_id

# Freshservice Configuration
FRESHSERVICE_APIKEY=your_freshservice_api_key
FRESHSERVICE_DOMAIN=your_domain.freshservice.com

# Tableau Configuration
TABLEAU_SERVER_URL=https://your-tableau-server.com
TABLEAU_USERNAME=your_username
TABLEAU_PASSWORD=your_password
TABLEAU_SITE_ID=your_site_id

# Orchestra Configuration
ORCHESTRA_API_URL=https://your-orchestra-instance.com
ORCHESTRA_API_TOKEN=your_orchestra_token

# Local Services
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_local_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password

OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
EOF
    
    log_success "Environment template created"
}

# Setup developer customization
setup_developer_customization() {
    log_info "Setting up developer customization framework..."
    
    # Create developer directory structure
    mkdir -p developer/{scripts,configs,knowledge}
    
    # Create customization template
    cat > developer/customize.sh << 'EOF'
#!/bin/bash

# Developer Customization Script
# Add your personal configuration here

# Example: Custom repository symlinks
setup_personal_repos() {
    echo "Setting up personal repository symlinks..."
    # ln -sf /path/to/your/dbt/project workspace/dbt
    # ln -sf /path/to/your/dlthub/project workspace/dlthub
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
    
    log_success "Developer customization framework created"
}

# Setup agents
setup_agents() {
    log_info "Setting up agents..."
    
    # Create user's Claude agents directory if it doesn't exist
    mkdir -p ~/.claude/agents
    
    # Copy all agents to user's Claude agents directory
    if [ -d ".claude/agents" ]; then
        cp .claude/agents/*.md ~/.claude/agents/ 2>/dev/null || true
        log_success "Agents copied to ~/.claude/agents"
    else
        log_warning "No agents found in .claude/agents directory"
    fi
}

# Create .gitignore
create_gitignore() {
    log_info "Creating .gitignore..."
    
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

# Workspace symlinks (will be recreated)
workspace/*
!workspace/README.md
EOF
    
    log_success ".gitignore created"
}

# Main setup function
main() {
    log_info "Starting D&A Agent Hub setup..."
    
    check_prerequisites
    setup_python_env
    install_mcp_servers
    setup_claude_config
    add_mcp_servers
    setup_workspace
    create_env_template
    setup_developer_customization
    create_gitignore
    
    log_success "D&A Agent Hub setup completed!"
    log_info ""
    log_info "Next steps:"
    log_info "1. Copy .env.template to .env and configure your credentials"
    log_info "2. Edit developer/customize.sh with your repository paths"
    log_info "3. Run ./developer/customize.sh"
    log_info "4. Restart Claude to load MCP servers: claude restart"
    log_info "5. Manage MCP servers: ./scripts/manage-mcp.sh [add|remove|list|status]"
    log_info "6. Run ./scripts/test-setup.sh to validate configuration"
    log_info ""
    log_info "For more information, see README.md"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi