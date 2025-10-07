# MCP Environment Setup Summary

**Date:** 2025-10-06
**Phase:** Week 1 Day 4
**Status:** Complete - Pending Claude Code restart

## Problem Solved

MCP servers configured in `.claude/mcp.json` could not access environment variables when Claude Code was launched from GUI (Dock/Spotlight), causing authentication failures.

## Root Cause

**Environment Variable Timing Issue:**
- Shell startup files (`.zshrc`) only execute in terminal sessions
- Claude Code launches from GUI, inheriting system environment (NOT shell environment)
- MCP servers start at Claude Code launch, before shell loads secrets
- Result: `${SLACK_BOT_TOKEN}` references in mcp.json resolve to empty strings

## Solution Implemented

### 1. Created `~/.zshenv` (System-Wide Environment)

**File:** `~/.zshenv`
**Location:** `/Users/TehFiestyGoat/.zshenv`
**Purpose:** Load 1Password secrets for ALL zsh sessions (interactive + non-interactive)

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

**Key Benefits:**
- Loaded before `.zshrc` (earlier in zsh initialization)
- Loaded for non-interactive shells (GUI app launches)
- Makes credentials available to Claude Code at startup

### 2. Enhanced `load-secrets-from-1password.sh`

**Changes Made:**

**a) Added 24-Hour Caching**
```bash
CACHE_FILE="$HOME/.da-agent-hub-secrets-cache"
CACHE_DURATION_SECONDS=$((24 * 60 * 60))  # 24 hours

# Check if cache exists and is fresh
if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -f %m "$CACHE_FILE")))
    if [ $CACHE_AGE -lt $CACHE_DURATION_SECONDS ]; then
        source "$CACHE_FILE"
        return 0
    fi
fi
```

**Benefits:**
- Reduces 1Password API calls from ~12 per shell to 1 per day
- Shell startup improvement: ~500ms when cached
- Auto-refreshes every 24 hours
- Secure: cache file has 600 permissions, gitignored

**b) Fixed `SLACK_TEAM_ID` Loading**
```bash
# Before (BROKEN)
export SLACK_TEAM_ID=$(op item get "..." --fields label=team_id 2>/dev/null)

# After (FIXED)
export SLACK_TEAM_ID=$(op item get "..." --fields label=team_id --reveal 2>/dev/null)
```

Added `--reveal` flag to get actual value instead of 1Password reference.

### 3. Updated `.gitignore`

Added cache file to dotfiles `.gitignore`:
```
.da-agent-hub-secrets-cache
```

Ensures cached credentials are never committed.

## Files Created/Modified

### Created
1. **`~/.zshenv`** - System-wide environment loader (not in git)
2. **`~/.da-agent-hub-secrets-cache`** - Cached secrets (gitignored, auto-generated)
3. **`tasks/mcp-environment-troubleshooting.md`** - Comprehensive troubleshooting guide
4. **`tasks/environment-setup-summary.md`** - This file

### Modified (Dotfiles Repo)
1. **`~/dotfiles/load-secrets-from-1password.sh`** - Added caching + fixed SLACK_TEAM_ID
2. **`~/dotfiles/.gitignore`** - Added cache file
3. **`~/dotfiles/claude/CLAUDE.md`** - Added credential management best practices

**Commits:**
- `feat: Add 24-hour caching to 1Password secrets loading` (bb332c4)
- `docs: Add credential management best practices to CLAUDE.md` (abe9d5e)

## Environment Variables Verified

All critical MCP credentials confirmed loaded:

```bash
✅ DBT_CLOUD_API_TOKEN (dbt-mcp)
✅ DBT_CLOUD_ACCOUNT_ID (dbt-mcp)
✅ DBT_PROJECT_DIR (dbt-mcp)
✅ GITHUB_PERSONAL_ACCESS_TOKEN (github-mcp)
✅ AWS_ACCESS_KEY_ID (aws-api-mcp)
✅ AWS_SECRET_ACCESS_KEY (aws-api-mcp)
✅ AWS_REGION (aws-api-mcp)
✅ SNOWFLAKE_ACCOUNT (snowflake-mcp)
✅ SNOWFLAKE_USER (snowflake-mcp)
✅ SNOWFLAKE_PASSWORD (snowflake-mcp)
✅ SNOWFLAKE_DATABASE (snowflake-mcp)
✅ SNOWFLAKE_WAREHOUSE (snowflake-mcp)
✅ SLACK_BOT_TOKEN (slack-mcp) - NEW
✅ SLACK_TEAM_ID (slack-mcp) - NEW (fixed)
```

## MCP Server Status

**Before Fix:**
- `claude mcp list` showed 2 servers (dbt-mcp, freshservice-mcp)
- Both failed to connect
- Other servers not listed

**After Fix (Expected after restart):**
- All 10 configured servers should appear
- All should connect successfully
- Credentials available via `${VAR}` interpolation

**Configured Servers:**
1. dbt-mcp
2. snowflake-mcp
3. aws-api
4. aws-docs
5. aws-knowledge
6. github
7. slack (NEW)
8. git
9. filesystem
10. sequential-thinking

## Next Steps

### REQUIRED: Restart Claude Code

**Why:**
- Processes inherit environment at launch
- `.zshenv` changes only apply to NEW processes
- Claude Code must restart to load new environment

**Steps:**
1. Save all work
2. Quit Claude Code completely (Cmd+Q)
3. Relaunch Claude Code from Dock or Spotlight
4. Verify MCP servers initialize

### After Restart Testing

```bash
# 1. Check MCP server status
claude mcp list

# Expected: All 10 servers shown with connection status

# 2. Verify environment variables
env | grep -E "(SLACK|GITHUB|AWS|DBT|SNOWFLAKE)"

# Expected: All credentials present

# 3. Test specialist agents
# Use dbt-expert, snowflake-expert, aws-expert
# Verify they can call MCP tools successfully
```

## Success Metrics

- ✅ `.zshenv` created and loads secrets system-wide
- ✅ 24-hour caching implemented and tested
- ✅ All environment variables verified in shell
- ✅ Dotfiles changes committed and pushed
- ⏳ Claude Code restart (USER ACTION REQUIRED)
- ⏳ MCP servers connect successfully after restart
- ⏳ Specialist agents can use MCP tools
- ⏳ Delegation patterns validated end-to-end

## Related Documentation

- **Troubleshooting:** `tasks/mcp-environment-troubleshooting.md`
- **MCP Config:** `.claude/mcp.json`
- **1Password Script:** `~/dotfiles/load-secrets-from-1password.sh`
- **Environment File:** `~/.zshenv`

---

**Week 1 Day 4 Status:** Environment setup complete ✅
**Next:** Restart Claude Code → Test MCP servers → Week 1 Day 5 validation
