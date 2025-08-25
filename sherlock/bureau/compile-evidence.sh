#!/bin/bash

# Sherlock Holmes Investigation Bureau - Evidence Compiler
# Aggregates findings from all detective investigations into actionable reports

SHERLOCK_DIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
CASES_DIR="$SHERLOCK_DIR/cases"
EVIDENCE_DIR="$SHERLOCK_DIR/evidence"
WORKSPACE_DIR="workspace"

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
    echo "        Evidence Compilation Division"
    echo "═══════════════════════════════════════════"
    echo -e "${NC}"
}

ensure_directories() {
    mkdir -p "$EVIDENCE_DIR"
    mkdir -p "$WORKSPACE_DIR"
}

get_case_priority() {
    local case_dir=$1
    local brief_file="$case_dir/case-brief.md"
    
    if [ -f "$brief_file" ]; then
        grep "Case Classification:" "$brief_file" | cut -d' ' -f3
    else
        echo "MEDIUM"
    fi
}

get_case_issues() {
    local case_dir=$1
    local brief_file="$case_dir/case-brief.md"
    
    if [ -f "$brief_file" ]; then
        grep "Assigned Issues:" "$brief_file" | cut -d' ' -f3-
    else
        echo "Unknown"
    fi
}

extract_evidence_summary() {
    local evidence_file=$1
    
    if [ ! -f "$evidence_file" ] || [ ! -s "$evidence_file" ]; then
        echo "🔄 Investigation pending"
        return
    fi
    
    # Extract investigation summary
    local summary=$(sed -n '/## Investigation Summary/,/##/p' "$evidence_file" | grep -v "^##" | grep -v "^\*\[" | head -3 | xargs)
    if [ -n "$summary" ]; then
        echo "$summary"
    else
        echo "📝 Evidence being compiled"
    fi
}

extract_recommended_actions() {
    local evidence_file=$1
    
    if [ ! -f "$evidence_file" ] || [ ! -s "$evidence_file" ]; then
        return
    fi
    
    # Extract recommended actions
    sed -n '/## Recommended Actions/,/##/p' "$evidence_file" | grep -v "^##" | grep -v "^\*\[" | while read -r line; do
        if [ -n "$line" ]; then
            echo "  $line"
        fi
    done
}

check_case_readiness() {
    local evidence_file=$1
    
    if [ ! -f "$evidence_file" ]; then
        echo "not-ready"
        return
    fi
    
    if grep -q "- \[x\] Investigation Complete" "$evidence_file" && 
       grep -q "- \[x\] Ready for Implementation" "$evidence_file"; then
        echo "ready"
    elif grep -q "- \[x\] Investigation Complete" "$evidence_file"; then
        echo "complete"
    elif grep -q "- \[x\] Blocked by Dependencies" "$evidence_file"; then
        echo "blocked"
    elif [ -s "$evidence_file" ]; then
        echo "in-progress"
    else
        echo "not-started"
    fi
}

