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

**Required Tools:**
- **Claude Code CLI** - [Install Guide](https://docs.anthropic.com/en/docs/claude-code/installation)
- **GitHub CLI (gh)** - [Install Guide](https://cli.github.com/manual/installation)

#### Quick Install Commands

**Claude Code CLI:**
```bash
# macOS (Homebrew)
brew install claude

# Linux (curl)
curl -fsSL https://claude.ai/install.sh | sh
```

**GitHub CLI:**
```bash
# macOS (Homebrew)  
brew install gh

# Linux (apt)
sudo apt install gh

# Or visit: https://cli.github.com/manual/installation
```

**Verification:**
```bash
claude --version    # Should show Claude Code version
gh --version       # Should show GitHub CLI version
```

### One-Command Installation

```bash
git clone https://github.com/graniterock/da-agent-hub.git da-agent-hub
cd da-agent-hub
./setup.sh
```

**That's it!** The setup script will:
- 🔍 Auto-detect your existing dbt projects and repositories
- ❓ Ask for only the credentials you actually need with helpful guidance
- 🔗 Test connections and validate configurations  
- 🏗️ Set up all MCP servers and agents automatically
- ✅ Provide a complete status report

**Setup time: 2-3 minutes**

### Status & Troubleshooting

```bash
# Check system status anytime
./setup.sh --status

# Re-run setup to update configuration  
./setup.sh

# Available Claude slash commands
/setup    # Interactive setup through Claude
/status   # System health check
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
| **DA Architect** | `.claude/agents/da-architect.md` | System design, data flow analysis, strategic platform decisions |

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
│   ├── agents/                 # Claude Code sub-agents
│   │   ├── business-context.md # Business requirements expert
│   │   ├── dbt-expert.md      # dbt specialist
│   │   ├── orchestra-expert.md # Orchestra specialist
│   │   ├── tableau-expert.md  # Tableau specialist
│   │   ├── snowflake-expert.md # Snowflake specialist
│   │   ├── dlthub-expert.md   # dlthub specialist
│   │   └── da-architect.md    # Data architecture specialist
│   ├── commands/              # Claude Code commands
│   └── tasks/                 # Task coordination files
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
└── setup.sh                  # Interactive setup script

## 🚀 Claude Code Best Practices for New Developers

*Based on [Anthropic's official Claude Code best practices guide](https://www.anthropic.com/engineering/claude-code-best-practices)*

### Quick Start Workflow (Recommended)

**1. 🔍 Explore, Plan, Code Pattern**
```bash
# Start by exploring what you have
/status                    # Check current system health
claude "analyze my dbt models"  # Let agents investigate first

# Then implement based on findings
claude "implement the recommendations from dbt-expert analysis"
```

**2. 🧪 Test-Driven Development for Data**
```bash
# Write tests first, confirm they fail
dbt test --select new_model --store-failures

# Implement to make tests pass  
dbt run --select new_model

# Verify success
dbt test --select new_model
```

**3. 📸 Visual Development (for dashboards)**
```bash
/screenshot    # Analyze dashboard screenshots
/visual-iterate # Structured design improvement workflow
```

### Advanced Workflows

**4. 🎯 Domain Expert Pattern**
```bash
# Use specific experts for complex analysis
claude --agent dbt-expert "analyze performance issues"
claude --agent snowflake-expert "optimize warehouse costs"  
claude --agent tableau-expert "improve dashboard load times"
```

**5. 🔧 GitHub CLI Integration**
```bash
/gh-workflow  # Enhanced PR and issue management
gh pr create --body "$(cat .claude/tasks/current-task.md)"
```

**6. 📋 Task Management**
- Always use TodoWrite for multi-step tasks
- Break complex work into smaller, trackable pieces
- Mark todos complete immediately after finishing

### Optimization Tips

**7. ⚡ Context Management**
- Use `/clear` when switching between different problem domains
- Provide specific instructions rather than vague requests
- Course-correct early if Claude misunderstands

**8. 🎪 Multi-Agent Coordination**
```bash
# Let experts analyze independently, then coordinate
claude "coordinate findings from dbt-expert and snowflake-expert analyses"
```

**9. 📊 Data Stack Workflows**
```bash
# Cross-system issue investigation
claude "investigate data quality issues across Orchestra → dbt → Snowflake pipeline"

# Performance optimization
claude "analyze end-to-end performance from source systems to dashboards"
```

### Key Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/setup` | Complete system setup | Initial configuration |
| `/status` | System health check | Regular maintenance |
| `/screenshot` | Visual analysis | Dashboard feedback |
| `/test-framework` | TDD workflows | Data quality testing |
| `/gh-workflow` | GitHub integration | PR automation |

### Pro Tips for Data Teams

**🔍 Investigation Pattern:**
1. Use business-context agent for requirements
2. Use technical experts for system analysis  
3. Use da-architect for cross-system decisions
4. Implement solutions incrementally

**⚡ Performance Optimization:**
- Run multiple Claude instances for parallel work
- Use git worktrees for concurrent feature development
- Leverage headless mode for automation tasks

**🛡️ Safety First:**
- All sub-agents are research-only (no system modification)
- Clear separation between analysis and implementation
- Built-in tool restrictions prevent accidents

### Getting Help

- **Documentation Issues**: Check `.claude/commands/` for examples
- **Setup Problems**: Run `./setup.sh --status` for diagnostics  
- **Agent Behavior**: Review `.claude/agents/` for role definitions
- **Best Practices**: This repo implements Anthropic's recommendations

**Remember**: The DA Agent Hub is designed around Claude Code best practices - explore, plan with agents, then implement systematically! 🎯

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