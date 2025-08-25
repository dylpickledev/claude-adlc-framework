#!/bin/bash

# Workspace Repository Manager
# Manages symlinks to actual repositories for organized Claude Code navigation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$PROJECT_DIR/workspace"
CONFIG_FILE="$PROJECT_DIR/developer/workspace-config.json"

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Create default workspace configuration
create_default_config() {
    log_info "Creating default workspace configuration..."
    
    mkdir -p "$(dirname "$CONFIG_FILE")"
    
    cat > "$CONFIG_FILE" << 'EOF'
{
  "repositories": {
    "dbt": {
      "path": "/path/to/your/dbt/project",
      "description": "dbt transformation project",
      "enabled": false
    },
    "dlthub": {
      "path": "/path/to/your/dlthub/project", 
      "description": "dlthub data ingestion project",
      "enabled": false
    },
    "orchestration": {
      "path": "/path/to/your/orchestration/dags",
      "description": "Orchestra/Airflow DAG repository",
      "enabled": false
    },
    "tableau": {
      "path": "/path/to/your/tableau/workbooks",
      "description": "Tableau workbooks and scripts",
      "enabled": false
    },
    "docs": {
      "path": "/path/to/your/documentation",
      "description": "Technical documentation repository",
      "enabled": false
    }
  },
  "settings": {
    "check_git_status": true,
    "create_missing_dirs": true,
    "backup_broken_links": true
  }
}
EOF
    
    log_success "Default configuration created at $CONFIG_FILE"
    log_info "Edit this file to configure your repository paths"
}

# Load workspace configuration
load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        create_default_config
        return 1
    fi
    
    if ! command -v jq &> /dev/null; then
        log_error "jq is required for configuration parsing"
        log_info "Install with: brew install jq"
        return 1
    fi
    
    return 0
}

# Validate repository path
validate_repo_path() {
    local repo_path="$1"
    local repo_name="$2"
    
    if [ ! -d "$repo_path" ]; then
        log_warning "Repository path does not exist: $repo_path ($repo_name)"
        return 1
    fi
    
    if [ ! -d "$repo_path/.git" ]; then
        log_warning "Path is not a git repository: $repo_path ($repo_name)"
        return 1
    fi
    
    return 0
}

# Create symlink for repository
create_symlink() {
    local repo_name="$1"
    local repo_path="$2"
    local link_path="$WORKSPACE_DIR/$repo_name"
    
    # Remove existing symlink or directory
    if [ -L "$link_path" ]; then
        log_info "Removing existing symlink: $repo_name"
        rm "$link_path"
    elif [ -d "$link_path" ]; then
        log_warning "Directory exists at $link_path, backing up"
        mv "$link_path" "$link_path.backup.$(date +%s)"
    fi
    
    # Create new symlink
    if ln -s "$repo_path" "$link_path"; then
        log_success "Created symlink: $repo_name -> $repo_path"
        return 0
    else
        log_error "Failed to create symlink for $repo_name"
        return 1
    fi
}

# Setup workspace symlinks
setup_symlinks() {
    log_info "Setting up workspace symlinks..."
    
    if ! load_config; then
        log_error "Please configure your repositories in $CONFIG_FILE"
        return 1
    fi
    
    mkdir -p "$WORKSPACE_DIR"
    
    # Process each repository
    local repos=$(jq -r '.repositories | keys[]' "$CONFIG_FILE")
    
    for repo_name in $repos; do
        local enabled=$(jq -r ".repositories.\"$repo_name\".enabled" "$CONFIG_FILE")
        local repo_path=$(jq -r ".repositories.\"$repo_name\".path" "$CONFIG_FILE")
        local description=$(jq -r ".repositories.\"$repo_name\".description" "$CONFIG_FILE")
        
        if [ "$enabled" = "true" ]; then
            log_info "Processing repository: $repo_name ($description)"
            
            if validate_repo_path "$repo_path" "$repo_name"; then
                create_symlink "$repo_name" "$repo_path"
            fi
        else
            log_info "Skipping disabled repository: $repo_name"
        fi
    done
    
    log_success "Workspace setup completed"
}

# List current workspace status
list_workspace() {
    log_info "Current workspace status:"
    
    if [ ! -d "$WORKSPACE_DIR" ]; then
        log_warning "Workspace directory does not exist"
        return 1
    fi
    
    for item in "$WORKSPACE_DIR"/*; do
        if [ -L "$item" ]; then
            local name=$(basename "$item")
            local target=$(readlink "$item")
            if [ -d "$target" ]; then
                echo -e "  ${GREEN}✓${NC} $name -> $target"
            else
                echo -e "  ${RED}✗${NC} $name -> $target (broken)"
            fi
        elif [ -d "$item" ]; then
            local name=$(basename "$item")
            echo -e "  ${YELLOW}!${NC} $name (directory, not symlink)"
        fi
    done
}

# Clean broken symlinks
clean_workspace() {
    log_info "Cleaning broken symlinks..."
    
    local cleaned=0
    
    for item in "$WORKSPACE_DIR"/*; do
        if [ -L "$item" ] && [ ! -e "$item" ]; then
            local name=$(basename "$item")
            log_warning "Removing broken symlink: $name"
            rm "$item"
            ((cleaned++))
        fi
    done
    
    log_success "Cleaned $cleaned broken symlinks"
}

# Show repository status
show_status() {
    log_info "Repository status check..."
    
    for item in "$WORKSPACE_DIR"/*; do
        if [ -L "$item" ] && [ -d "$item" ]; then
            local name=$(basename "$item")
            local path=$(readlink "$item")
            
            echo -e "\n${BLUE}=== $name ===${NC}"
            echo "Path: $path"
            
            cd "$path"
            
            # Git status
            if [ -d ".git" ]; then
                local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
                local status=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
                echo "Branch: $branch"
                echo "Uncommitted changes: $status"
            else
                echo "Not a git repository"
            fi
            
            cd - > /dev/null
        fi
    done
}

# Main function
main() {
    case "${1:-setup}" in
        "setup")
            setup_symlinks
            ;;
        "list"|"ls")
            list_workspace
            ;;
        "clean")
            clean_workspace
            ;;
        "status")
            show_status
            ;;
        "config")
            if [ -f "$CONFIG_FILE" ]; then
                echo "Configuration file: $CONFIG_FILE"
                cat "$CONFIG_FILE"
            else
                log_error "Configuration file not found: $CONFIG_FILE"
                log_info "Run '$0 setup' to create default configuration"
            fi
            ;;
        "help"|"-h"|"--help")
            echo "Workspace Repository Manager"
            echo ""
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  setup     Create/update workspace symlinks (default)"
            echo "  list|ls   List current workspace status"
            echo "  clean     Remove broken symlinks"
            echo "  status    Show git status for all repositories"
            echo "  config    Show current configuration"
            echo "  help      Show this help message"
            echo ""
            echo "Configuration: $CONFIG_FILE"
            ;;
        *)
            log_error "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi