#!/bin/bash
#
# Memory Consolidation Scheduler
#
# Automates the three-tier memory consolidation pipeline:
# - Daily: Move aging patterns to intermediate, summarize
# - Weekly: Promote high-value patterns to permanent
# - Monthly: Archive low-value patterns
#
# Usage:
#     ./scripts/schedule-consolidation.sh install    # Install cron jobs
#     ./scripts/schedule-consolidation.sh uninstall  # Remove cron jobs
#     ./scripts/schedule-consolidation.sh status     # Show current jobs
#     ./scripts/schedule-consolidation.sh run-daily  # Manual daily run
#     ./scripts/schedule-consolidation.sh run-weekly # Manual weekly run
#     ./scripts/schedule-consolidation.sh run-monthly # Manual monthly run
#

set -e

# Get absolute path to da-agent-hub
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DA_AGENT_HUB="$( cd "$SCRIPT_DIR/.." && pwd )"
LOG_DIR="$DA_AGENT_HUB/.claude/logs/consolidation"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/consolidation.log"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a "$LOG_DIR/consolidation.log" >&2
}

# Daily consolidation task
run_daily() {
    log "=== DAILY CONSOLIDATION STARTED ==="

    # Move patterns older than 30 days to intermediate
    log "Moving aging patterns to intermediate tier..."
    python3 "$DA_AGENT_HUB/scripts/migrate-to-tiers.py" \
        --source "$DA_AGENT_HUB/.claude/memory/recent" \
        >> "$LOG_DIR/daily-$(date +%Y%m%d).log" 2>&1

    # Summarize patterns in intermediate
    log "Summarizing intermediate patterns..."
    python3 "$DA_AGENT_HUB/scripts/summarize-patterns.py" \
        --dir "$DA_AGENT_HUB/.claude/memory/intermediate" \
        --fresh-only \
        >> "$LOG_DIR/daily-$(date +%Y%m%d).log" 2>&1

    log "=== DAILY CONSOLIDATION COMPLETED ==="
}

# Weekly consolidation task
run_weekly() {
    log "=== WEEKLY CONSOLIDATION STARTED ==="

    # Promote high-value patterns from intermediate to permanent
    log "Promoting high-value patterns..."
    python3 "$DA_AGENT_HUB/scripts/promote-patterns.py" \
        --source "$DA_AGENT_HUB/.claude/memory/intermediate" \
        --dest "$DA_AGENT_HUB/.claude/memory/patterns" \
        >> "$LOG_DIR/weekly-$(date +%Y%m%d).log" 2>&1

    log "=== WEEKLY CONSOLIDATION COMPLETED ==="
}

# Monthly consolidation task
run_monthly() {
    log "=== MONTHLY CONSOLIDATION STARTED ==="

    # Archive low-value patterns from intermediate
    log "Archiving low-value patterns..."
    python3 "$DA_AGENT_HUB/scripts/archive-patterns.py" \
        --source "$DA_AGENT_HUB/.claude/memory/intermediate" \
        --archive "$DA_AGENT_HUB/.claude/memory/archive" \
        --age 90 \
        >> "$LOG_DIR/monthly-$(date +%Y%m%d).log" 2>&1

    log "=== MONTHLY CONSOLIDATION COMPLETED ==="
}

# Install cron jobs
install_cron() {
    echo -e "${YELLOW}Installing memory consolidation cron jobs...${NC}"

    # Check if already installed
    if crontab -l 2>/dev/null | grep -q "memory-consolidation"; then
        echo -e "${YELLOW}Cron jobs already installed. Updating...${NC}"
        uninstall_cron
    fi

    # Create temporary cron file
    TEMP_CRON=$(mktemp)

    # Preserve existing crontab
    crontab -l 2>/dev/null > "$TEMP_CRON" || true

    # Add consolidation jobs
    cat >> "$TEMP_CRON" << EOF

# DA Agent Hub Memory Consolidation Pipeline
# Daily at 2 AM: Move aging patterns and summarize
0 2 * * * $SCRIPT_DIR/schedule-consolidation.sh run-daily >> $LOG_DIR/cron.log 2>&1 # memory-consolidation-daily

# Weekly on Sunday at 3 AM: Promote high-value patterns
0 3 * * 0 $SCRIPT_DIR/schedule-consolidation.sh run-weekly >> $LOG_DIR/cron.log 2>&1 # memory-consolidation-weekly

# Monthly on 1st at 4 AM: Archive low-value patterns
0 4 1 * * $SCRIPT_DIR/schedule-consolidation.sh run-monthly >> $LOG_DIR/cron.log 2>&1 # memory-consolidation-monthly
EOF

    # Install new crontab
    crontab "$TEMP_CRON"
    rm "$TEMP_CRON"

    echo -e "${GREEN}✅ Cron jobs installed successfully!${NC}"
    echo ""
    echo "Scheduled tasks:"
    echo "  Daily (2 AM):   Move aging patterns to intermediate, summarize"
    echo "  Weekly (3 AM):  Promote high-value patterns to permanent"
    echo "  Monthly (4 AM): Archive low-value patterns"
    echo ""
    echo "Logs: $LOG_DIR/"
}

