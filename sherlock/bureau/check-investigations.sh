#!/bin/bash

# Sherlock Holmes Investigation Bureau - Investigation Monitor
# Watson-style progress checking across all active cases

SHERLOCK_DIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
CASES_DIR="$SHERLOCK_DIR/cases"
EVIDENCE_DIR="$SHERLOCK_DIR/evidence"

# Victorian detective styling
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

print_header() {
    echo -e "${PURPLE}"
    echo "🔍 SHERLOCK HOLMES INVESTIGATION BUREAU 🔍"
    echo "═══════════════════════════════════════════"
    echo "      Investigation Monitor (Watson)"
    echo "═══════════════════════════════════════════"
    echo -e "${NC}"
}

get_case_status() {
    local case_dir=$1
    local evidence_file="$case_dir/evidence-report.md"
    
    if [ ! -f "$evidence_file" ]; then
        echo "📋 Case Filed"
        return
    fi
    
    # Check evidence report for status indicators
    if grep -q "Investigation Complete" "$evidence_file" && grep -q "- \[x\] Investigation Complete" "$evidence_file"; then
        if grep -q "- \[x\] Ready for Implementation" "$evidence_file"; then
            echo "✅ Ready for Action"
        else
            echo "🔍 Evidence Compiled"
        fi
    elif grep -q "- \[x\] Requires Additional Evidence" "$evidence_file"; then
        echo "🔄 Needs More Evidence"
    elif grep -q "- \[x\] Blocked by Dependencies" "$evidence_file"; then
        echo "⏸️  Blocked"
    elif [ -s "$evidence_file" ]; then
        # Evidence file exists and has content
        local word_count=$(wc -w < "$evidence_file")
        if [ "$word_count" -gt 100 ]; then
            echo "🔄 Investigation Active"
        else
            echo "🚀 Detective Deployed"
        fi
    else
        echo "📋 Case Filed"
    fi
}

get_priority_icon() {
    local priority=$1
    case $priority in
        "HIGH")     echo "🔴" ;;
        "MEDIUM")   echo "🟡" ;;
        "LOW")      echo "🟢" ;;
        *)          echo "⚪" ;;
    esac
}

get_case_summary() {
    local case_dir=$1
    local brief_file="$case_dir/case-brief.md"
    
    if [ -f "$brief_file" ]; then
        grep -A 1 "## Case Description" "$brief_file" | tail -1
    else
        echo "Case details unavailable"
    fi
}

show_detailed_status() {
    local case_dir=$1
    local case_name=$(basename "$case_dir")
    local case_title=$(echo "$case_name" | sed 's/-/ /g' | sed 's/\b\w/\U&/g')
    
    local brief_file="$case_dir/case-brief.md"
    local evidence_file="$case_dir/evidence-report.md"
    
    echo -e "${BOLD}${BLUE}═══ $case_title ═══${NC}"
    
    # Priority and Issues
    if [ -f "$brief_file" ]; then
        local priority=$(grep "Case Classification:" "$brief_file" | cut -d' ' -f3)
        local issues=$(grep "Assigned Issues:" "$brief_file" | cut -d' ' -f3-)
        echo -e "${CYAN}Priority:${NC} $(get_priority_icon "$priority") $priority"
        echo -e "${CYAN}Issues:${NC} $issues"
    fi
    
    # Status
    local status=$(get_case_status "$case_dir")
    echo -e "${CYAN}Status:${NC} $status"
    
    # Progress indicators
    if [ -f "$evidence_file" ]; then
        local last_update=$(stat -c %y "$evidence_file" 2>/dev/null || stat -f %m "$evidence_file" 2>/dev/null | xargs -I{} date -r {})
        echo -e "${CYAN}Last Update:${NC} $last_update"
        
        # Evidence summary
        if [ -s "$evidence_file" ]; then
            echo -e "${CYAN}Evidence:${NC}"
            local summary=$(grep -A 3 "## Investigation Summary" "$evidence_file" | tail -3 | head -1)
            if [ -n "$summary" ] && [ "$summary" != "*[Provide overview of investigation conducted]*" ]; then
                echo -e "  📝 $summary"
            else
                echo -e "  🔄 Investigation in progress..."
            fi
        fi
    else
        echo -e "${CYAN}Evidence:${NC} 📋 No evidence file yet"
    fi
    
    echo ""
}

show_coordination_status() {
    local coord_file="$CASES_DIR/case-coordination.md"
    
    if [ -f "$coord_file" ]; then
        echo -e "${BOLD}${PURPLE}📋 COORDINATION NOTES${NC}"
        echo ""
        
        # Extract and display investigation notes
        if grep -q "## Investigation Notes" "$coord_file"; then
            sed -n '/## Investigation Notes/,/##/p' "$coord_file" | grep -v "^##" | grep -v "^\*Bureau coordination" | while read -r line; do
                if [ -n "$line" ]; then
                    echo -e "  📝 $line"
                fi
            done
        fi
        
        # Show cross-case dependencies
        if grep -q "## Cross-Case Dependencies" "$coord_file"; then
            echo -e "${CYAN}🔗 Dependencies:${NC}"
            sed -n '/## Cross-Case Dependencies/,/^$/p' "$coord_file" | grep "^-" | while read -r line; do
                echo -e "  $line"
            done
        fi
        echo ""
    fi
}

