#!/bin/bash

# MCP Server Management Script
# Provides utilities for managing MCP servers in the D&A Agent Hub

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

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

# Show usage
show_usage() {
    echo "MCP Server Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  add         Add MCP servers from configuration"
    echo "  remove      Remove MCP servers"
    echo "  list        List configured MCP servers"
    echo "  status      Show server connection status"
    echo "  restart     Restart Claude to reload servers"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 add              # Add all servers from config"
    echo "  $0 remove clickup   # Remove specific server"
    echo "  $0 list             # List all servers"
    echo "  $0 status           # Check server status"
}

# Add MCP servers
add_servers() {
    log_info "Adding MCP servers from configuration..."
    
    if [ -f "$PROJECT_DIR/scripts/add-mcp-servers.py" ]; then
        cd "$PROJECT_DIR"
        python "$PROJECT_DIR/scripts/add-mcp-servers.py"
        log_success "MCP server addition completed"
    else
        log_error "MCP server configuration script not found"
        exit 1
    fi
}

# Remove MCP server
remove_server() {
    local server_name="$1"
    
    if [ -z "$server_name" ]; then
        log_error "Server name required for removal"
        echo "Usage: $0 remove <server_name>"
        exit 1
    fi
    
    log_info "Removing MCP server: $server_name"
    
    if claude mcp remove "$server_name" 2>/dev/null; then
        log_success "Removed MCP server: $server_name"
    else
        log_warning "Failed to remove MCP server '$server_name' (may not exist)"
    fi
}

# List MCP servers
list_servers() {
    log_info "Configured MCP servers:"
    claude mcp list
}

# Check server status
check_status() {
    log_info "Checking MCP server status..."
    
    # List servers and their status
    claude mcp list
    
    # Check for .env file
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        log_warning ".env file not found - servers may not connect properly"
        log_info "Copy .env.template to .env and configure your credentials"
    fi
    
    # Note about future servers
    log_info "Note: Additional servers (ClickUp, Tableau, Orchestra) are planned for future releases"
    log_info "See FUTURE-IMPROVEMENTS.md for roadmap and implementation status"
}

# Restart Claude
restart_claude() {
    log_info "Restarting Claude to reload MCP servers..."
    claude restart
    log_success "Claude restarted"
}

# Main function
main() {
    case "${1:-help}" in
        "add")
            add_servers
            ;;
        "remove")
            remove_server "$2"
            ;;
        "list")
            list_servers
            ;;
        "status")
            check_status
            ;;
        "restart")
            restart_claude
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            log_error "Unknown command: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi