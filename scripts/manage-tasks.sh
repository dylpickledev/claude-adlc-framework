#!/bin/bash

# Task Management Script for D&A Agent Hub
# Manages agent task files: archive, purge, and compact operations

TASKS_DIR=".claude/tasks"
ARCHIVE_DIR="$TASKS_DIR/archive"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Ensure we're in the right directory
if [ ! -d "$TASKS_DIR" ]; then
    echo -e "${RED}Error: $TASKS_DIR not found. Are you in the da-agent-hub directory?${NC}"
    exit 1
fi

# Create archive directory if it doesn't exist
mkdir -p "$ARCHIVE_DIR"

show_usage() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  status         Show current task file status"
    echo "  archive        Archive all current task files with timestamp"
    echo "  purge          Delete all current task files (keep current-task.md)"
    echo "  clean-archive  Remove archived files older than 30 days"
    echo "  compact        Archive current tasks and clean old archives"
    echo ""
    echo "Options:"
    echo "  --dry-run      Show what would be done without making changes"
    echo "  --force        Skip confirmation prompts"
    echo ""
    echo "Examples:"
    echo "  $0 status                # Show task file status"
    echo "  $0 archive              # Archive current task files"
    echo "  $0 purge --dry-run      # Preview what would be purged"
    echo "  $0 compact --force      # Archive and clean without prompts"
}

