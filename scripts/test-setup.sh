#!/bin/bash

# D&A Agent Hub Setup Validation Script
# Tests the complete setup to ensure everything is working

set -e

RED='\033[0;31m'
GREEN='\033[0;32m' 
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

test_prerequisites() {
    log_info "Testing prerequisites..."
    
    local missing=0
    
    for tool in python3 git claude jq; do
        if command -v $tool &> /dev/null; then
            log_success "$tool is available"
        else
            log_error "$tool is missing"
            ((missing++))
        fi
    done
    
    return $missing
}

test_directory_structure() {
    log_info "Testing directory structure..."
    
    local dirs=("knowledge" "repos" "developer" "scripts" ".claude")
    local missing=0
    
    for dir in "${dirs[@]}"; do
        if [ -d "$PROJECT_DIR/$dir" ]; then
            log_success "Directory exists: $dir"
        else
            log_error "Missing directory: $dir"
            ((missing++))
        fi
    done
    
    return $missing
}

test_agent_definitions() {
    log_info "Testing agent definitions..."
    
    local agents=("dbt-expert" "orchestra-expert" "tableau-expert" "snowflake-expert" "dlthub-expert" "business-context")
    local missing=0
    
    for agent in "${agents[@]}"; do
        if [ -f "$PROJECT_DIR/.claude/agents/$agent.md" ]; then
            log_success "Agent definition exists: $agent"
        else
            log_error "Missing agent definition: $agent"
            ((missing++))
        fi
    done
    
    return $missing
}

test_scripts() {
    log_info "Testing scripts..."
    
    local scripts=("setup.sh" "scripts/manage-workspace.sh" "scripts/manage-mcp.py")
    local missing=0
    
    for script in "${scripts[@]}"; do
        if [ -f "$PROJECT_DIR/$script" ] && [ -x "$PROJECT_DIR/$script" ]; then
            log_success "Script is executable: $script"
        else
            log_error "Script missing or not executable: $script"
            ((missing++))
        fi
    done
    
    return $missing
}

test_configuration() {
    log_info "Testing configuration..."
    
    local configs=("CLAUDE.md" ".env.template")
    local missing=0
    
    for config in "${configs[@]}"; do
        if [ -f "$PROJECT_DIR/$config" ]; then
            log_success "Configuration exists: $config"
        else
            log_error "Missing configuration: $config"
            ((missing++))
        fi
    done
    
    if [ -f "$PROJECT_DIR/.env" ]; then
        log_success "Environment file exists: .env"
    else
        log_warning "Environment file missing: .env (copy from .env.template)"
    fi
    
    return $missing
}

main() {
    log_info "Starting D&A Agent Hub setup validation..."
    echo
    
    local total_errors=0
    
    test_prerequisites || ((total_errors+=$?))
    echo
    test_directory_structure || ((total_errors+=$?))
    echo
    test_agent_definitions || ((total_errors+=$?))
    echo
    test_scripts || ((total_errors+=$?))
    echo
    test_configuration || ((total_errors+=$?))
    echo
    
    if [ $total_errors -eq 0 ]; then
        log_success "All tests passed! Setup is ready."
        echo
        log_info "Next steps:"
        log_info "1. Copy .env.template to .env and configure credentials"
        log_info "2. Edit developer/customize.sh with your repository paths"
        log_info "3. Run ./developer/customize.sh"
        log_info "4. Run python scripts/add-mcp-servers.py"
        log_info "5. Restart Claude: claude restart"
    else
        log_error "Found $total_errors issues. Please fix before proceeding."
        exit 1
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
