# DA Agent Hub - Setup Guide

Quick setup guide for cloning and configuring the DA Agent Hub for your organization.

## Prerequisites

- [Claude Code CLI](https://docs.claude.com/en/docs/claude-code) installed
- Git installed
- GitHub CLI (`gh`) installed and authenticated
- Access to your organization's GitHub repositories

## Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/da-agent-hub.git
cd da-agent-hub
```

### 2. Make Scripts Executable

```bash
chmod +x scripts/*.sh
```

### 3. Configure Repositories (Optional)

If you want to work with multiple data stack repositories:

```bash
# Copy the example configuration
cp config/repositories.json.example config/repositories.json

# Edit with your organization's repositories
# Replace 'your-org' with your GitHub organization name
# Update URLs to match your actual repository names
```

**Note**: `config/repositories.json` is git-ignored to keep organization-specific configuration private.

### 4. Test the Installation

```bash
# Create your first idea
claude /idea "Test the DA Agent Hub setup"

# This should create a GitHub issue in your repository
```

## Available Commands

Once setup is complete, you have access to 5 core commands:

| Command | Purpose | Example |
|---------|---------|---------|
| `/idea` | Capture ideas as GitHub issues | `claude /idea "Build customer dashboard"` |
| `/research` | Deep analysis with specialist agents | `claude /research 123` |
| `/start` | Begin development from issue | `claude /start 123` |
| `/switch` | Context switching between projects | `claude /switch` |
| `/complete` | Finish and archive project | `claude /complete feature-project-name` |

## Available Agents

### Role Agents (Primary - 80% Independent)
- **analytics-engineer-role**: dbt models, SQL transformations, data modeling
- **data-engineer-role**: Pipeline setup, ingestion, orchestration
- **data-architect-role**: System design, architecture patterns

### Specialist Agents (Consultation - 20% Edge Cases)
- **dbt-expert**: SQL transformations, dbt patterns (MCP-enabled)
- **snowflake-expert**: Warehouse optimization (MCP-enabled)
- **github-sleuth-expert**: Repository analysis (MCP-enabled)
- **dlthub-expert**: Data ingestion patterns
- **tableau-expert**: BI optimization

## MCP Integration (Optional)

To enable MCP (Model Context Protocol) integration for real-time data access:

1. **dbt Cloud API**: Configure `.mcp.json` with dbt Cloud token
2. **Snowflake**: Configure `.mcp.json` with Snowflake credentials
3. **GitHub**: GitHub CLI authentication (`gh auth login`)

See [Claude Code MCP documentation](https://docs.claude.com/en/docs/claude-code/mcp) for detailed setup.

## VS Code Worktree Integration (Optional)

For seamless project switching with isolated workspaces:

```bash
claude /setup-worktrees
```

This enables:
- Dedicated worktree per project
- Automatic VS Code workspace switching
- Clean context separation

See `knowledge/da-agent-hub/development/vscode-worktree-integration.md` for details.

## First Project Workflow

```bash
# 1. Capture an idea
claude /idea "Analyze customer churn patterns"
# → Creates GitHub issue #1

# 2. (Optional) Deep analysis
claude /research 1
# → Adds analysis to issue as comment

# 3. Start development
claude /start 1
# → Creates projects/active/feature-analyze-customer-churn-patterns/

# 4. Work with agents
claude "use analytics-engineer-role to design the data model"

# 5. Complete project
claude /complete feature-analyze-customer-churn-patterns
# → Archives project, closes issue #1
```

## Repository Branch Cleanup (Maintainers)

If you see many old remote branches, clean them up:

```bash
# List merged branches
git branch -r --merged main | grep -v main | grep -v HEAD

# Delete merged remote branches (after confirming they're merged)
git push origin --delete <branch-name>

# Or use GitHub UI: Settings → Branches → Automatically delete head branches
```

## Troubleshooting

### "Permission denied" on scripts
```bash
chmod +x scripts/*.sh
```

### "gh: command not found"
```bash
# Install GitHub CLI
# macOS: brew install gh
# Linux: https://github.com/cli/cli#installation
# Windows: https://github.com/cli/cli#installation
```

### "Repository not found"
```bash
# Authenticate with GitHub CLI
gh auth login

# Verify you have access to the repository
gh repo view your-org/da-agent-hub
```

## Next Steps

1. **Read the docs**: Check `README.md` for full feature overview
2. **Review CLAUDE.md**: Understand the agent system and workflow
3. **Explore agents**: See `.claude/agents/` for agent capabilities
4. **Create your first idea**: Run `claude /idea "your idea"`

## Support

- **Documentation**: `knowledge/da-agent-hub/README.md`
- **Git Workflows**: `.claude/memory/patterns/git-workflow-patterns.md`
- **Testing Patterns**: `.claude/memory/patterns/testing-patterns.md`

---

**Ready to go!** Start with `claude /idea "your first idea"` and let the agents guide you.
