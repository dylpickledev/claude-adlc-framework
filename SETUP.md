# Claude ADLC Framework - Setup Guide

Quick setup guide for installing and configuring the Claude ADLC Framework for your data team.

## Prerequisites

- [Claude Code CLI](https://docs.claude.com/en/docs/claude-code) installed
- Git installed
- GitHub CLI (`gh`) installed and authenticated
- Node.js/npm installed (for MCP servers)

## Quick Setup

### Option A: Interactive Setup (Recommended)

The fastest way to get started:

```bash
# Clone the repository
git clone https://github.com/your-org/claude-adlc-framework.git
cd claude-adlc-framework

# Run interactive onboarding
./setup.sh
```

The interactive onboarding will:
1. ✅ Discover your data stack (dbt, Snowflake, Tableau, etc.)
2. ✅ Configure specialist agents for your tools
3. ✅ Set up dbt MCP server with your preferred authentication method:
   - **Local .env** (simplest - credentials in .env file)
   - **Local OAuth** (most secure - browser-based auth)
   - **Remote OAuth** (team/cloud - centralized MCP server)
4. ✅ Optional: Configure Snowflake, GitHub, and other MCP servers
5. ✅ Quick tutorial on the ADLC workflow

Takes about 5 minutes to complete.

### Option B: Manual Setup

If you prefer manual configuration:

#### 1. Clone the Repository

```bash
git clone https://github.com/your-org/claude-adlc-framework.git
cd claude-adlc-framework
```

#### 2. Make Scripts Executable

```bash
chmod +x scripts/*.sh
```

#### 3. Configure Your Data Stack

```bash
# Copy example configuration
cp config/repositories.json.example config/repositories.json

# Edit with your organization's repositories
# Replace 'your-org' with your GitHub organization name
# Update URLs to match your actual repository names
```

**Note**: `config/repositories.json` is git-ignored to keep organization-specific configuration private.

#### 4. (Optional) Configure dbt MCP Server

See `config/dbt-mcp-setup.md` for detailed setup instructions for all three authentication methods.

Quick option (Local .env):
```bash
# Copy environment template
cp .env.template .env

# Edit .env with your dbt Cloud credentials
# DBT_TOKEN, DBT_PROD_ENV_ID, etc.

# Install MCP server
npm install -g @modelcontextprotocol/server-dbt

# Configure Claude Desktop
# Edit ~/Library/Application Support/Claude/claude_desktop_config.json
# (See config/dbt-mcp-setup.md for complete configuration)
```

#### 5. Test the Installation

```bash
# Create your first idea
claude /capture "Test the Claude ADLC Framework setup"

# This should create a GitHub issue in your repository
```

## Available Commands

Once setup is complete, you have access to the ADLC workflow commands:

| Command | Purpose | Example |
|---------|---------|---------|
| `/capture` | Capture ideas as GitHub issues | `claude /capture "Build customer dashboard"` |
| `/research` | Deep analysis with specialist agents | `claude /research 123` |
| `/start` | Begin development from issue | `claude /start 123` |
| `/switch` | Context switching between projects | `claude /switch` |
| `/complete` | Finish and archive project | `claude /complete feature-project-name` |
| `/onboard` | Reconfigure your data stack and MCP servers | `claude /onboard` |

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

## MCP Integration

MCP (Model Context Protocol) servers provide real-time access to your data tools.

### Recommended Setup Method

Run the interactive onboarding for guided MCP configuration:
```bash
claude /onboard
```

This will walk you through:
- **dbt MCP Server**: Choose between .env, OAuth (local), or OAuth (remote)
- **Snowflake MCP Server**: Direct warehouse access (optional)
- **GitHub MCP Server**: Repository and issue management (optional)

### Manual Setup

For manual dbt MCP configuration, see:
- **Complete guide**: `config/dbt-mcp-setup.md`
- **Quick reference**: `.env.template`

The guide covers all three authentication options with step-by-step instructions.

## VS Code Worktree Integration (Optional)

For seamless project switching with isolated workspaces:

```bash
claude /setup-worktrees
```

This enables:
- Dedicated worktree per project
- Automatic VS Code workspace switching
- Clean context separation

See `knowledge/platform/development/vscode-worktree-integration.md` for details.

## First Project Workflow

```bash
# 1. Capture an idea
claude /capture "Analyze customer churn patterns"
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

- **Platform Documentation**: `knowledge/platform/README.md`
- **dbt MCP Setup**: `config/dbt-mcp-setup.md`
- **Git Workflows**: `.claude/memory/patterns/git-workflow-patterns.md`
- **Testing Patterns**: `.claude/memory/patterns/testing-patterns.md`

## Reconfiguration

Need to change your data stack or MCP servers?

```bash
# Run onboarding again to reconfigure
claude /onboard
```

The onboarding will detect your existing configuration and offer to update it.

---

**Ready to go!** Start with `./setup.sh` for interactive onboarding or `claude /capture "your first idea"` to begin.
