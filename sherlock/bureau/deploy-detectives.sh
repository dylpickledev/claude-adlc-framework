#!/bin/bash

# Sherlock Holmes Investigation Bureau - Detective Deployment System
# Launches multiple Claude instances as specialized detectives

SHERLOCK_DIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
CASES_DIR="$SHERLOCK_DIR/cases"

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
    echo "       Detective Deployment Division"  
    echo "═══════════════════════════════════════════"
    echo -e "${NC}"
}

print_detective_assignment() {
    local case_name=$1
    local priority=$2
    local status=$3
    
    case $priority in
        "HIGH")     color=$RED ;;
        "MEDIUM")   color=$YELLOW ;;
        "LOW")      color=$GREEN ;;
        *)          color=$NC ;;
    esac
    
    echo -e "${color}🕵️  Detective Claude → $case_name ($priority)${NC}"
    echo -e "   Status: $status"
}

check_prerequisites() {
    echo -e "${BLUE}📋 Checking deployment prerequisites...${NC}"
    
    if [ ! -d "$CASES_DIR" ]; then
        echo -e "${RED}❌ Cases directory not found: $CASES_DIR${NC}"
        echo -e "${YELLOW}   Run: ./sherlock/bureau/dispatch-cases.sh first${NC}"
        exit 1
    fi
    
    local case_count=$(find "$CASES_DIR" -mindepth 1 -maxdepth 1 -type d | grep -v archive | wc -l)
    if [ "$case_count" -eq 0 ]; then
        echo -e "${RED}❌ No cases found for deployment${NC}"
        echo -e "${YELLOW}   Run: ./sherlock/bureau/dispatch-cases.sh first${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Found $case_count cases ready for investigation${NC}"
    echo ""
}

deploy_detective() {
    local case_dir=$1
    local case_name=$(basename "$case_dir")
    local case_title=$(echo "$case_name" | sed 's/-/ /g' | sed 's/\b\w/\U&/g')
    
    # Get case priority from case-brief.md
    local priority="MEDIUM"
    if [ -f "$case_dir/case-brief.md" ]; then
        priority=$(grep "Case Classification:" "$case_dir/case-brief.md" | cut -d' ' -f3)
    fi
    
    # Create detective startup script for this case
    local detective_script="/tmp/detective-$case_name-$(date +%s).sh"
    cat > "$detective_script" << EOF
#!/bin/bash

# Detective Claude Startup Script for: $case_title
# Generated: $(date)

CASE_DIR="$case_dir"
CASE_NAME="$case_name"

# Terminal customization
echo -e "\033]0;Detective Claude: $case_title\007"

# Print detective briefing
cat << 'BRIEFING'
🔍 DETECTIVE CLAUDE REPORTING FOR DUTY 🔍

Case Assignment: $case_title
Case Directory: $case_dir
Priority Level: $priority

═══════════════════════════════════════════
Your mission awaits in the case files...
═══════════════════════════════════════════

BRIEFING

echo ""
echo "📂 Case Files Available:"
echo "   📋 case-brief.md           - Your case assignment"
echo "   🕵️  detective-instructions.md - Investigation protocol" 
echo "   📝 evidence-report.md      - Document findings here"
echo ""
echo "📖 Reading case brief..."
echo ""

# Show case brief if it exists
if [ -f "\$CASE_DIR/case-brief.md" ]; then
    cat "\$CASE_DIR/case-brief.md"
    echo ""
    echo "═══════════════════════════════════════════"
    echo ""
fi

echo "🚀 Ready to start investigation!"
echo "💡 Tip: Read your detective-instructions.md for guidance"
echo ""

# Change to case directory
cd "\$CASE_DIR"

# Start Claude with context
claude --new-session
EOF

    chmod +x "$detective_script"
    
    # Launch detective in new terminal (works on macOS)
    if command -v osascript >/dev/null 2>&1; then
        # macOS - open new Terminal window
        osascript << EOF
tell application "Terminal"
    activate
    do script "$detective_script; rm -f $detective_script"
end tell
EOF
        print_detective_assignment "$case_title" "$priority" "🚀 Deployed in new terminal"
    elif command -v gnome-terminal >/dev/null 2>&1; then
        # Linux with GNOME Terminal
        gnome-terminal --title="Detective Claude: $case_title" -- bash -c "$detective_script; rm -f $detective_script; exec bash"
        print_detective_assignment "$case_title" "$priority" "🚀 Deployed in GNOME terminal"
    elif command -v xterm >/dev/null 2>&1; then
        # Fallback to xterm
        xterm -title "Detective Claude: $case_title" -e "$detective_script; rm -f $detective_script; exec bash" &
        print_detective_assignment "$case_title" "$priority" "🚀 Deployed in xterm"
    else
        # Fallback - just show instructions
        echo -e "${YELLOW}⚠️  Unable to auto-launch terminal${NC}"
        echo -e "${CYAN}   Manual deployment required:${NC}"
        echo -e "   cd $case_dir"
        echo -e "   claude --new-session"
        print_detective_assignment "$case_title" "$priority" "📋 Manual deployment required"
        rm -f "$detective_script"
    fi
    
    # Small delay between deployments
    sleep 1
}

