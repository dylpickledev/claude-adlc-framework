# D&A Agent Hub

A Claude Code sub-agent system for navigating complex data analytics stacks. This repository provides specialized expert agents for dbt, Orchestra, Tableau, Snowflake, dlthub, and business context management.

## Overview

The D&A Agent Hub implements a **research-only sub-agent pattern** where expert agents analyze and plan, while the parent Claude instance handles implementation. This approach optimizes token usage and provides specialized expertise for each tool in your data stack.

### Key Features

- **Sub-Agent Architecture**: Specialized experts for each tool (dbt, Orchestra, Tableau, Snowflake, dlthub)
- **Business Context Agent**: Flexible document retrieval from various sources
- **MCP Server Integration**: Pre-configured connections to data tools
- **Workspace Management**: Organized repository symlinks for easy navigation
- **Developer Customization**: Personal configuration framework
- **Cross-Platform Support**: macOS-optimized with tool-agnostic design

## Quick Start

### Prerequisites

- macOS (tested) or Linux
- Python 3.8+
- Git
- Claude Code CLI

### Installation

1. **Clone and setup the repository:**
   ```bash
   git clone <your-repo-url> da-agent-hub
   cd da-agent-hub
   ./setup.sh
   ```

2. **Configure your environment:**
   ```bash
   cp .env.template .env
   # Edit .env with your actual credentials
   ```

3. **Customize for your repositories:**
   ```bash
   ./developer/customize.sh
   ```

4. **Validate the setup:**
   ```bash
   ./scripts/test-setup.sh
   ```

5. **Activate the configuration:**
   ```bash
   scripts/manage-mcp.py add
   claude restart
   ```

## Sub-Agent System

### Architecture Pattern

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Parent Agent │───▶│  .claude/tasks/  │◀───│   Sub-Agent     │
│  (Claude Code)  │    │  current-task.md │    │   (Specialist)  │
│                 │    │  findings.md     │    │                 │
│  Implementation │    │  plan.md         │    │   Research Only │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Available Experts

| Agent | Location | Specialization |
|-------|----------|----------------|
| **dbt Expert** | `.claude/agents/dbt-expert.md` | SQL transformations, modeling, testing |
| **Orchestra Expert** | `.claude/agents/orchestra-expert.md` | Workflow orchestration, pipeline analysis |
| **Tableau Expert** | `.claude/agents/tableau-expert.md` | Dashboard optimization, reporting analysis |
| **Snowflake Expert** | `.claude/agents/snowflake-expert.md` | Query optimization, cost analysis |
| **dlthub Expert** | `.claude/agents/dlthub-expert.md` | Data ingestion, connector configuration |
| **Business Context** | `.claude/agents/business-context.md` | Requirements analysis, stakeholder context |

### Usage Pattern

1. **Task Assignment**: Assign research to appropriate expert
2. **Context Handoff**: Expert reads task from `.claude/tasks/current-task.md`
3. **Research Phase**: Expert analyzes and investigates thoroughly
4. **Documentation**: Expert creates detailed findings in `.claude/tasks/[tool]-findings.md`
5. **Implementation**: Parent agent executes based on expert recommendations

## Directory Structure

```
da-agent-hub/
├── .claude/
│   └── agents/                 # Claude Code sub-agents
│       ├── business-context.md # Business requirements expert
│       ├── dbt-expert.md      # dbt specialist
│       ├── orchestra-expert.md # Orchestra specialist
│       ├── tableau-expert.md  # Tableau specialist
│       ├── snowflake-expert.md # Snowflake specialist
│       └── dlthub-expert.md   # dlthub specialist
├── agents/                    # Documentation only (legacy structure)
├── knowledge/                  # Knowledge base
│   ├── business/               # Business context docs
│   ├── technical/              # Technical documentation
│   └── projects/               # Project-specific info
├── repos/                      # Symlinked repositories
├── developer/                  # Personal customizations
│   ├── customize.sh           # Personal setup script
│   └── workspace-config.json  # Repository configuration
├── scripts/                    # Utility scripts
│   ├── manage-mcp.py          # Unified MCP server management
│   ├── manage-workspace.sh    # Workspace manager
│   ├── manage-tasks.sh        # Task file management
│   └── test-setup.sh          # Setup validation
├── mcp-servers/               # MCP server implementations
└── setup.sh                  # Main setup script
```

