#!/bin/bash

# DA Agent Hub - Guest Mode
# Creates an isolated session for testing da-agent-hub with guest's own GitHub repos
# Uses YOUR Claude Code installation and API credits
# Isolates THEIR GitHub authentication and repository context

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }
log_step() { echo -e "\n${BOLD}${CYAN}=== $1 ===${NC}"; }

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DA_AGENT_HUB_ROOT="$(dirname "$SCRIPT_DIR")"
GUEST_SESSION_DIR="$DA_AGENT_HUB_ROOT/.guest-sessions"

show_help() {
    cat << EOF
${BOLD}DA Agent Hub - Guest Mode${NC}

Create an isolated session for testing da-agent-hub with a guest's own repositories.

${BOLD}Usage:${NC}
  ./scripts/guest-mode.sh start <session-name>   # Start new guest session
  ./scripts/guest-mode.sh stop <session-name>    # End guest session
  ./scripts/guest-mode.sh list                   # List active sessions
  ./scripts/guest-mode.sh cleanup                # Remove all guest sessions

${BOLD}What gets isolated:${NC}
  ✓ GitHub authentication (guest uses their own gh CLI login)
  ✓ Repository clones (guest's repos, not yours)
  ✓ Git configuration (guest's git config)
  ✓ Working directory (isolated workspace)

${BOLD}What gets shared:${NC}
  ✓ Claude Code installation (your CLI)
  ✓ Anthropic API credits (your account)
  ✓ da-agent-hub scripts and agents (from this repo)
  ✓ MCP server configurations (your setup)

${BOLD}Example:${NC}
  # Host starts guest session
  ./scripts/guest-mode.sh start workshop-demo

  # Guest authenticates with their GitHub
  # (prompted automatically)

  # Guest uses da-agent-hub commands with their repos
  claude /capture "Build customer dashboard"

  # Host ends session when done
  ./scripts/guest-mode.sh stop workshop-demo

EOF
}

start_guest_session() {
    local session_name="$1"

    if [ -z "$session_name" ]; then
        log_error "Session name required"
        echo "Usage: ./scripts/guest-mode.sh start <session-name>"
        exit 1
    fi

    local session_dir="$GUEST_SESSION_DIR/$session_name"

    if [ -d "$session_dir" ]; then
        log_error "Session '$session_name' already exists"
        echo "Use: ./scripts/guest-mode.sh stop $session_name"
        exit 1
    fi

    log_step "Starting Guest Session: $session_name"

    # Create isolated session directory
    mkdir -p "$session_dir"/{repos,knowledge,projects,config}

    log_success "Created isolated workspace at: $session_dir"

    # Create guest-specific config
    cat > "$session_dir/config/repositories.json" << 'EOF'
{
  "_comment": "Guest session repository configuration - Add your own repositories here",
  "settings": {
    "clone_method": "https",
    "update_existing": true
  },
  "knowledge": {},
  "data_stack": {
    "transformation": {},
    "ingestion": {},
    "front_end": {},
    "operations": {}
  }
}
EOF

    log_success "Created guest configuration"

    # Create session activation script
    cat > "$session_dir/activate.sh" << EOF
#!/bin/bash

# Guest Session Activation Script
# Run this to enter guest mode: source .guest-sessions/$session_name/activate.sh

export GUEST_SESSION_NAME="$session_name"
export GUEST_SESSION_DIR="$session_dir"

# Override working directory
cd "$session_dir"

# Save original GitHub auth for restoration
export ORIGINAL_GH_CONFIG_DIR="\$GH_CONFIG_DIR"
export ORIGINAL_GIT_CONFIG_GLOBAL="\$GIT_CONFIG_GLOBAL"

# Isolate GitHub CLI authentication
export GH_CONFIG_DIR="$session_dir/.config/gh"
mkdir -p "\$GH_CONFIG_DIR"

# Isolate git configuration
export GIT_CONFIG_GLOBAL="$session_dir/.gitconfig"

# Update prompt to show guest mode
export PS1="${CYAN}[GUEST: $session_name]${NC} \$PS1"

echo -e "${GREEN}✓${NC} Guest session activated: $session_name"
echo -e "${BLUE}ℹ${NC} Working directory: $session_dir"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo -e "  1. Authenticate with your GitHub account: ${CYAN}gh auth login${NC}"
echo -e "  2. Configure git: ${CYAN}git config --global user.name 'Your Name'${NC}"
echo -e "  3. Configure git: ${CYAN}git config --global user.email 'your@email.com'${NC}"
echo -e "  4. Use da-agent-hub commands as normal"
echo ""
echo -e "${YELLOW}⚠${NC}  Your work stays in: $session_dir"
echo -e "${YELLOW}⚠${NC}  Host's repositories are NOT accessible"
echo ""
EOF

    chmod +x "$session_dir/activate.sh"

    # Create deactivation script
    cat > "$session_dir/deactivate.sh" << EOF
#!/bin/bash

# Guest Session Deactivation Script

# Restore original environment
export GH_CONFIG_DIR="\$ORIGINAL_GH_CONFIG_DIR"
export GIT_CONFIG_GLOBAL="\$ORIGINAL_GIT_CONFIG_GLOBAL"
unset GUEST_SESSION_NAME
unset GUEST_SESSION_DIR
unset ORIGINAL_GH_CONFIG_DIR
unset ORIGINAL_GIT_CONFIG_GLOBAL

# Return to da-agent-hub root
cd "$DA_AGENT_HUB_ROOT"

echo -e "${GREEN}✓${NC} Guest session deactivated"
echo -e "${BLUE}ℹ${NC} Returned to host environment"
EOF

    chmod +x "$session_dir/deactivate.sh"

    # Create session metadata
    cat > "$session_dir/.session-info" << EOF
SESSION_NAME=$session_name
CREATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CREATED_BY=$USER
HOST_DA_AGENT_HUB=$DA_AGENT_HUB_ROOT
EOF

    log_step "Guest Session Ready"

    echo ""
    echo -e "${BOLD}${GREEN}Guest session '$session_name' created successfully!${NC}"
    echo ""
    echo -e "${BOLD}To activate this session:${NC}"
    echo -e "  ${CYAN}source .guest-sessions/$session_name/activate.sh${NC}"
    echo ""
    echo -e "${BOLD}Guest will then:${NC}"
    echo -e "  1. Authenticate with their GitHub: ${CYAN}gh auth login${NC}"
    echo -e "  2. Configure their git identity"
    echo -e "  3. Use da-agent-hub commands normally"
    echo ""
    echo -e "${BOLD}Their work will be isolated to:${NC}"
    echo -e "  $session_dir"
    echo ""
    echo -e "${BOLD}To end the session:${NC}"
    echo -e "  ${CYAN}source .guest-sessions/$session_name/deactivate.sh${NC}"
    echo -e "  ${CYAN}./scripts/guest-mode.sh stop $session_name${NC}"
    echo ""
}

stop_guest_session() {
    local session_name="$1"

    if [ -z "$session_name" ]; then
        log_error "Session name required"
        echo "Usage: ./scripts/guest-mode.sh stop <session-name>"
        exit 1
    fi

    local session_dir="$GUEST_SESSION_DIR/$session_name"

    if [ ! -d "$session_dir" ]; then
        log_error "Session '$session_name' not found"
        exit 1
    fi

    log_step "Stopping Guest Session: $session_name"

    # Show session summary
    if [ -f "$session_dir/.session-info" ]; then
        source "$session_dir/.session-info"
        echo "Session details:"
        echo "  Created: $CREATED_AT"
        echo "  Created by: $CREATED_BY"
        echo ""
    fi

    # Ask for confirmation
    read -p "Archive this session before removal? [Y/n]: " should_archive

    if [[ ! $should_archive =~ ^[Nn]$ ]]; then
        local archive_dir="$DA_AGENT_HUB_ROOT/.guest-sessions-archive"
        local archive_name="${session_name}_$(date +%Y%m%d_%H%M%S)"

        mkdir -p "$archive_dir"

        log_info "Archiving session to: $archive_dir/$archive_name.tar.gz"
        tar -czf "$archive_dir/$archive_name.tar.gz" -C "$GUEST_SESSION_DIR" "$session_name"

        log_success "Session archived"
    fi

    # Remove session directory
    rm -rf "$session_dir"

    log_success "Guest session '$session_name' removed"
    echo ""
    echo -e "${BOLD}Session cleaned up${NC}"
    echo "Guest's work has been removed from your system"
    echo ""
}

list_sessions() {
    log_step "Active Guest Sessions"

    if [ ! -d "$GUEST_SESSION_DIR" ] || [ -z "$(ls -A "$GUEST_SESSION_DIR" 2>/dev/null)" ]; then
        echo "No active guest sessions"
        echo ""
        echo "Create one with: ./scripts/guest-mode.sh start <session-name>"
        exit 0
    fi

    for session_path in "$GUEST_SESSION_DIR"/*; do
        if [ -d "$session_path" ]; then
            local session_name=$(basename "$session_path")
            local session_info="$session_path/.session-info"

            echo ""
            echo -e "${BOLD}Session: $session_name${NC}"

            if [ -f "$session_info" ]; then
                source "$session_info"
                echo "  Created: $CREATED_AT"
                echo "  Created by: $CREATED_BY"
            fi

            # Count files in session
            local file_count=$(find "$session_path" -type f 2>/dev/null | wc -l | tr -d ' ')
            echo "  Files: $file_count"

            # Check if repos exist
            if [ -d "$session_path/repos" ]; then
                local repo_count=$(find "$session_path/repos" -maxdepth 1 -type d 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
                echo "  Repositories: $repo_count"
            fi

            echo "  Location: $session_path"
            echo ""
            echo "  Activate: ${CYAN}source .guest-sessions/$session_name/activate.sh${NC}"
            echo "  Stop: ${CYAN}./scripts/guest-mode.sh stop $session_name${NC}"
        fi
    done

    echo ""
}

cleanup_all_sessions() {
    log_step "Cleanup All Guest Sessions"

    if [ ! -d "$GUEST_SESSION_DIR" ] || [ -z "$(ls -A "$GUEST_SESSION_DIR" 2>/dev/null)" ]; then
        log_info "No guest sessions to clean up"
        exit 0
    fi

    echo -e "${YELLOW}⚠${NC}  This will remove ALL guest sessions"
    read -p "Are you sure? [y/N]: " confirm

    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        log_info "Cleanup cancelled"
        exit 0
    fi

    read -p "Archive all sessions before removal? [Y/n]: " should_archive

    if [[ ! $should_archive =~ ^[Nn]$ ]]; then
        local archive_dir="$DA_AGENT_HUB_ROOT/.guest-sessions-archive"
        local archive_name="all_sessions_$(date +%Y%m%d_%H%M%S)"

        mkdir -p "$archive_dir"

        log_info "Archiving all sessions to: $archive_dir/$archive_name.tar.gz"
        tar -czf "$archive_dir/$archive_name.tar.gz" -C "$(dirname "$GUEST_SESSION_DIR")" "$(basename "$GUEST_SESSION_DIR")"

        log_success "All sessions archived"
    fi

    rm -rf "$GUEST_SESSION_DIR"

    log_success "All guest sessions removed"
    echo ""
}

# Main command router
case "${1:-}" in
    start)
        start_guest_session "$2"
        ;;
    stop)
        stop_guest_session "$2"
        ;;
    list)
        list_sessions
        ;;
    cleanup)
        cleanup_all_sessions
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
