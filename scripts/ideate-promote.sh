#!/bin/bash

# ideate-promote.sh - Promote organized ideas to projects or ClickUp
# Usage: ./scripts/ideate-promote.sh [idea-cluster] [project|clickup]

set -e

# Configuration
IDEAS_DIR="ideas"
ORGANIZED_DIR="$IDEAS_DIR/organized"
PIPELINE_DIR="$IDEAS_DIR/pipeline"
PROJECTS_DIR="projects/active"

# Ensure directories exist
mkdir -p "$PIPELINE_DIR"

# Check arguments
if [ $# -eq 0 ]; then
    echo "📋 Available organized idea clusters:"
    if [ -d "$ORGANIZED_DIR" ]; then
        find "$ORGANIZED_DIR" -maxdepth 1 -type d ! -path "$ORGANIZED_DIR" -exec basename {} \; | sort
    else
        echo "   No organized ideas found. Run 'claude /organize' first."
    fi
    echo ""
    echo "Usage: $0 [cluster-name] [project|clickup]"
    echo "Example: $0 customer-analytics project"
    exit 1
fi

CLUSTER_NAME="$1"
PROMOTION_TYPE="${2:-project}"

CLUSTER_PATH="$ORGANIZED_DIR/$CLUSTER_NAME"

# Validate cluster exists
if [ ! -d "$CLUSTER_PATH" ]; then
    echo "❌ Error: Cluster '$CLUSTER_NAME' not found in $ORGANIZED_DIR"
    echo "📋 Available clusters:"
    find "$ORGANIZED_DIR" -maxdepth 1 -type d ! -path "$ORGANIZED_DIR" -exec basename {} \; | sort
    exit 1
fi

echo "🚀 Promoting idea cluster: $CLUSTER_NAME"
echo "📍 Promotion type: $PROMOTION_TYPE"

case "$PROMOTION_TYPE" in
    "project")
        echo "🔄 Creating active project..."
        echo ""
        echo "This will:"
        echo "  1. Run work-init.sh to create project structure"
        echo "  2. Populate spec.md with organized idea content"
        echo "  3. Link back to original ideation context"
        echo "  4. Move cluster to pipeline directory"
        echo ""
        echo "🤖 Run: claude /promote $CLUSTER_NAME project"
        echo ""
        echo "After promotion:"
        echo "  - Review projects/active/feature-$CLUSTER_NAME/"
        echo "  - Coordinate with recommended specialist agents"
        echo "  - Begin implementation phases"
        ;;
    "clickup")
        echo "📊 Exporting for ClickUp..."
        echo ""
        echo "This will:"
        echo "  1. Generate strategic summary in business language"
        echo "  2. Create stakeholder-ready export document"
        echo "  3. Include resource and timeline implications"
        echo "  4. Maintain technical link back to da-agent-hub"
        echo ""
        echo "🤖 Run: claude /promote $CLUSTER_NAME clickup"
        echo ""
        echo "After export:"
        echo "  - Share summary with leadership team"
        echo "  - Create ClickUp project with strategic milestones"
        echo "  - Schedule stakeholder alignment meeting"
        ;;
    *)
        echo "❌ Error: Invalid promotion type '$PROMOTION_TYPE'"
        echo "Valid types: project, clickup"
        exit 1
        ;;
esac

echo ""
echo "📁 Cluster location: $CLUSTER_PATH"
if [ -f "$CLUSTER_PATH/cluster-summary.md" ]; then
    echo "📄 Review cluster summary before promotion:"
    echo "   cat $CLUSTER_PATH/cluster-summary.md"
fi