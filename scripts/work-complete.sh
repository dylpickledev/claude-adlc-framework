#!/bin/bash

# work-complete.sh - Complete work project and disseminate knowledge
# Usage: ./scripts/work-complete.sh <project-name>
# Example: ./scripts/work-complete.sh feature-snowflake-optimization

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validate arguments
if [ $# -ne 1 ]; then
    echo -e "${RED}Error: Invalid arguments${NC}"
    echo "Usage: $0 <project-name>"
    echo "Example: $0 feature-snowflake-optimization"
    exit 1
fi

PROJECT_NAME="$1"
PROJECT_DIR="projects/active/$PROJECT_NAME"

# Check if project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}Error: Project '$PROJECT_NAME' not found in $PROJECT_DIR${NC}"
    exit 1
fi

# Check if we're on the project branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$PROJECT_NAME" ]; then
    echo -e "${YELLOW}Warning: Not on project branch '$PROJECT_NAME' (currently on: $CURRENT_BRANCH)${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

echo -e "${BLUE}🔍 Analyzing project for knowledge extraction...${NC}"
echo "Project: $PROJECT_NAME"
echo "Directory: $PROJECT_DIR"
echo

# Create completion timestamp directory
COMPLETION_DATE=$(date '+%Y-%m')
ARCHIVE_DIR="projects/completed/$COMPLETION_DATE"
mkdir -p "$ARCHIVE_DIR"

# Function to perform knowledge dissemination reminder
suggest_knowledge_dissemination() {
    echo -e "${BLUE}=== KNOWLEDGE DISSEMINATION REMINDER ===${NC}"
    echo "Before completing, consider if any content should be disseminated:"
    echo
    
    # Check for different types of content worth preserving
    local suggestions_made=false
    
    # Check for technical learnings
    if find "$PROJECT_DIR" -name "*.md" -o -name "*.txt" | grep -v README.md | head -1 > /dev/null 2>&1; then
        echo -e "${YELLOW}📄 Technical Documentation:${NC} Consider copying to knowledge/technical/"
        suggestions_made=true
    fi
    
    # Check for code examples
    if find "$PROJECT_DIR" -name "*.py" -o -name "*.sql" -o -name "*.sh" | head -1 > /dev/null 2>&1; then
        echo -e "${YELLOW}💻 Code Examples:${NC} Consider copying to agents/<expert>/examples/"
        suggestions_made=true
    fi
    
    # Check for agent-specific learnings
    if grep -q -i "dbt\|snowflake\|tableau\|orchestra\|dlthub" "$PROJECT_DIR"/* 2>/dev/null; then
        echo -e "${YELLOW}🤖 Tool-Specific Learnings:${NC} Consider updating agent knowledge bases"
        suggestions_made=true
    fi
    
    if [ "$suggestions_made" = true ]; then
        echo
        echo "Note: Moving to completed/ signals that dissemination is done."
        echo "The full project history remains available in the git repository."
        echo
    fi
}

# Main workflow
echo -e "${BLUE}📋 Project Summary:${NC}"
if [ -f "$PROJECT_DIR/README.md" ]; then
    head -20 "$PROJECT_DIR/README.md" | grep -E "^#|^\*\*|^-" || echo "No structured content found in README"
fi
echo

suggest_knowledge_dissemination

# Confirm completion
echo
read -p "Ready to complete project? This will move it to completed/ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Completion cancelled."
    exit 1
fi

# Archive the project
echo -e "${BLUE}📦 Archiving project...${NC}"
cp -r "$PROJECT_DIR" "$ARCHIVE_DIR/$PROJECT_NAME"

# Clean up active directory
rm -rf "$PROJECT_DIR"

# Switch back to main branch
echo -e "${BLUE}🔀 Switching to main branch...${NC}"
git checkout main

# Optionally delete the work branch
echo
read -p "Delete work branch '$PROJECT_NAME'? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git branch -d "$PROJECT_NAME"
    echo -e "${GREEN}Work branch '$PROJECT_NAME' deleted.${NC}"
else
    echo -e "${YELLOW}Work branch '$PROJECT_NAME' kept for reference.${NC}"
fi

echo
echo -e "${GREEN}✅ Project completion successful!${NC}"
echo "Project: $PROJECT_NAME"
echo "Archived to: $ARCHIVE_DIR/$PROJECT_NAME"
echo "Status: Work completed and archived"
echo
echo "Remember to:"
echo "• Push any changes to remote repositories"
echo "• Update relevant documentation in knowledge/"
echo "• Share learnings with the team if applicable"