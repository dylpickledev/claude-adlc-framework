#!/bin/bash

# Sherlock Holmes Investigation Bureau - Case Dispatch System
# Generates investigation case files from dbt issue analysis

SHERLOCK_DIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
CASES_DIR="$SHERLOCK_DIR/cases"
TEMPLATES_DIR="$SHERLOCK_DIR/templates"
EVIDENCE_DIR="$SHERLOCK_DIR/evidence"
ANALYSIS_FILE="workspace/dbt-cloud-pr-issue-analysis.md"

# Victorian detective styling
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "${PURPLE}"
    echo "🔍 SHERLOCK HOLMES INVESTIGATION BUREAU 🔍"
    echo "═══════════════════════════════════════════"
    echo "         Case Dispatch Department"
    echo "═══════════════════════════════════════════"
    echo -e "${NC}"
}

print_case_assignment() {
    local case_name=$1
    local issues=$2
    local priority=$3
    local detective_type=$4
    
    case $priority in
        "HIGH")     color=$RED ;;
        "MEDIUM")   color=$YELLOW ;;
        "LOW")      color=$GREEN ;;
        *)          color=$NC ;;
    esac
    
    echo -e "${color}📋 CASE: $case_name${NC}"
    echo -e "   Issues: $issues"
    echo -e "   Priority: $priority"
    echo -e "   Detective Type: $detective_type"
    echo ""
}