monitor_investigations() {
    local mode=$1
    
    print_header
    
    if [ ! -d "$CASES_DIR" ]; then
        echo -e "${RED}❌ No cases directory found${NC}"
        echo -e "${YELLOW}   Run: ./sherlock/bureau/dispatch-cases.sh first${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}📊 Current Investigation Status${NC}"
    echo -e "${CYAN}Report Time: $(date)${NC}"
    echo ""
    
    # Count cases by status and priority
    local total_cases=0
    local active_cases=0
    local completed_cases=0
    local blocked_cases=0
    local high_priority=0
    local medium_priority=0
    local low_priority=0
    
    # Quick overview table
    if [ "$mode" != "detailed" ]; then
        echo -e "${BOLD}Case Name${NC} | ${BOLD}Priority${NC} | ${BOLD}Status${NC}"
        echo "────────────────────────────────────────────────────────"
    fi
    
    for case_dir in "$CASES_DIR"/*; do
        if [ -d "$case_dir" ] && [ "$(basename "$case_dir")" != "archive" ]; then
            local case_file=$(basename "$case_dir")
            
            # Skip coordination file
            if [ "$case_file" = "case-coordination.md" ]; then
                continue
            fi
            
            ((total_cases++))
            
            local case_title=$(echo "$case_file" | sed 's/-/ /g' | sed 's/\b\w/\U&/g')
            local status=$(get_case_status "$case_dir")
            
            # Get priority
            local priority="MEDIUM"
            local brief_file="$case_dir/case-brief.md"
            if [ -f "$brief_file" ]; then
                priority=$(grep "Case Classification:" "$brief_file" | cut -d' ' -f3)
            fi
            
            # Count by priority
            case $priority in
                "HIGH") ((high_priority++)) ;;
                "MEDIUM") ((medium_priority++)) ;;
                "LOW") ((low_priority++)) ;;
            esac
            
            # Count by status
            case $status in
                *"Active"*|*"Deployed"*) ((active_cases++)) ;;
                *"Ready"*|*"Compiled"*) ((completed_cases++)) ;;
                *"Blocked"*) ((blocked_cases++)) ;;
            esac
            
            if [ "$mode" = "detailed" ]; then
                show_detailed_status "$case_dir"
            else
                printf "%-25s | %s %-6s | %s\n" "$case_title" "$(get_priority_icon "$priority")" "$priority" "$status"
            fi
        fi
    done
    
    if [ "$mode" != "detailed" ]; then
        echo ""
    fi
    
    # Summary statistics
    echo -e "${BOLD}${GREEN}📈 BUREAU STATISTICS${NC}"
    echo ""
    echo -e "${CYAN}📊 Case Status:${NC}"
    echo -e "   Total Cases: $total_cases"
    echo -e "   🔄 Active Investigations: $active_cases"
    echo -e "   ✅ Ready for Action: $completed_cases" 
    echo -e "   ⏸️  Blocked Cases: $blocked_cases"
    echo ""
    echo -e "${CYAN}🎯 Priority Breakdown:${NC}"
    echo -e "   🔴 High Priority: $high_priority cases"
    echo -e "   🟡 Medium Priority: $medium_priority cases"
    echo -e "   🟢 Low Priority: $low_priority cases"
    echo ""
    
    # Show coordination status
    show_coordination_status
    
    # Next actions
    echo -e "${YELLOW}🚀 Recommended Actions:${NC}"
    if [ $completed_cases -gt 0 ]; then
        echo -e "   📋 Review completed investigations for implementation"
    fi
    if [ $blocked_cases -gt 0 ]; then
        echo -e "   🔓 Address blocked case dependencies"
    fi
    if [ $active_cases -gt 0 ]; then
        echo -e "   ⏰ Monitor active investigations progress"
    fi
    if [ $completed_cases -ge 3 ]; then
        echo -e "   📄 Compile evidence: ${BLUE}./sherlock/bureau/compile-evidence.sh${NC}"
    fi
    echo ""
}

# Script execution
case "$1" in
    --help|-h)
        echo "Sherlock Holmes Investigation Bureau - Investigation Monitor"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h      Show this help message"
        echo "  --detailed, -d  Show detailed case information"
        echo "  --watch, -w     Continuous monitoring (refresh every 30s)"
        echo ""
        echo "Description:"
        echo "  Monitor progress across all active investigation cases."
        echo "  Shows case status, detective assignments, and evidence compilation."
        echo "  Like having Watson provide investigation updates."
        echo ""
        exit 0
        ;;
    --detailed|-d)
        monitor_investigations "detailed"
        ;;
    --watch|-w)
        echo -e "${PURPLE}🔍 Continuous Investigation Monitor Active${NC}"
        echo -e "${CYAN}Press Ctrl+C to exit${NC}"
        echo ""
        while true; do
            clear
            monitor_investigations
            echo -e "${CYAN}Refreshing in 30 seconds...${NC}"
            sleep 30
        done
        ;;
    *)
        monitor_investigations
        ;;
esac