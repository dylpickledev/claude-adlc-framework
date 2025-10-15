#!/bin/bash
#
# Phase 5 Automation Orchestrator
#
# Runs automated pattern lifecycle workflows in proper sequence.
#
# Usage:
#     ./scripts/run-phase5-automation.sh daily      # Daily automation
#     ./scripts/run-phase5-automation.sh weekly     # Weekly automation
#     ./scripts/run-phase5-automation.sh monthly    # Monthly automation
#     ./scripts/run-phase5-automation.sh report     # Status report only
#

set -e  # Exit on error

# Activate venv for tiktoken
source projects/active/ai-memory-system-improvements/.venv/bin/activate

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Phase 5 automation workflows
run_daily_automation() {
    log "Starting daily Phase 5 automation..."

    # 1. Auto-promote qualified patterns
    log "Checking for promotion candidates..."
    python3 scripts/auto-promote-patterns.py --report || warning "Promotion check failed"

    # 2. Update lifecycle metrics
    log "Updating memory health metrics..."
    python3 scripts/check-memory-health.py || warning "Health check failed"

    log "Daily automation complete"
}

run_weekly_automation() {
    log "Starting weekly Phase 5 automation..."

    # 1. Run daily automation first
    run_daily_automation

    # 2. Duplicate detection
    log "Scanning for duplicate patterns..."
    python3 scripts/deduplicate-patterns.py || warning "Duplicate scan failed"

    # 3. Weekly summary report
    log "Generating weekly summary..."
    python3 scripts/check-memory-health.py --detailed || warning "Detailed report failed"

    log "Weekly automation complete"
}

run_monthly_automation() {
    log "Starting monthly Phase 5 automation..."

    # 1. Run weekly automation first
    run_weekly_automation

    # 2. Auto-archive stale patterns
    log "Checking for archival candidates..."
    python3 scripts/auto-archive-patterns.py --report || warning "Archival check failed"

    # 3. Monthly health report
    log "Generating monthly health report..."
    python3 scripts/check-memory-health.py --detailed --history || warning "Monthly report failed"

    log "Monthly automation complete"
}

run_status_report() {
    log "Generating Phase 5 status report..."

    echo ""
    echo "========================================================================"
    echo "PHASE 5 AUTOMATION STATUS"
    echo "========================================================================"

    # Memory health
    python3 scripts/check-memory-health.py

    # Promotion candidates
    echo ""
    python3 scripts/auto-promote-patterns.py --report

    # Archival candidates
    echo ""
    python3 scripts/auto-archive-patterns.py --report

    # Duplicate detection
    echo ""
    python3 scripts/deduplicate-patterns.py

    echo "========================================================================"
}

# Main execution
case "${1:-help}" in
    daily)
        run_daily_automation
        ;;
    weekly)
        run_weekly_automation
        ;;
    monthly)
        run_monthly_automation
        ;;
    report)
        run_status_report
        ;;
    *)
        echo "Usage: $0 {daily|weekly|monthly|report}"
        echo ""
        echo "  daily   - Run daily automation (promotion check, health update)"
        echo "  weekly  - Run weekly automation (daily + duplicates + summary)"
        echo "  monthly - Run monthly automation (weekly + archival + full report)"
        echo "  report  - Generate status report only"
        exit 1
        ;;
esac

exit 0