compile_investigation_summary() {
    local output_file="$EVIDENCE_DIR/investigation-summary.md"
    
    echo -e "${BLUE}📋 Compiling investigation summary...${NC}"
    
    cat > "$output_file" << EOF
# SHERLOCK HOLMES INVESTIGATION BUREAU
## Comprehensive Investigation Summary

**Report Generated:** $(date)  
**Bureau Chief:** Inspector Dylan  

---

EOF

    # Summary statistics
    local total_cases=0
    local ready_cases=0
    local complete_cases=0
    local blocked_cases=0
    local in_progress_cases=0
    
    cat >> "$output_file" << EOF
## Executive Summary

EOF

    # Process each case
    for case_dir in "$CASES_DIR"/*; do
        if [ -d "$case_dir" ] && [ "$(basename "$case_dir")" != "archive" ]; then
            local case_file=$(basename "$case_dir")
            
            # Skip coordination file
            if [ "$case_file" = "case-coordination.md" ]; then
                continue
            fi
            
            ((total_cases++))
            
            local case_title=$(echo "$case_file" | sed 's/-/ /g' | sed 's/\b\w/\U&/g')
            local evidence_file="$case_dir/evidence-report.md"
            local readiness=$(check_case_readiness "$evidence_file")
            
            case $readiness in
                "ready") ((ready_cases++)) ;;
                "complete") ((complete_cases++)) ;;
                "blocked") ((blocked_cases++)) ;;
                "in-progress") ((in_progress_cases++)) ;;
            esac
        fi
    done
    
    cat >> "$output_file" << EOF
### Bureau Statistics
- **Total Cases:** $total_cases investigations launched
- **Ready for Implementation:** $ready_cases cases
- **Investigation Complete:** $complete_cases cases  
- **In Progress:** $in_progress_cases active investigations
- **Blocked:** $blocked_cases cases awaiting dependencies

---

## Detailed Case Reports

EOF

    # Detailed case information
    for case_dir in "$CASES_DIR"/*; do
        if [ -d "$case_dir" ] && [ "$(basename "$case_dir")" != "archive" ]; then
            local case_file=$(basename "$case_dir")
            
            # Skip coordination file
            if [ "$case_file" = "case-coordination.md" ]; then
                continue
            fi
            
            local case_title=$(echo "$case_file" | sed 's/-/ /g' | sed 's/\b\w/\U&/g')
            local priority=$(get_case_priority "$case_dir")
            local issues=$(get_case_issues "$case_dir")
            local evidence_file="$case_dir/evidence-report.md"
            local readiness=$(check_case_readiness "$evidence_file")
            local summary=$(extract_evidence_summary "$evidence_file")
            
            # Priority icon
            local priority_icon="⚪"
            case $priority in
                "HIGH") priority_icon="🔴" ;;
                "MEDIUM") priority_icon="🟡" ;;
                "LOW") priority_icon="🟢" ;;
            esac
            
            # Status icon
            local status_icon="📋"
            case $readiness in
                "ready") status_icon="✅" ;;
                "complete") status_icon="🔍" ;;
                "blocked") status_icon="⏸️" ;;
                "in-progress") status_icon="🔄" ;;
            esac
            
            cat >> "$output_file" << EOF
### $status_icon **$case_title** $priority_icon

**Priority:** $priority  
**Issues:** $issues  
**Status:** $(echo $readiness | sed 's/-/ /g' | sed 's/\b\w/\U&/g')

**Investigation Summary:**
$summary

EOF

            # Add recommended actions if available
            if [ "$readiness" = "ready" ] || [ "$readiness" = "complete" ]; then
                echo "**Recommended Actions:**" >> "$output_file"
                extract_recommended_actions "$evidence_file" >> "$output_file"
                echo "" >> "$output_file"
            fi
            
            echo "---" >> "$output_file"
            echo "" >> "$output_file"
        fi
    done
    
    cat >> "$output_file" << EOF

## Investigation Conclusion

This comprehensive summary represents the current state of all active investigations in the Sherlock Holmes Investigation Bureau. Each case has been thoroughly analyzed by specialized Detective Claude instances working with expert sub-agents.

**Next Actions:**
1. Review ready-for-implementation cases for immediate deployment
2. Address blocked cases by resolving identified dependencies  
3. Continue monitoring in-progress investigations
4. Implement findings from completed high-priority cases first

---

*"Elementary, my dear Watson!"*

**Report compiled by:** Evidence Division  
**Bureau Location:** \`$EVIDENCE_DIR/\`  
**Case Files:** \`$CASES_DIR/\`

EOF

    echo -e "${GREEN}✅ Investigation summary compiled: $output_file${NC}"
}

compile_pr_readiness_report() {
    local output_file="$WORKSPACE_DIR/pr-readiness-report.md"
    
    echo -e "${BLUE}📋 Compiling PR readiness report...${NC}"
    
    cat > "$output_file" << EOF
# dbt Cloud Issues - PR Readiness Report

**Generated:** $(date)  
**Source:** Sherlock Holmes Investigation Bureau Evidence  

## Ready for Deployment

EOF

    local ready_count=0
    
    # Find cases that are ready for implementation
    for case_dir in "$CASES_DIR"/*; do
        if [ -d "$case_dir" ] && [ "$(basename "$case_dir")" != "archive" ]; then
            local case_file=$(basename "$case_dir")
            
            # Skip coordination file  
            if [ "$case_file" = "case-coordination.md" ]; then
                continue
            fi
            
            local evidence_file="$case_dir/evidence-report.md"
            local readiness=$(check_case_readiness "$evidence_file")
            
            if [ "$readiness" = "ready" ]; then
                ((ready_count++))
                
                local case_title=$(echo "$case_file" | sed 's/-/ /g' | sed 's/\b\w/\U&/g')
                local priority=$(get_case_priority "$case_dir")
                local issues=$(get_case_issues "$case_dir")
                
                cat >> "$output_file" << EOF
### ✅ $case_title ($priority Priority)

**Issues Resolved:** $issues  

**Actions Ready for Implementation:**
EOF
                extract_recommended_actions "$evidence_file" >> "$output_file"
                echo "" >> "$output_file"
                echo "---" >> "$output_file"
                echo "" >> "$output_file"
            fi
        fi
    done
    
    if [ $ready_count -eq 0 ]; then
        cat >> "$output_file" << EOF
*No investigations are currently marked as ready for implementation.*

Check investigation progress with: \`./sherlock/bureau/check-investigations.sh\`

EOF
    fi
    
    cat >> "$output_file" << EOF

## Implementation Priority

1. **HIGH Priority Cases** - Address critical blocking issues first
2. **Existing PRs** - Review and merge PRs #1814-1820 which already address many issues
3. **MEDIUM Priority Cases** - Data quality and business logic fixes
4. **LOW Priority Cases** - Minor issues and warnings

## Next Steps

1. Review this report with the development team
2. Plan implementation sprints based on priority and complexity
3. Test solutions in development environment before production deployment
4. Update case status after implementation

---

**Evidence Sources:** \`sherlock/cases/*/evidence-report.md\`  
**Full Investigation Summary:** \`sherlock/evidence/investigation-summary.md\`

EOF

    echo -e "${GREEN}✅ PR readiness report compiled: $output_file${NC}"
}

compile_next_actions() {
    local output_file="$WORKSPACE_DIR/next-actions.md"
    
    echo -e "${BLUE}📋 Compiling next actions list...${NC}"
    
    cat > "$output_file" << EOF
# dbt Cloud Issues - Next Actions

**Generated:** $(date)  
**Priority Order:** HIGH → MEDIUM → LOW  

EOF

    # Group actions by priority
    for priority_level in "HIGH" "MEDIUM" "LOW"; do
        cat >> "$output_file" << EOF
## $priority_level Priority Actions

EOF
        
        local found_actions=false
        
        for case_dir in "$CASES_DIR"/*; do
            if [ -d "$case_dir" ] && [ "$(basename "$case_dir")" != "archive" ]; then
                local case_file=$(basename "$case_dir")
                
                # Skip coordination file
                if [ "$case_file" = "case-coordination.md" ]; then
                    continue
                fi
                
                local priority=$(get_case_priority "$case_dir")
                
                if [ "$priority" = "$priority_level" ]; then
                    local case_title=$(echo "$case_file" | sed 's/-/ /g' | sed 's/\b\w/\U&/g')
                    local evidence_file="$case_dir/evidence-report.md"
                    local readiness=$(check_case_readiness "$evidence_file")
                    local issues=$(get_case_issues "$case_dir")
                    
                    cat >> "$output_file" << EOF
### $case_title
**Issues:** $issues  
**Status:** $(echo $readiness | sed 's/-/ /g' | sed 's/\b\w/\U&/g')

EOF
                    
                    if [ "$readiness" = "ready" ] || [ "$readiness" = "complete" ]; then
                        extract_recommended_actions "$evidence_file" >> "$output_file"
                        found_actions=true
                    elif [ "$readiness" = "blocked" ]; then
                        echo "🚧 **Blocked** - Resolve dependencies before proceeding" >> "$output_file"
                    elif [ "$readiness" = "in-progress" ]; then
                        echo "🔄 **In Progress** - Investigation active, await results" >> "$output_file"
                    else
                        echo "📋 **Pending** - Investigation not yet started" >> "$output_file"
                    fi
                    
                    echo "" >> "$output_file"
                    found_actions=true
                fi
            fi
        done
        
        if [ "$found_actions" = false ]; then
            echo "*No $priority_level priority cases found.*" >> "$output_file"
            echo "" >> "$output_file"
        fi
    done
    
    cat >> "$output_file" << EOF

## Immediate Next Steps

1. **Review existing PRs:** Check PRs #1814-1820 for merge readiness
2. **Address HIGH priority cases:** Focus on blocking issues first  
3. **Monitor active investigations:** Use \`./sherlock/bureau/check-investigations.sh --watch\`
4. **Plan implementation:** Schedule development work based on priority

## Investigation Commands

\`\`\`bash
# Check all investigation status
./sherlock/bureau/check-investigations.sh

# Detailed status view  
./sherlock/bureau/check-investigations.sh --detailed

# Continuous monitoring
./sherlock/bureau/check-investigations.sh --watch

# Recompile evidence
./sherlock/bureau/compile-evidence.sh
\`\`\`

---

**Investigation Bureau:** \`sherlock/\`  
**Full Evidence:** \`sherlock/evidence/investigation-summary.md\`

EOF

    echo -e "${GREEN}✅ Next actions compiled: $output_file${NC}"
}

compile_all_evidence() {
    print_header
    ensure_directories
    
    if [ ! -d "$CASES_DIR" ]; then
        echo -e "${RED}❌ No cases directory found${NC}"
        echo -e "${YELLOW}   Run: ./sherlock/bureau/dispatch-cases.sh first${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}📊 Compiling evidence from all investigations...${NC}"
    echo ""
    
    # Compile different report types
    compile_investigation_summary
    compile_pr_readiness_report  
    compile_next_actions
    
    echo ""
    echo -e "${GREEN}🎯 Evidence Compilation Complete!${NC}"
    echo ""
    echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
    echo -e "${BOLD}Reports Generated:${NC}"
    echo -e "📋 ${BLUE}Investigation Summary:${NC} sherlock/evidence/investigation-summary.md"
    echo -e "🚀 ${BLUE}PR Readiness Report:${NC} workspace/pr-readiness-report.md"  
    echo -e "📝 ${BLUE}Next Actions List:${NC} workspace/next-actions.md"
    echo ""
    echo -e "${CYAN}🔍 Present these findings to the client for case resolution!${NC}"
}

# Script execution
case "$1" in
    --help|-h)
        echo "Sherlock Holmes Investigation Bureau - Evidence Compiler"
        echo ""
        echo "Usage: $0 [options]"
        echo ""  
        echo "Options:"
        echo "  --help, -h        Show this help message"
        echo "  --summary-only    Compile investigation summary only"
        echo "  --pr-only         Compile PR readiness report only"
        echo "  --actions-only    Compile next actions list only"
        echo ""
        echo "Description:"
        echo "  Aggregates findings from all detective investigations into"
        echo "  comprehensive reports ready for client presentation."
        echo ""
        exit 0
        ;;
    --summary-only)
        print_header
        ensure_directories
        compile_investigation_summary
        ;;
    --pr-only)
        print_header  
        ensure_directories
        compile_pr_readiness_report
        ;;
    --actions-only)
        print_header
        ensure_directories
        compile_next_actions
        ;;
    *)
        compile_all_evidence
        ;;
esac