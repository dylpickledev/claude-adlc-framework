#!/bin/bash

# Git Worktree Helper Script
# Simplifies worktree management for D&A Agent Hub

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Logging functions
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Help function
show_help() {
    echo -e "${BOLD}Git Worktree Helper${NC}"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  ${CYAN}add <name> <branch>${NC}     Create new worktree"
    echo "  ${CYAN}list${NC}                   Show all active worktrees"
    echo "  ${CYAN}remove <name>${NC}          Remove worktree and clean up"
    echo "  ${CYAN}clean${NC}                  Remove all worktrees and prune"
    echo "  ${CYAN}help${NC}                   Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 add hotfix hotfix/fix-login-bug"
    echo "  $0 add feature feature/new-dashboard"
    echo "  $0 remove hotfix"
    echo ""
}

# Add worktree
add_worktree() {
    local name="$1"
    local branch="$2"
    
    if [ -z "$name" ] || [ -z "$branch" ]; then
        log_error "Usage: $0 add <name> <branch>"
        echo "Example: $0 add hotfix hotfix/fix-login-bug"
        exit 1
    fi
    
    local worktree_path="worktrees/$name"
    
    # Check if worktree already exists
    if [ -d "$worktree_path" ]; then
        log_error "Worktree '$name' already exists at $worktree_path"
        exit 1
    fi
    
    # Create worktree
    log_info "Creating worktree '$name' with branch '$branch'..."
    if git worktree add "$worktree_path" -b "$branch" 2>/dev/null; then
        log_success "Created worktree at $worktree_path"
        echo ""
        echo "Next steps:"
        echo "  ${CYAN}cd $worktree_path${NC}     # Switch to worktree"
        echo "  # Make your changes"
        echo "  ${CYAN}$0 remove $name${NC}       # Clean up when done"
    else
        log_error "Failed to create worktree. Branch may already exist."
        exit 1
    fi
}

# List worktrees
list_worktrees() {
    echo -e "${BOLD}Active Worktrees:${NC}"
    git worktree list | while read path hash branch; do
        if [[ "$path" == *"/worktrees/"* ]]; then
            name=$(basename "$path")
            echo "  ${CYAN}$name${NC} -> $branch"
        elif [[ "$path" == *"da-agent-hub"* ]] && [[ "$path" != *"/worktrees/"* ]]; then
            echo "  ${CYAN}main${NC} -> $branch (primary repository)"
        fi
    done
}

# Remove worktree
remove_worktree() {
    local name="$1"
    
    if [ -z "$name" ]; then
        log_error "Usage: $0 remove <name>"
        echo "Example: $0 remove hotfix"
        exit 1
    fi
    
    local worktree_path="worktrees/$name"
    
    # Check if worktree exists
    if [ ! -d "$worktree_path" ]; then
        log_error "Worktree '$name' not found at $worktree_path"
        exit 1
    fi
    
    # Get branch name for cleanup
    local branch=$(cd "$worktree_path" && git branch --show-current 2>/dev/null || echo "")
    
    # Remove worktree
    log_info "Removing worktree '$name'..."
    if git worktree remove "$worktree_path" 2>/dev/null; then
        log_success "Removed worktree '$name'"
        
        # Ask about branch cleanup
        if [ -n "$branch" ]; then
            read -p "Delete branch '$branch'? [y/N]: " delete_branch
            if [[ $delete_branch =~ ^[Yy]$ ]]; then
                if git branch -D "$branch" 2>/dev/null; then
                    log_success "Deleted branch '$branch'"
                else
                    log_warning "Failed to delete branch '$branch'"
                fi
            fi
        fi
        
        # Prune stale references
        git worktree prune
    else
        log_error "Failed to remove worktree"
        exit 1
    fi
}

# Clean all worktrees
clean_worktrees() {
    echo -e "${BOLD}Cleaning All Worktrees...${NC}"
    
    # Confirm action
    read -p "This will remove ALL worktrees. Continue? [y/N]: " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        log_info "Cancelled"
        exit 0
    fi
    
    # Find and remove all worktrees
    local removed_count=0
    if [ -d "worktrees" ]; then
        for worktree_dir in worktrees/*/; do
            if [ -d "$worktree_dir" ]; then
                local name=$(basename "$worktree_dir")
                local branch=$(cd "$worktree_dir" && git branch --show-current 2>/dev/null || echo "")
                
                log_info "Removing worktree '$name'..."
                if git worktree remove "$worktree_dir" 2>/dev/null; then
                    ((removed_count++))
                    
                    # Clean up branch
                    if [ -n "$branch" ] && git show-ref --verify --quiet "refs/heads/$branch"; then
                        if git branch -D "$branch" 2>/dev/null; then
                            log_info "Deleted branch '$branch'"
                        fi
                    fi
                fi
            fi
        done
    fi
    
    # Prune stale references
    git worktree prune
    
    log_success "Cleaned $removed_count worktrees"
}

# Main script
main() {
    case "${1:-help}" in
        "add")
            add_worktree "$2" "$3"
            ;;
        "list"|"ls")
            list_worktrees
            ;;
        "remove"|"rm")
            remove_worktree "$2"
            ;;
        "clean")
            clean_worktrees
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"