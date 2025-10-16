# DA Agent Hub

> AI-powered Analytics Development Lifecycle (ADLC) workflow for data and analytics engineers

**5 commands + 8 agents + MCP integration = Your complete data engineering AI assistant**

---

## What This Does

Implements the [dbt Analytics Development Lifecycle](https://www.getdbt.com/analytics-engineering/transformation/) with AI agents that understand dbt, Snowflake, and your modern data stack.

**Core workflow:**
```bash
/capture "idea" → /research → /start → /switch → /pause → /complete
```

**Available agents:**
- **Roles**: analytics-engineer-role, data-engineer-role, data-architect-role
- **Specialists**: dbt-expert, snowflake-expert, github-sleuth-expert, dlthub-expert, tableau-expert

**MCP integration:**
- Direct access to dbt Cloud API
- Query Snowflake warehouse
- GitHub repository operations

---

## Quick Start

```bash
# Clone
git clone https://github.com/yourusername/da-agent-hub.git
cd da-agent-hub

# Make scripts executable
chmod +x scripts/*.sh

# Start using
claude /capture "Build customer churn prediction model"
```

---

## The 5 Commands

### 1. `/capture` - Capture ideas
Creates GitHub issues for data initiatives
```bash
claude /capture "Optimize Snowflake costs"
```

### 2. `/research` - Deep exploration
Specialist agents analyze technical approach
```bash
claude /research "dbt incremental model strategy"
claude /research 123  # Analyze issue #123
```

### 3. `/start` - Begin development
Creates project structure + git worktree
```bash
claude /start 123  # From issue
claude /start "new project idea"  # Creates issue + starts
```

### 4. `/switch` - Context switching
Zero-loss project switching with backup
```bash
claude /switch  # Save current, switch to main
claude /switch feature-branch  # Switch to specific branch
```

### 5. `/complete` - Finish project
Archives project, closes issue, cleans up
```bash
claude /complete feature-project-name
```

**Note**: Use GitHub's native issue management, labels, and milestones for roadmap planning and prioritization.

---

## The Agents

### Role Agents (Primary - 80% Independent Work)
**analytics-engineer-role**
- dbt models, SQL transformations, data modeling
- Performance optimization, semantic layer, BI data prep
- Delegates to specialists for complex edge cases

**data-engineer-role**
- Pipeline setup, ingestion, orchestration
- Source system integration, data quality at ingestion
- Chooses right tool (dlthub vs Prefect vs Airbyte)

**data-architect-role**
- System design, architecture patterns
- Technology selection, cross-system integration
- Strategic platform decisions

### Specialist Agents (Consultation Layer - 20% Edge Cases)
**dbt-expert** - SQL transformations, dbt patterns (MCP-enabled)

**snowflake-expert** - Warehouse optimization, cost analysis (MCP-enabled)

**github-sleuth-expert** - Repository analysis, issue investigation (MCP-enabled)

**dlthub-expert** - Data ingestion patterns

**tableau-expert** - BI optimization

---

## MCP Integration

Agents access your data systems in real-time:

```
dbt-expert:
   ├─ dbt-mcp → Access dbt Cloud API (jobs, runs, models, tests)
   ├─ snowflake-mcp → Query Snowflake directly
   └─ Returns: Performance optimizations based on actual query patterns

snowflake-expert:
   ├─ snowflake-mcp → Warehouse metadata, cost analysis
   └─ Returns: Cost optimization with projected savings

github-sleuth-expert:
   ├─ github-mcp → Repository operations, issue analysis
   └─ Returns: Cross-repo coordination recommendations
```

**Result:** AI decisions based on REAL data, not generic advice.

---

## Installation

### Prerequisites
- [Claude Code CLI](https://docs.claude.com/en/docs/claude-code)
- Git
- Modern data stack (dbt, Snowflake, etc.)

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/da-agent-hub.git
cd da-agent-hub

# Make scripts executable
chmod +x scripts/*.sh

# Optional: VS Code worktree integration
claude /setup-worktrees

# Start using
claude /capture "Your first data project idea"
```

### MCP Configuration (Optional)
Configure MCP servers in `.mcp.json` for real-time data access:
- dbt Cloud API token
- Snowflake credentials
- GitHub personal access token

See `knowledge/da-agent-hub/development/setup.md` for detailed MCP setup.

---

## Example Workflow

```bash
# 1. Capture idea
claude /capture "Build real-time customer analytics dashboard"
# → Creates GitHub issue #123

# 2. Research approach (optional for complex projects)
claude /research 123
# → Specialist agents analyze: data sources, dbt models needed, BI layer

# 3. Start development
claude /start 123
# → Creates: projects/active/feature-real-time-customer-analytics/
# → Sets up git worktree (if configured)
# → Links to GitHub issue

# 4. Development with specialists
claude "use analytics-engineer-role to build dbt models for customer metrics"
claude "use data-engineer-role to set up incremental refresh pipeline"

# 5. Switch to urgent work
claude /switch  # Saves current state
claude /start 125  # Work on urgent issue
claude /complete feature-urgent-fix
claude /switch feature-real-time-customer-analytics  # Resume

# 6. Complete project
claude /complete feature-real-time-customer-analytics
# → Archives project
# → Closes GitHub issue #123
# → Cleans up worktree
```

---

## Why This Matters

**For data engineers:**
- Specialist agents understand dbt patterns, Snowflake optimization, pipeline orchestration
- MCP integration = decisions based on YOUR actual data warehouse state
- Multi-repo coordination across dbt, source control, BI tools

**For analytics engineers:**
- AI that knows dimensional modeling, incremental strategies, semantic layers
- Direct dbt Cloud API access for model analysis
- Testing and data quality validation built-in

**For data architects:**
- System-level thinking across ingestion → transformation → consumption
- Cross-tool coordination (Orchestra, dlthub, Prefect, dbt, Tableau)
- Architecture patterns specific to modern data stacks

---

## Core Scripts

Essential scripts (automatically called by slash commands):
- `capture.sh` → Creates GitHub issues (called by `/capture`)
- `start.sh` → Project initialization (called by `/start`)
- `research.sh` → Research helper (called by `/research`)
- `switch.sh` → Context switching (called by `/switch`)
- `finish.sh` → Project completion (called by `/complete`)
- `work-init.sh` → Project setup (called by start.sh)
- `setup-worktrees.sh` → VS Code integration (called by `/setup-worktrees`)
- `pull-all-repos.sh` → Sync multiple repos
- `resolve-repo-context.py` → Multi-repo support
- `get-repo-owner.sh` → Helper utility

---

## Project Structure

When you `/start` a project:
```
projects/active/feature-project-name/
├── README.md      # Navigation hub
├── spec.md        # Requirements from GitHub issue
├── context.md     # Dynamic state tracking
└── tasks/         # Agent coordination
    ├── current-task.md
    └── [tool]-findings.md
```

---

## Documentation

- `CLAUDE.md` - Project instructions for Claude
- `knowledge/da-agent-hub/` - Platform documentation
- `.claude/agents/` - Agent definitions and prompts

---

## Git Workflow

**Protected branches:** Never push directly to main/master/production
- Always create feature branch
- All code changes require PR workflow
- Use commands: `/start` creates branch, `/complete` guides PR creation

**Multi-repo support:**
- Configure repositories in `config/repositories.json.example`
- Smart context resolution for cross-repo coordination
- Automatic owner/repo detection for GitHub operations

---

## License

MIT License - See LICENSE file

---

## Credits

Built for data/analytics engineers who want AI that understands their modern data stack.

**Inspired by:**
- [dbt Analytics Development Lifecycle](https://www.getdbt.com/analytics-engineering/transformation/)
- [Anthropic's Claude Code](https://docs.claude.com/en/docs/claude-code)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

---

**Focus:** ADLC workflow for data engineering • 6 commands • 8 specialist agents • MCP integration