deploy_squad() {
    print_header
    check_prerequisites
    
    echo -e "${BLUE}🚀 Deploying detective squad...${NC}"
    echo ""
    
    # Count cases by priority
    local high_count=0
    local medium_count=0
    local low_count=0
    
    # Deploy detectives for each case
    for case_dir in "$CASES_DIR"/*; do
        if [ -d "$case_dir" ] && [ "$(basename "$case_dir")" != "archive" ]; then
            # Skip coordination file
            if [ "$(basename "$case_dir")" = "case-coordination.md" ]; then
                continue
            fi
            
            deploy_detective "$case_dir"
            
            # Count by priority
            if [ -f "$case_dir/case-brief.md" ]; then
                local priority=$(grep "Case Classification:" "$case_dir/case-brief.md" | cut -d' ' -f3)
                case $priority in
                    "HIGH") ((high_count++)) ;;
                    "MEDIUM") ((medium_count++)) ;;
                    "LOW") ((low_count++)) ;;
                esac
            fi
        fi
    done
    
    echo ""
    echo -e "${GREEN}🎯 Detective Squad Deployment Complete!${NC}"
    echo ""
    echo -e "${CYAN}📊 Squad Composition:${NC}"
    echo -e "   🔴 High Priority Cases: $high_count detectives"
    echo -e "   🟡 Medium Priority Cases: $medium_count detectives" 
    echo -e "   🟢 Low Priority Cases: $low_count detectives"
    echo ""
    echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
    echo -e "${BOLD}Each detective has been briefed with:${NC}"
    echo -e "• Case assignment and priority level"
    echo -e "• Investigation protocols and sub-agent contacts"
    echo -e "• Evidence documentation templates"
    echo -e "• Cross-case coordination guidelines"
    echo ""
    echo -e "${YELLOW}📋 Next Steps:${NC}"
    echo -e "1. Each detective will start their investigation"
    echo -e "2. Monitor progress: ${BLUE}./sherlock/bureau/check-investigations.sh${NC}"
    echo -e "3. Compile results: ${BLUE}./sherlock/bureau/compile-evidence.sh${NC}"
    echo ""
    echo -e "${CYAN}🔍 The game is afoot!${NC}"
}

# Handle command line arguments
case "$1" in
    --help|-h)
        echo "Sherlock Holmes Investigation Bureau - Detective Deployment"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h    Show this help message"
        echo "  --dry-run     Show what would be deployed without launching"
        echo ""
        echo "Description:"
        echo "  Deploys multiple Detective Claude instances, each assigned to"
        echo "  specific investigation cases. Each detective opens in a new"
        echo "  terminal window with case-specific briefings and instructions."
        echo ""
        echo "Prerequisites:"
        echo "  - Cases must be dispatched first: ./dispatch-cases.sh"
        echo "  - Terminal application must be available"
        echo ""
        exit 0
        ;;
    --dry-run)
        print_header
        check_prerequisites
        echo -e "${YELLOW}🔍 DRY RUN: Detective deployment preview${NC}"
        echo ""
        for case_dir in "$CASES_DIR"/*; do
            if [ -d "$case_dir" ] && [ "$(basename "$case_dir")" != "archive" ]; then
                if [ "$(basename "$case_dir")" = "case-coordination.md" ]; then
                    continue
                fi
                local case_name=$(basename "$case_dir")
                local case_title=$(echo "$case_name" | sed 's/-/ /g' | sed 's/\b\w/\U&/g')
                local priority="MEDIUM"
                if [ -f "$case_dir/case-brief.md" ]; then
                    priority=$(grep "Case Classification:" "$case_dir/case-brief.md" | cut -d' ' -f3)
                fi
                print_detective_assignment "$case_title" "$priority" "📋 Would deploy"
            fi
        done
        echo ""
        echo -e "${BLUE}Run without --dry-run to deploy the squad${NC}"
        exit 0
        ;;
    *)
        deploy_squad
        ;;
esac