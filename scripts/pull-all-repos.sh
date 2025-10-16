#!/bin/bash
# Pull latest changes from all repositories defined in config/repositories.json

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🔄 Pulling latest from all repositories in config/repositories.json${NC}\n"

# Pull da-agent-hub itself first
echo -e "${GREEN}📦 da-agent-hub${NC}"
cd "$REPO_ROOT"
git checkout main
git pull origin main
echo ""

# Knowledge repos
echo -e "${BLUE}=== Knowledge Repositories ===${NC}"

cd "$REPO_ROOT/knowledge/da_obsidian"
echo -e "${GREEN}📦 da_obsidian${NC}"
git checkout master
git pull origin master
echo ""

cd "$REPO_ROOT/knowledge/da_team_documentation"
echo -e "${GREEN}📦 da_team_documentation${NC}"
git checkout main
git pull origin main
echo ""

# Orchestration repos
if [ -d "$REPO_ROOT/repos/orchestration" ]; then
    echo -e "${BLUE}=== Orchestration Repositories ===${NC}"

    if [ -d "$REPO_ROOT/repos/orchestration/orchestra" ]; then
        cd "$REPO_ROOT/repos/orchestration/orchestra"
        echo -e "${GREEN}📦 orchestra${NC}"
        git checkout master
        git pull origin master
        echo ""
    fi

    if [ -d "$REPO_ROOT/repos/orchestration/prefect" ]; then
        cd "$REPO_ROOT/repos/orchestration/prefect"
        echo -e "${GREEN}📦 prefect${NC}"
        git checkout master
        git pull origin master
        echo ""
    fi
fi

# Ingestion - Operational repos
if [ -d "$REPO_ROOT/repos/ingestion_operational" ]; then
    echo -e "${BLUE}=== Ingestion (Operational) Repositories ===${NC}"

    for repo in plantdemand_etl mapistry_etl postgres_pipelines; do
        if [ -d "$REPO_ROOT/repos/ingestion_operational/$repo" ]; then
            cd "$REPO_ROOT/repos/ingestion_operational/$repo"
            echo -e "${GREEN}📦 $repo${NC}"
            git checkout master
            git pull origin master
            echo ""
        fi
    done

    # XBE uses main branch
    if [ -d "$REPO_ROOT/repos/ingestion_operational/xbe_data_ingestion" ]; then
        cd "$REPO_ROOT/repos/ingestion_operational/xbe_data_ingestion"
        echo -e "${GREEN}📦 xbe_data_ingestion${NC}"
        git checkout main
        git pull origin main
        echo ""
    fi
fi

# Ingestion - Analytics repos
if [ -d "$REPO_ROOT/repos/ingestion_analytics" ]; then
    echo -e "${BLUE}=== Ingestion (Analytics) Repositories ===${NC}"

    if [ -d "$REPO_ROOT/repos/ingestion_analytics/hex_pipelines" ]; then
        cd "$REPO_ROOT/repos/ingestion_analytics/hex_pipelines"
        echo -e "${GREEN}📦 hex_pipelines${NC}"
        git checkout master
        git pull origin master
        echo ""
    fi

    if [ -d "$REPO_ROOT/repos/ingestion_analytics/dlthub" ]; then
        cd "$REPO_ROOT/repos/ingestion_analytics/dlthub"
        echo -e "${GREEN}📦 dlthub${NC}"
        git checkout main
        git pull origin main
        echo ""
    fi
fi

# Transformation repos
if [ -d "$REPO_ROOT/repos/transformation" ]; then
    echo -e "${BLUE}=== Transformation Repositories ===${NC}"

    if [ -d "$REPO_ROOT/repos/transformation/dbt_cloud" ]; then
        cd "$REPO_ROOT/repos/transformation/dbt_cloud"
        echo -e "${GREEN}📦 dbt_cloud (staging: dbt_dw)${NC}"
        git checkout dbt_dw
        git pull origin dbt_dw
        echo ""
    fi

    if [ -d "$REPO_ROOT/repos/transformation/dbt_postgres" ]; then
        cd "$REPO_ROOT/repos/transformation/dbt_postgres"
        echo -e "${GREEN}📦 dbt_postgres${NC}"
        git checkout master
        git pull origin master
        echo ""
    fi
fi

# Front End repos
if [ -d "$REPO_ROOT/repos/front_end" ]; then
    echo -e "${BLUE}=== Front End Repositories ===${NC}"

    for repo in streamlit_apps_snowflake snowflake_notebooks; do
        if [ -d "$REPO_ROOT/repos/front_end/$repo" ]; then
            cd "$REPO_ROOT/repos/front_end/$repo"
            echo -e "${GREEN}📦 $repo${NC}"
            git checkout master
            git pull origin master
            echo ""
        fi
    done

    # react-sales-journal uses master branch
    if [ -d "$REPO_ROOT/repos/front_end/react-sales-journal" ]; then
        cd "$REPO_ROOT/repos/front_end/react-sales-journal"
        echo -e "${GREEN}📦 react-sales-journal${NC}"
        git checkout master
        git pull origin master
        echo ""
    fi

    # da-app-portal uses master branch
    if [ -d "$REPO_ROOT/repos/front_end/da-app-portal" ]; then
        cd "$REPO_ROOT/repos/front_end/da-app-portal"
        echo -e "${GREEN}📦 da-app-portal${NC}"
        git checkout master
        git pull origin master
        echo ""
    fi
fi

# Operations repos
if [ -d "$REPO_ROOT/repos/operations" ]; then
    echo -e "${BLUE}=== Operations Repositories ===${NC}"

    if [ -d "$REPO_ROOT/repos/operations/roy_kent" ]; then
        cd "$REPO_ROOT/repos/operations/roy_kent"
        echo -e "${GREEN}📦 roy_kent${NC}"
        git checkout master
        git pull origin master
        echo ""
    fi

    if [ -d "$REPO_ROOT/repos/operations/sherlock" ]; then
        cd "$REPO_ROOT/repos/operations/sherlock"
        echo -e "${GREEN}📦 sherlock${NC}"
        git checkout main
        git pull origin main
        echo ""
    fi
fi

cd "$REPO_ROOT"
echo -e "${GREEN}✅ All repositories updated successfully!${NC}"
