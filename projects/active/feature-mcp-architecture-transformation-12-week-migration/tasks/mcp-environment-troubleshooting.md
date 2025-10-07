# MCP Environment Setup & Troubleshooting

**Created:** 2025-10-06
**Purpose:** Document MCP server environment variable timing issues and solutions

## Problem: MCP Servers Can't Access Environment Variables

### Symptoms
- `claude mcp list` shows limited or failed servers
- MCP servers configured in `.claude/mcp.json` fail to connect
- Environment variables work in terminal but not in Claude Code
- Errors like "Cannot access credentials" or "Authentication failed"

### Root Cause: Process Environment vs Shell Environment

**The Issue:**
1. Claude Code starts MCP servers at **application launch**
2. MCP server processes inherit environment from Claude's parent process
3. Shell startup files (`.zshrc`) only load in **terminal sessions**
4. Environment variables set in `.zshrc` are NOT available to GUI-launched apps

**The Timing Problem:**
```
GUI Launch (Dock/Spotlight)
  ↓
Claude Code starts (inherits system environment)
  ↓
MCP servers start (use ${VAR} from mcp.json)
  ↓❌ Variables from .zshrc NOT available yet

Terminal Launch
  ↓
.zshrc loads → sources 1Password script
  ↓
Environment variables set
  ↓✅ Variables available in shell, but TOO LATE for MCP servers
```

## Solution: Use `.zshenv` for System-Wide Environment

### Why `.zshenv`?
- Loaded for **ALL** zsh sessions (interactive + non-interactive)
- Loaded **before** login shells, GUI apps, and interactive terminals
- Perfect for credentials that need to be available system-wide

### Implementation

**Step 1: Create `~/.zshenv`**
```bash
#!/bin/zsh
# .zshenv - Loaded for ALL zsh sessions (interactive and non-interactive)
# This ensures environment variables are available to applications launched from GUI (Dock, Spotlight)
# including Claude Code and its MCP servers

# Load 1Password secrets for DA Agent Hub
# This runs before .zshrc, ensuring credentials are available system-wide
if [ -f "$HOME/dotfiles/load-secrets-from-1password.sh" ]; then
    source "$HOME/dotfiles/load-secrets-from-1password.sh" 2>/dev/null
fi
```

**Step 2: Fix `load-secrets-from-1password.sh`**

Ensure all fields use `--reveal` flag (not just credentials):
```bash
# Before (BROKEN - shows 1Password reference instead of value)
export SLACK_TEAM_ID=$(op item get "DA Agent Hub - Slack Bot Token" --vault="$VAULT" --fields label=team_id 2>/dev/null || echo "")

# After (FIXED - shows actual value)
export SLACK_TEAM_ID=$(op item get "DA Agent Hub - Slack Bot Token" --vault="$VAULT" --fields label=team_id --reveal 2>/dev/null || echo "")
```

**Step 3: Restart Claude Code**

Environment variables are inherited at process start. After creating `.zshenv`, you MUST restart Claude Code:
1. Save all work
2. Quit Claude Code completely
3. Relaunch from Dock/Spotlight
4. MCP servers will now have access to credentials

### Verification

**Test 1: Check environment variables in terminal**
```bash
source ~/.zshenv
echo $SLACK_BOT_TOKEN
echo $SLACK_TEAM_ID
echo $GITHUB_PERSONAL_ACCESS_TOKEN
```

**Test 2: Check MCP server status**
```bash
claude mcp list
```

Should show all configured servers with connection status.

**Test 3: Verify credentials in 1Password**
```bash
op item get "DA Agent Hub - Slack Bot Token" --vault=GRC --reveal
op item get "DA Agent Hub - GitHub PAT" --vault=GRC --reveal
```

## MCP Configuration Pattern

Use environment variable references in `.claude/mcp.json`:
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      },
      "disabled": false
    }
  }
}
```

**Key Points:**
- Use `${VARIABLE_NAME}` syntax - Claude interpolates at startup
- Variables MUST exist in parent process environment
- DO NOT hardcode credentials in mcp.json (security violation)

## Alternative Solutions (Not Recommended)

### Option B: Restart Claude After Shell Init
- Load secrets in terminal → restart Claude from that terminal
- **Pro**: No config changes needed
- **Con**: Manual restart required every session, not automated

### Option C: launchctl setenv (macOS specific)
```bash
launchctl setenv SLACK_BOT_TOKEN "xoxb-..."
launchctl setenv SLACK_TEAM_ID "T..."
```
- **Pro**: System-wide immediately
- **Con**: Requires manual setup for each variable, not version controlled

## Best Practices

1. **Never commit credentials** - Use environment variables + 1Password
2. **Use .zshenv for system-wide vars** - Ensures GUI apps can access them
3. **Use .zshrc for interactive shells** - Keeps prompts, aliases, functions separate
4. **Restart after environment changes** - Processes inherit environment at launch
5. **Test in fresh terminal** - Ensures setup works for new sessions

## Related Files
- **Setup**: `~/.zshenv` (this file loads secrets)
- **Credentials**: `~/dotfiles/load-secrets-from-1password.sh`
- **MCP Config**: `/Users/TehFiestyGoat/da-agent-hub/da-agent-hub/.claude/mcp.json`
- **1Password Items**: See GRC vault in 1Password desktop app

## Troubleshooting Commands

```bash
# Reload environment in current shell
source ~/.zshenv

# Check if 1Password CLI is authenticated
op vault list

# List all MCP-related environment variables
env | grep -E "(SLACK|GITHUB|AWS|DBT|SNOWFLAKE)"

# Test MCP server manually (Slack example)
SLACK_BOT_TOKEN="$SLACK_BOT_TOKEN" SLACK_TEAM_ID="$SLACK_TEAM_ID" npx -y @modelcontextprotocol/server-slack
```

## Success Metrics
- ✅ `claude mcp list` shows all 10+ servers
- ✅ All MCP servers connect successfully (no failures)
- ✅ Environment variables available in fresh terminal
- ✅ Claude Code can use MCP tools without authentication errors
- ✅ Specialist agents can delegate to MCP servers

---

**Status:** Week 1 Day 4 - Environment setup complete, pending Claude restart