# Uninstall cron jobs
uninstall_cron() {
    echo -e "${YELLOW}Uninstalling memory consolidation cron jobs...${NC}"

    # Remove consolidation jobs from crontab
    TEMP_CRON=$(mktemp)
    crontab -l 2>/dev/null | grep -v "memory-consolidation" > "$TEMP_CRON" || true
    crontab "$TEMP_CRON"
    rm "$TEMP_CRON"

    echo -e "${GREEN}✅ Cron jobs uninstalled${NC}"
}

# Show status
show_status() {
    echo -e "${GREEN}Memory Consolidation Status${NC}"
    echo "=============================="
    echo ""

    # Check if cron jobs installed
    if crontab -l 2>/dev/null | grep -q "memory-consolidation"; then
        echo -e "${GREEN}✅ Cron jobs: INSTALLED${NC}"
        echo ""
        echo "Scheduled tasks:"
        crontab -l 2>/dev/null | grep "memory-consolidation" | sed 's/ # memory-consolidation.*//'
    else
        echo -e "${RED}❌ Cron jobs: NOT INSTALLED${NC}"
        echo ""
        echo "Run './scripts/schedule-consolidation.sh install' to enable automated consolidation"
    fi

    echo ""
    echo "Recent logs:"
    ls -lt "$LOG_DIR" 2>/dev/null | head -n 6 || echo "No logs yet"

    echo ""
    echo "Memory usage:"
    if [ -d "$DA_AGENT_HUB/.claude/memory" ]; then
        echo "  Recent:       $(find $DA_AGENT_HUB/.claude/memory/recent -name '*.md' 2>/dev/null | wc -l | tr -d ' ') patterns"
        echo "  Intermediate: $(find $DA_AGENT_HUB/.claude/memory/intermediate -name '*.md' 2>/dev/null | wc -l | tr -d ' ') patterns"
        echo "  Patterns:     $(find $DA_AGENT_HUB/.claude/memory/patterns -name '*.md' 2>/dev/null | wc -l | tr -d ' ') patterns"
        echo "  Archive:      $(find $DA_AGENT_HUB/.claude/memory/archive -name '*.md' 2>/dev/null | wc -l | tr -d ' ') patterns"
    fi
}

# Main command dispatcher
case "${1:-}" in
    install)
        install_cron
        ;;
    uninstall)
        uninstall_cron
        ;;
    status)
        show_status
        ;;
    run-daily)
        run_daily
        ;;
    run-weekly)
        run_weekly
        ;;
    run-monthly)
        run_monthly
        ;;
    *)
        echo "Memory Consolidation Scheduler"
        echo ""
        echo "Usage:"
        echo "  $0 install      Install automated cron jobs"
        echo "  $0 uninstall    Remove automated cron jobs"
        echo "  $0 status       Show consolidation status"
        echo "  $0 run-daily    Run daily consolidation manually"
        echo "  $0 run-weekly   Run weekly consolidation manually"
        echo "  $0 run-monthly  Run monthly consolidation manually"
        echo ""
        echo "Automated schedule (when installed):"
        echo "  Daily (2 AM):   Move aging patterns to intermediate, summarize"
        echo "  Weekly (3 AM):  Promote high-value patterns to permanent"
        echo "  Monthly (4 AM): Archive low-value patterns"
        exit 1
        ;;
esac
