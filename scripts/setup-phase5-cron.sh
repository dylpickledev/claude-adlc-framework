#!/bin/bash
#
# Phase 5 Automation Cron Setup
#
# Sets up cron jobs for automated pattern lifecycle management:
# - Daily: Promotion scan + health updates (5:00 AM)
# - Weekly: Duplicate detection + summaries (Sunday 6:00 AM)
# - Monthly: Archival scan + comprehensive reports (1st day, 7:00 AM)
#
# Usage:
#     ./scripts/setup-phase5-cron.sh install    # Install cron jobs
#     ./scripts/setup-phase5-cron.sh uninstall  # Remove cron jobs
#     ./scripts/setup-phase5-cron.sh status     # Show current cron jobs
#

set -e

# Get absolute path to da-agent-hub
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DA_AGENT_HUB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Log directory
LOG_DIR="$DA_AGENT_HUB_DIR/.claude/cache/phase5-logs"
mkdir -p "$LOG_DIR"

# Cron job definitions
DAILY_CRON="0 5 * * * cd $DA_AGENT_HUB_DIR && ./scripts/run-phase5-automation.sh daily >> $LOG_DIR/daily.log 2>&1"
WEEKLY_CRON="0 6 * * 0 cd $DA_AGENT_HUB_DIR && ./scripts/run-phase5-automation.sh weekly >> $LOG_DIR/weekly.log 2>&1"
MONTHLY_CRON="0 7 1 * * cd $DA_AGENT_HUB_DIR && ./scripts/run-phase5-automation.sh monthly >> $LOG_DIR/monthly.log 2>&1"

# Cron comment marker for easy identification
CRON_MARKER="# DA Agent Hub - Phase 5 Pattern Lifecycle Automation"

install_cron_jobs() {
    echo "Installing Phase 5 automation cron jobs..."

    # Check if cron jobs already exist
    if crontab -l 2>/dev/null | grep -q "$CRON_MARKER"; then
        echo "⚠️  Phase 5 cron jobs already installed. Run 'uninstall' first to update."
        exit 1
    fi

    # Get current crontab (if exists)
    CURRENT_CRONTAB=$(crontab -l 2>/dev/null || echo "")

    # Create new crontab with Phase 5 jobs
    {
        echo "$CURRENT_CRONTAB"
        echo ""
        echo "$CRON_MARKER"
        echo "# Daily: Promotion scan + health updates (5:00 AM)"
        echo "$DAILY_CRON"
        echo ""
        echo "# Weekly: Duplicate detection + summaries (Sunday 6:00 AM)"
        echo "$WEEKLY_CRON"
        echo ""
        echo "# Monthly: Archival scan + reports (1st day, 7:00 AM)"
        echo "$MONTHLY_CRON"
        echo ""
    } | crontab -

    echo "✅ Phase 5 cron jobs installed successfully!"
    echo ""
    echo "Schedules:"
    echo "  Daily   : 5:00 AM - Promotion scan + health updates"
    echo "  Weekly  : Sunday 6:00 AM - Duplicate detection + summaries"
    echo "  Monthly : 1st day 7:00 AM - Archival scan + comprehensive reports"
    echo ""
    echo "Logs: $LOG_DIR"
    echo ""
    echo "Manual execution:"
    echo "  cd $DA_AGENT_HUB_DIR"
    echo "  ./scripts/run-phase5-automation.sh daily|weekly|monthly|report"
}

uninstall_cron_jobs() {
    echo "Uninstalling Phase 5 automation cron jobs..."

    # Check if cron jobs exist
    if ! crontab -l 2>/dev/null | grep -q "$CRON_MARKER"; then
        echo "⚠️  No Phase 5 cron jobs found to uninstall."
        exit 1
    fi

    # Remove Phase 5 cron jobs (everything from marker until next non-empty non-comment line)
    crontab -l 2>/dev/null | awk "
        BEGIN { skip=0 }
        /$CRON_MARKER/ { skip=1; next }
        /^$/ && skip { next }
        /^#/ && skip { next }
        /^[^#]/ { skip=0 }
        !skip { print }
    " | crontab -

    echo "✅ Phase 5 cron jobs uninstalled successfully!"
}

show_status() {
    echo "Phase 5 Automation Cron Status"
    echo "========================================================================"
    echo ""

    if crontab -l 2>/dev/null | grep -q "$CRON_MARKER"; then
        echo "✅ Phase 5 cron jobs INSTALLED"
        echo ""
        echo "Cron jobs:"
        crontab -l 2>/dev/null | awk "/$CRON_MARKER/,/^$/{print}"
        echo ""
        echo "Logs directory: $LOG_DIR"
        echo ""

        # Show recent log activity
        if [ -d "$LOG_DIR" ]; then
            echo "Recent activity:"
            ls -lht "$LOG_DIR" 2>/dev/null | head -10 || echo "  No logs yet"
        fi
    else
        echo "❌ Phase 5 cron jobs NOT installed"
        echo ""
        echo "To install: ./scripts/setup-phase5-cron.sh install"
    fi

    echo ""
    echo "========================================================================"
}

# Main execution
case "${1:-status}" in
    install)
        install_cron_jobs
        ;;
    uninstall)
        uninstall_cron_jobs
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: $0 {install|uninstall|status}"
        echo ""
        echo "  install   - Install Phase 5 automation cron jobs"
        echo "  uninstall - Remove Phase 5 automation cron jobs"
        echo "  status    - Show current installation status"
        exit 1
        ;;
esac

exit 0