create_case_structure() {
    local case_dir=$1
    local case_name=$2
    local issues=$3
    local priority=$4
    local detective_type=$5
    local description=$6
    
    mkdir -p "$case_dir"
    
    # Case Brief
    cat > "$case_dir/case-brief.md" << EOF
# $(echo "$case_name" | tr '[:lower:]' '[:upper:]') 🔍

**Case Classification:** $priority PRIORITY
**Case Number:** $(date +%Y%m%d-%H%M%S)
**Assigned Issues:** $issues
**Detective Type Required:** $detective_type

## Case Description
$description

## Initial Evidence
- Analysis Report: @dbt-cloud-pr-issue-analysis.md
- Issues identified in central bureau analysis
- Cross-referenced with existing PR solutions

## Investigation Objective
$(get_investigation_objective "$case_name")

## Expected Evidence
- Root cause analysis
- Technical findings documentation
- Recommended action plan
- Cross-case dependencies noted

---
*"The game is afoot!" - S.H.*
EOF

    # Detective Instructions
    cat > "$case_dir/detective-instructions.md" << EOF
# DETECTIVE CLAUDE ASSIGNMENT 🕵️

## Your Mission Briefing
You are Detective Claude, assigned to **$(echo "$case_name" | tr '[:lower:]' '[:upper:]')**.

### Case Details
- **Read your case brief:** ./case-brief.md
- **Reference central analysis:** @dbt-cloud-pr-issue-analysis.md
- **Priority Level:** $priority
- **Issues:** $issues

### Expert Contacts (Sub-Agents) Available
$(get_expert_contacts "$detective_type")

### Investigation Protocol
1. **Scene Analysis**: Examine the technical evidence
2. **Expert Consultation**: Deploy appropriate sub-agents
3. **Cross-Reference**: Check with other active cases  
4. **Evidence Documentation**: Record findings systematically
5. **Conclusion**: Present actionable recommendations

### Evidence Documentation
Document all findings in: \`./evidence-report.md\`

Use the standard evidence template from bureau templates.

### Investigation Style
- Systematic and methodical approach
- Focus on root causes, not just symptoms  
- Cross-reference findings with other cases
- Present clear, actionable conclusions

---
*"You see, but you do not observe." - S.H.*
EOF

    # Evidence Report Template
    cat > "$case_dir/evidence-report.md" << EOF
# EVIDENCE REPORT: $(echo "$case_name" | tr '[:lower:]' '[:upper:]')

**Detective:** Claude  
**Date:** $(date +"%Y-%m-%d %H:%M:%S")  
**Case Priority:** $priority  

## Investigation Summary
*[Provide overview of investigation conducted]*

## Technical Evidence Gathered
*[Detail technical findings from sub-agent analysis]*

## Root Cause Analysis  
*[Identify underlying causes, not just symptoms]*

## Cross-Case Dependencies
*[Note any connections to other active investigations]*

## Recommended Actions
*[Provide specific, actionable recommendations]*

## Case Status
- [ ] Investigation Complete
- [ ] Ready for Implementation  
- [ ] Requires Additional Evidence
- [ ] Blocked by Dependencies

---
**Detective Signature:** Claude  
**Bureau File:** $case_dir
EOF

    echo -e "${GREEN}✓ Case file created: $case_dir${NC}"
}

get_investigation_objective() {
    local case_name=$1
    case $case_name in
        "the-camera-mystery")
            echo "Identify root cause of 5.3M duplicate camera records and provide remediation strategy"
            ;;
        "inventory-ledger-affair")
            echo "Resolve JDE F4111 vs data mart reconciliation failures and fix cross-system validation"
            ;;
        "pr-review-critical")
            echo "Analyze ready-to-merge PRs for deployment readiness and identify any blockers"
            ;;
        "fuelcloud-duplicates")
            echo "Consolidate duplicate FuelCloud issues and implement unified deduplication solution"
            ;;
        "safety-validation")
            echo "Resolve safety inspection validation failures and inappropriate test configurations"
            ;;
        "accounting-mysteries")
            echo "Fix accounting master units duplication through proper surrogate key handling"
            ;;
        "business-logic-validation")
            echo "Address business logic validation failures in tickets and freight reporting"
            ;;
        *)
            echo "Conduct thorough investigation and provide actionable technical recommendations"
            ;;
    esac
}

get_expert_contacts() {
    local detective_type=$1
    case $detective_type in
        "data-forensics")
            cat << EOF
- **Sherlock Snowflake** (snowflake-expert): Database forensics and query analysis
- **Watson dbt** (dbt-expert): Model logic and transformation analysis  
- **Inspector Business** (business-context): Domain knowledge and requirements
EOF
            ;;
        "pr-analysis")
            cat << EOF
- **Watson dbt** (dbt-expert): Code review and model analysis
- **Inspector Business** (business-context): Business impact assessment
- **Professor GitHub** (github-expert): PR and branch analysis
EOF
            ;;
        "pipeline-investigation")
            cat << EOF
- **Colonel Orchestra** (orchestra-expert): Pipeline orchestration analysis
- **Watson dbt** (dbt-expert): Transformation logic review
- **Sherlock Snowflake** (snowflake-expert): Data warehouse impact analysis
EOF
            ;;
        *)
            cat << EOF
- **Watson dbt** (dbt-expert): Primary dbt analysis expert
- **Sherlock Snowflake** (snowflake-expert): Database and query analysis
- **Inspector Business** (business-context): Business domain expertise
EOF
            ;;
    esac
}

# Main case dispatch logic
dispatch_cases() {
    print_header
    
    if [ ! -f "$ANALYSIS_FILE" ]; then
        echo -e "${RED}❌ Analysis file not found: $ANALYSIS_FILE${NC}"
        echo "Please run the issue analysis first."
        exit 1
    fi
    
    echo -e "${BLUE}📝 Dispatching cases based on analysis...${NC}"
    echo ""
    
    # High Priority Cases
    print_case_assignment "THE CAMERA MYSTERY" "#1750" "HIGH" "data-forensics"
    create_case_structure "$CASES_DIR/the-camera-mystery" "the-camera-mystery" "#1750" "HIGH" "data-forensics" \
        "Massive duplication in fact_camera model with 5,388,082 duplicate records causing data warehouse bloat."
    
    print_case_assignment "INVENTORY LEDGER AFFAIR" "#1574, #1800, #1591" "HIGH" "data-forensics"
    create_case_structure "$CASES_DIR/inventory-ledger-affair" "inventory-ledger-affair" "#1574, #1800, #1591" "HIGH" "data-forensics" \
        "Cross-system validation failures between JDE F4111 and data mart, affecting inventory reconciliation."
    
    # PR Review Squad  
    print_case_assignment "PR REVIEW CRITICAL SQUAD" "PRs #1814-1820" "MEDIUM" "pr-analysis"
    create_case_structure "$CASES_DIR/pr-review-critical" "pr-review-critical" "PRs #1814-1820" "MEDIUM" "pr-analysis" \
        "Analysis of 7 ready-to-merge PRs that address multiple dbt issues. Verify deployment readiness."
    
    # Medium Priority Cases
    print_case_assignment "FUELCLOUD DUPLICATES" "#1806, #1752" "MEDIUM" "data-forensics" 
    create_case_structure "$CASES_DIR/fuelcloud-duplicates" "fuelcloud-duplicates" "#1806, #1752" "MEDIUM" "data-forensics" \
        "Consolidate duplicate FuelCloud concrete fuel usage issues (1,820 duplicate primary keys)."
    
    print_case_assignment "BUSINESS LOGIC VALIDATION" "#1748, #1731, #1728" "MEDIUM" "pipeline-investigation"
    create_case_structure "$CASES_DIR/business-logic-validation" "business-logic-validation" "#1748, #1731, #1728" "MEDIUM" "pipeline-investigation" \
        "Freight reporting, safety inspections, and ticket validation business logic failures."
    
    # Low Priority Cases  
    print_case_assignment "MINOR INCIDENTS" "#1801, #1788, #1749" "LOW" "data-forensics"
    create_case_structure "$CASES_DIR/minor-incidents" "minor-incidents" "#1801, #1788, #1749" "LOW" "data-forensics" \
        "Low-impact null value and duplicate record issues requiring routine investigation."
    
    # Create coordination hub
    cat > "$CASES_DIR/case-coordination.md" << EOF
# SHERLOCK HOLMES INVESTIGATION BUREAU - COORDINATION HUB

**Bureau Chief:** Inspector Dylan  
**Investigation Start Date:** $(date +"%Y-%m-%d %H:%M:%S")

## Active Cases Status

| Case Name | Priority | Issues | Detective Assigned | Status |
|-----------|----------|--------|-------------------|---------|
| The Camera Mystery | HIGH | #1750 | TBD | 📋 Case Filed |
| Inventory Ledger Affair | HIGH | #1574, #1800, #1591 | TBD | 📋 Case Filed |
| PR Review Critical | MEDIUM | PRs #1814-1820 | TBD | 📋 Case Filed |
| FuelCloud Duplicates | MEDIUM | #1806, #1752 | TBD | 📋 Case Filed |
| Business Logic Validation | MEDIUM | #1748, #1731, #1728 | TBD | 📋 Case Filed |
| Minor Incidents | LOW | #1801, #1788, #1749 | TBD | 📋 Case Filed |

## Investigation Notes
*Bureau coordination notes will be updated here as cases progress*

## Cross-Case Dependencies
- Camera Mystery insights may inform FuelCloud Duplicates approach
- PR Review results will unblock several investigation paths
- Inventory Ledger findings critical for data quality initiatives

---
**Next Action:** Deploy detective squad via \`./bureau/deploy-detectives.sh\`
EOF
    
    echo -e "${GREEN}✅ All cases dispatched successfully!${NC}"
    echo ""
    echo -e "${CYAN}📂 Cases created in: $CASES_DIR${NC}"
    echo -e "${CYAN}📋 Coordination hub: $CASES_DIR/case-coordination.md${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Next step: Deploy the detective squad!${NC}"
    echo -e "   Run: ${BLUE}./sherlock/bureau/deploy-detectives.sh${NC}"
}

# Script execution
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0"
    echo ""
    echo "Dispatches investigation cases based on dbt issue analysis."
    echo "Creates case files and detective assignments for parallel investigation."
    echo ""
    echo "Files created:"
    echo "  - Case briefs with issue details"
    echo "  - Detective instructions with sub-agent guidance"  
    echo "  - Evidence report templates"
    echo "  - Central coordination hub"
    exit 0
fi

dispatch_cases