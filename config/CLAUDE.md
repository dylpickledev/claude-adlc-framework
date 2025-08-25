# D&A Agent Hub - Claude Code Context

This is the operational context for the D&A (Data & Analytics) Agent Hub. This file contains technical details and current state information for Claude Code to work effectively with this project.

## Current Project State

**Working Directory**: `/Users/dylanmorrish/da-agent-hub`
**Setup Status**: Configured with sub-agents and MCP servers
**Environment**: Development environment with local services

## Sub-Agent Architecture

### Research-Only Pattern
All sub-agents follow the **research and planning only** pattern:
- Sub-agents analyze and create detailed plans
- Parent agent implements based on sub-agent findings
- Communication via `.claude/tasks/` directory
- Clear separation between research and implementation

### Available Sub-Agents

#### Business Context Agent
**Purpose**: Flexible document retrieval and business knowledge management
**Location**: `agents/business-context/`
**Capabilities**: Retrieves relevant business context from various sources

#### Tool Experts
- **dbt Expert**: `agents/dbt-expert/` - dbt transformations and modeling
- **Orchestra Expert**: `agents/orchestra-expert/` - Workflow orchestration
- **Tableau Expert**: `agents/tableau-expert/` - Dashboard and reporting analysis
- **Snowflake Expert**: `agents/snowflake-expert/` - Data warehouse optimization
- **dlthub Expert**: `agents/dlthub-expert/` - Data loading and ingestion

## Available MCP Servers

### 1. dbt-mcp (uvx Package)
**Command**: `uvx --env-file .env dbt-mcp`
**Purpose**: dbt Cloud and Snowflake integration
**Environment**: Uses `.env` file for configuration

### 2. clickup (Node MCP Server)
**File**: `mcp-servers/clickup-mcp/dist/index.js`
**Environment Variables**: `CLICKUP_CLIENT_ID`, `CLICKUP_CLIENT_SECRET`, `CLICKUP_TEAM_ID`

### 3. freshservice-mcp (uvx Package)
**Command**: `uvx freshservice-mcp`
**Environment Variables**: `FRESHSERVICE_APIKEY`, `FRESHSERVICE_DOMAIN`

### 4. tableau (uvx Package)
**Command**: `uvx tableau-mcp`
**Environment Variables**: `TABLEAU_SERVER_URL`, `TABLEAU_USERNAME`, `TABLEAU_PASSWORD`, `TABLEAU_SITE_ID`

## File Locations & Paths

### Key Scripts
- `./setup.sh`: Main setup script
- `./scripts/merge_mcp_config.py`: MCP configuration merger
- `./developer/customize.sh`: Personal customization script

### Configuration Files
- `./.env`: Environment variables (not committed)
- `./config/mcp-base.json`: Base MCP server configuration
- `./config/CLAUDE.md`: This context template

### Directory Structure
```
da-agent-hub/
├── agents/                     # Sub-agent definitions
│   ├── business-context/
│   ├── dbt-expert/
│   ├── orchestra-expert/
│   ├── tableau-expert/
│   ├── snowflake-expert/
│   └── dlthub-expert/
├── knowledge/                  # Knowledge base
│   ├── business/
│   ├── technical/
│   └── projects/
├── config/                     # Configuration files
├── workspace/                  # Symlinked repositories
├── developer/                  # Personal customizations
├── scripts/                    # Utility scripts
└── mcp-servers/               # MCP server implementations
```

## Usage Patterns

### Sub-Agent Workflow
1. **Task Assignment**: Assign specific research to appropriate expert
2. **Context Handoff**: Expert reads from `.claude/tasks/current-task.md`
3. **Research Phase**: Expert analyzes and investigates thoroughly
4. **Documentation**: Expert creates detailed findings file
5. **Plan Creation**: Expert develops implementation plan
6. **Return to Parent**: Parent agent executes the plan

### Cross-Tool Workflows
- Query analysis: Snowflake Expert → dbt Expert → Implementation
- Pipeline issues: Orchestra Expert → dlthub Expert → Root cause analysis
- Performance problems: Tableau Expert → Snowflake Expert → Optimization

## Environment Configuration

### Database Connections
- **Snowflake**: Production data warehouse
- **PostgreSQL**: Local development database (if configured)

### API Integrations
- **dbt Cloud**: Transformation management
- **Orchestra**: Workflow orchestration
- **ClickUp**: Project management and task tracking
- **Freshservice**: IT service management
- **Tableau Server**: Business intelligence platform

## Common Workflows

### Data Quality Investigation
1. Use Snowflake Expert to investigate data anomalies
2. Use dbt Expert to review transformation logic
3. Use Orchestra Expert to check pipeline health
4. Create coordinated remediation plan

### Performance Optimization
1. Use Tableau Expert to identify slow dashboards
2. Use Snowflake Expert to analyze query performance
3. Use dbt Expert to optimize model structure
4. Implement coordinated improvements

### New Feature Development
1. Use Business Context Agent to gather requirements
2. Use appropriate tool experts for technical analysis
3. Plan implementation across all affected systems
4. Coordinate deployment and testing

## Important Notes

- **Security**: Never commit `.env` file or expose API keys
- **Sub-Agent Pattern**: Always use experts for research, parent for implementation
- **File Communication**: Use `.claude/tasks/` for sub-agent handoffs
- **Environment**: Activate Python venv before manual operations
- **MCP Updates**: Run `python scripts/merge_mcp_config.py` after changes
- **Restart Required**: Run `claude restart` after MCP configuration changes