show_status() {
    echo -e "${BLUE}=== Task File Status ===${NC}"
    echo ""
    
    # Count files in each agent directory
    for agent_dir in "$TASKS_DIR"/*/; do
        if [ -d "$agent_dir" ] && [ "$(basename "$agent_dir")" != "archive" ]; then
            agent=$(basename "$agent_dir")
            file_count=$(find "$agent_dir" -name "*.md" 2>/dev/null | wc -l)
            if [ "$file_count" -gt 0 ]; then
                echo -e "${GREEN}$agent:${NC} $file_count files"
                find "$agent_dir" -name "*.md" -exec basename {} \; | sed 's/^/  - /'
            fi
        fi
    done
    
    # Show current-task.md status
    if [ -f "$TASKS_DIR/current-task.md" ]; then
        echo -e "${GREEN}current-task.md:${NC} present"
    else
        echo -e "${YELLOW}current-task.md:${NC} missing"
    fi
    
    # Show archive status
    archive_count=$(find "$ARCHIVE_DIR" -name "*.tar.gz" 2>/dev/null | wc -l)
    echo -e "${BLUE}Archives:${NC} $archive_count archived task sets"
    
    echo ""
}

archive_tasks() {
    local dry_run=$1
    local timestamp=$(date +"%Y%m%d-%H%M%S")
    local archive_name="tasks-$timestamp.tar.gz"
    local archive_path="$ARCHIVE_DIR/$archive_name"
    
    echo -e "${BLUE}=== Archiving Task Files ===${NC}"
    
    # Find all agent task files
    local files_to_archive=()
    for agent_dir in "$TASKS_DIR"/*/; do
        if [ -d "$agent_dir" ] && [ "$(basename "$agent_dir")" != "archive" ]; then
            while IFS= read -r -d '' file; do
                files_to_archive+=("$file")
            done < <(find "$agent_dir" -name "*.md" -print0 2>/dev/null)
        fi
    done
    
    if [ ${#files_to_archive[@]} -eq 0 ]; then
        echo -e "${YELLOW}No agent task files to archive.${NC}"
        return 0
    fi
    
    echo "Will archive ${#files_to_archive[@]} files to: $archive_name"
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY RUN] Would archive:${NC}"
        printf '%s\n' "${files_to_archive[@]}"
        return 0
    fi
    
    # Create archive
    tar -czf "$archive_path" "${files_to_archive[@]}" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Archived to $archive_name${NC}"
        
        # Remove original files after successful archive
        for file in "${files_to_archive[@]}"; do
            rm -f "$file"
        done
        echo -e "${GREEN}✓ Removed original task files${NC}"
    else
        echo -e "${RED}✗ Failed to create archive${NC}"
        return 1
    fi
}

purge_tasks() {
    local dry_run=$1
    local force=$2
    
    echo -e "${BLUE}=== Purging Task Files ===${NC}"
    
    # Find all agent task files
    local files_to_purge=()
    for agent_dir in "$TASKS_DIR"/*/; do
        if [ -d "$agent_dir" ] && [ "$(basename "$agent_dir")" != "archive" ]; then
            while IFS= read -r -d '' file; do
                files_to_purge+=("$file")
            done < <(find "$agent_dir" -name "*.md" -print0 2>/dev/null)
        fi
    done
    
    if [ ${#files_to_purge[@]} -eq 0 ]; then
        echo -e "${YELLOW}No agent task files to purge.${NC}"
        return 0
    fi
    
    echo -e "${RED}Will permanently delete ${#files_to_purge[@]} task files${NC}"
    echo -e "${YELLOW}Note: current-task.md will be preserved${NC}"
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY RUN] Would delete:${NC}"
        printf '%s\n' "${files_to_purge[@]}"
        return 0
    fi
    
    if [ "$force" != "true" ]; then
        echo -e "${RED}This will permanently delete all agent task files. Continue? (y/N)${NC}"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            echo "Cancelled."
            return 0
        fi
    fi
    
    # Delete files
    for file in "${files_to_purge[@]}"; do
        rm -f "$file"
    done
    
    echo -e "${GREEN}✓ Purged ${#files_to_purge[@]} task files${NC}"
}

clean_archive() {
    local dry_run=$1
    local force=$2
    
    echo -e "${BLUE}=== Cleaning Old Archives ===${NC}"
    
    # Find archives older than 30 days
    local old_archives=()
    while IFS= read -r -d '' file; do
        old_archives+=("$file")
    done < <(find "$ARCHIVE_DIR" -name "*.tar.gz" -mtime +30 -print0 2>/dev/null)
    
    if [ ${#old_archives[@]} -eq 0 ]; then
        echo -e "${YELLOW}No old archives to clean (>30 days).${NC}"
        return 0
    fi
    
    echo "Found ${#old_archives[@]} archives older than 30 days"
    
    if [ "$dry_run" = "true" ]; then
        echo -e "${YELLOW}[DRY RUN] Would delete:${NC}"
        printf '%s\n' "${old_archives[@]}"
        return 0
    fi
    
    if [ "$force" != "true" ]; then
        echo -e "${YELLOW}Delete old archive files? (y/N)${NC}"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            echo "Cancelled."
            return 0
        fi
    fi
    
    # Delete old archives
    for file in "${old_archives[@]}"; do
        rm -f "$file"
    done
    
    echo -e "${GREEN}✓ Cleaned ${#old_archives[@]} old archives${NC}"
}

compact_tasks() {
    local dry_run=$1
    local force=$2
    
    echo -e "${BLUE}=== Compacting Tasks ===${NC}"
    echo "This will archive current tasks and clean old archives"
    echo ""
    
    # Archive current tasks
    archive_tasks "$dry_run"
    
    # Clean old archives
    clean_archive "$dry_run" "$force"
    
    echo -e "${GREEN}✓ Task compaction complete${NC}"
}

# Main script logic
DRY_RUN=false
FORCE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        status)
            show_status
            exit 0
            ;;
        archive)
            archive_tasks "$DRY_RUN"
            exit $?
            ;;
        purge)
            purge_tasks "$DRY_RUN" "$FORCE"
            exit $?
            ;;
        clean-archive)
            clean_archive "$DRY_RUN" "$FORCE"
            exit $?
            ;;
        compact)
            compact_tasks "$DRY_RUN" "$FORCE"
            exit $?
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown command: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
done

# If no command provided, show status
show_status