## MCP Server Integration

### Currently Active

The system includes pre-configured MCP servers for:

- **dbt-mcp**: dbt Cloud and Snowflake transformations
- **freshservice-mcp**: IT service management and ticketing

### Planned Future Integrations

Additional servers are documented in `FUTURE-IMPROVEMENTS.md`:

- **ClickUp**: Project management (custom server)
- **Tableau**: Dashboard platform (awaiting uvx package)
- **Orchestra**: Workflow orchestration (awaiting uvx package)

### Configuration

MCP servers are configured directly in the management script using `claude mcp add` commands. Environment variables are loaded from `.env`.

**Management Commands:**
```bash
# Add all configured servers
scripts/manage-mcp.py add

# Check server status  
scripts/manage-mcp.py status

# List configured servers
scripts/manage-mcp.py list

# Remove specific server
scripts/manage-mcp.py remove server-name
```

## Workspace Management

### Repository Organization

Use the repository manager to organize your repositories:

```bash
# Setup repository symlinks
./scripts/manage-workspace.sh setup

# List current repositories
./scripts/manage-workspace.sh list

# Check repository status
./scripts/manage-workspace.sh status

# Clean broken links
./scripts/manage-workspace.sh clean
```

### Configuration

Edit `developer/workspace-config.json` to configure your repository paths:

```json
{
  "repositories": {
    "dbt": {
      "path": "/path/to/your/dbt/project",
      "description": "dbt transformation project",
      "enabled": true
    },
    "dlthub": {
      "path": "/path/to/your/dlthub/project",
      "description": "dlthub data ingestion project", 
      "enabled": true
    }
  }
}
```

## Developer Customization

### Personal Configuration

The `developer/` directory contains your personal customizations:

- `customize.sh`: Personal setup script
- `workspace-config.json`: Repository configuration
- `scripts/`: Custom scripts
- `configs/`: Personal configuration files
- `knowledge/`: Personal knowledge base

### Team Sharing

The system supports 90% shared configuration with 10% personal customization:

- **Shared**: Agent definitions, MCP configurations, scripts
- **Personal**: Repository paths, credentials, custom knowledge
- **Ignored**: The entire `developer/` directory is git-ignored

## Common Workflows

### Data Quality Investigation

```bash
# 1. Use Business Context Agent to understand requirements
# 2. Use Snowflake Expert to investigate data anomalies  
# 3. Use dbt Expert to review transformation logic
# 4. Use Orchestra Expert to check pipeline health
# 5. Implement coordinated remediation plan
```

### Performance Optimization

```bash
# 1. Use Tableau Expert to identify slow dashboards
# 2. Use Snowflake Expert to analyze query performance
# 3. Use dbt Expert to optimize model structure
# 4. Implement coordinated improvements
```

### New Feature Development

```bash
# 1. Use Business Context Agent to gather requirements
# 2. Use appropriate tool experts for technical analysis
# 3. Plan implementation across all affected systems
# 4. Coordinate deployment and testing
```

## Troubleshooting

### Setup Issues

1. **Run the test script:**
   ```bash
   ./scripts/test-setup.sh
   ```

2. **Check MCP server status:**
   ```bash
   claude mcp list
   ```

3. **Validate environment:**
   ```bash
   source venv/bin/activate
   python -c "import json; print('Python OK')"
   ```

### Common Problems

| Issue | Solution |
|-------|----------|
| MCP servers not loading | Check `.env` file, restart Claude |
| Repository symlinks broken | Run `./scripts/manage-workspace.sh clean` |
| Permission errors | Check script permissions with `chmod +x` |
| Python package issues | Recreate venv: `rm -rf venv && python3 -m venv venv` |

## Contributing

### Adding New Agents

1. Create agent directory: `agents/new-tool-expert/`
2. Add agent definition: `agents/new-tool-expert/agent.md`
3. Update documentation and tests

### Adding MCP Servers

1. Add server configuration to `scripts/manage-mcp.py`
2. Update environment template: `.env.template`  
3. Run `scripts/manage-mcp.py add` to configure
4. Test with `./scripts/test-setup.sh`

### Future Improvements

See `FUTURE-IMPROVEMENTS.md` for planned enhancements and roadmap.

## Support

For issues and feature requests, please see the project repository issues section.

## License

[Your License Here]