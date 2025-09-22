#!/bin/bash

# ideate-export.sh - Export ideas/roadmaps for ClickUp integration
# Usage: ./scripts/ideate-export.sh [quarterly|cluster] [name]

set -e

# Configuration
IDEAS_DIR="ideas"
QUARTERLY_DIR="$IDEAS_DIR/quarterly"
ORGANIZED_DIR="$IDEAS_DIR/organized"
EXPORT_DIR="exports"

# Check arguments
if [ $# -lt 2 ]; then
    echo "📊 ClickUp Export Utility"
    echo ""
    echo "Usage: $0 [type] [name]"
    echo ""
    echo "Export Types:"
    echo "  quarterly [period]  - Export quarterly roadmap (e.g., Q2-2025)"
    echo "  cluster [name]      - Export organized idea cluster"
    echo ""
    echo "Examples:"
    echo "  $0 quarterly Q2-2025"
    echo "  $0 cluster customer-analytics"
    echo ""
    echo "📋 Available quarterly plans:"
    if [ -d "$QUARTERLY_DIR" ]; then
        find "$QUARTERLY_DIR" -maxdepth 1 -type d ! -path "$QUARTERLY_DIR" -exec basename {} \; | sort
    else
        echo "   No quarterly plans found."
    fi
    echo ""
    echo "📋 Available organized clusters:"
    if [ -d "$ORGANIZED_DIR" ]; then
        find "$ORGANIZED_DIR" -maxdepth 1 -type d ! -path "$ORGANIZED_DIR" -exec basename {} \; | sort
    else
        echo "   No organized clusters found."
    fi
    exit 1
fi

EXPORT_TYPE="$1"
EXPORT_NAME="$2"
TIMESTAMP=$(date +"%Y-%m-%d")

case "$EXPORT_TYPE" in
    "quarterly")
        QUARTERLY_PATH="$QUARTERLY_DIR/$EXPORT_NAME"
        if [ ! -d "$QUARTERLY_PATH" ]; then
            echo "❌ Error: Quarterly plan '$EXPORT_NAME' not found"
            echo "📋 Available plans:"
            find "$QUARTERLY_DIR" -maxdepth 1 -type d ! -path "$QUARTERLY_DIR" -exec basename {} \; | sort
            exit 1
        fi

        # Create export directory
        mkdir -p "$QUARTERLY_PATH/$EXPORT_DIR"
        EXPORT_FILE="$QUARTERLY_PATH/$EXPORT_DIR/clickup-strategic-export-$TIMESTAMP.md"

        echo "📊 Exporting quarterly roadmap: $EXPORT_NAME"
        echo "📁 Export location: $EXPORT_FILE"
        echo ""
        echo "🤖 Run: claude /export-clickup quarterly $EXPORT_NAME"
        echo ""
        echo "This will create a stakeholder-ready summary including:"
        echo "  - Executive overview of quarterly goals"
        echo "  - Strategic initiatives requiring cross-team coordination"
        echo "  - Resource requirements and timeline"
        echo "  - Key milestones for stakeholder tracking"
        echo "  - Risk factors and mitigation strategies"
        ;;

    "cluster")
        CLUSTER_PATH="$ORGANIZED_DIR/$EXPORT_NAME"
        if [ ! -d "$CLUSTER_PATH" ]; then
            echo "❌ Error: Cluster '$EXPORT_NAME' not found"
            echo "📋 Available clusters:"
            find "$ORGANIZED_DIR" -maxdepth 1 -type d ! -path "$ORGANIZED_DIR" -exec basename {} \; | sort
            exit 1
        fi

        # Create export directory
        mkdir -p "$CLUSTER_PATH/$EXPORT_DIR"
        EXPORT_FILE="$CLUSTER_PATH/$EXPORT_DIR/clickup-initiative-export-$TIMESTAMP.md"

        echo "📊 Exporting idea cluster: $EXPORT_NAME"
        echo "📁 Export location: $EXPORT_FILE"
        echo ""
        echo "🤖 Run: claude /export-clickup cluster $EXPORT_NAME"
        echo ""
        echo "This will create a strategic initiative summary including:"
        echo "  - Business problem and proposed solution"
        echo "  - Expected outcomes and success metrics"
        echo "  - Implementation phases and timeline"
        echo "  - Resource requirements and dependencies"
        echo "  - Stakeholder communication plan"
        ;;

    *)
        echo "❌ Error: Invalid export type '$EXPORT_TYPE'"
        echo "Valid types: quarterly, cluster"
        exit 1
        ;;
esac

echo ""
echo "📤 After export:"
echo "  1. Review generated summary for business language"
echo "  2. Share with leadership team for feedback"
echo "  3. Create corresponding ClickUp project/initiative"
echo "  4. Maintain link reference back to da-agent-hub"
echo ""
echo "🔗 Technical details remain in da-agent-hub for execution"