# MCP Troubleshooting Runbook

**Pattern Type:** Operational Runbook
**Confidence:** 1.0 (Production validated)
**Last Updated:** 2025-10-15
**Purpose:** Comprehensive troubleshooting guide for all MCP server issues

## Critical Rule

**When Claude says an MCP is working, it MUST work.** This runbook ensures we can quickly diagnose and fix any MCP issues so tools remain reliable.

## Quick Diagnosis Flow

```
MCP tool failing?
    ↓
1. Run: ./scripts/check-mcp-health.sh
    ↓
2. Is server showing "✗ Failed"?
    YES → See Server-Specific Troubleshooting (below)
    NO → See Tool-Specific Issues (below)
    ↓
3. Check debug log: tail /tmp/{server}-mcp-debug.log
    ↓
4. Apply fix from patterns below
    ↓
5. Restart Claude Code (full quit + relaunch)
    ↓
6. Verify: ./scripts/check-mcp-health.sh
```

## Session Startup Protocol

**MANDATORY at start of EVERY Claude Code session**:

```bash
./scripts/check-mcp-health.sh
```

**Expected output**:
- ✓ 8/9 servers connected
- ⚠ snowflake-mcp (known issue)

**If ANY unexpected failures**: Stop and troubleshoot before proceeding with user tasks.

## Server-Specific Troubleshooting

### dbt-mcp

**Symptoms**:
- Tool calls return 401 errors
- Empty responses from tools
- "Invalid token" messages

**Root Causes & Fixes**:

#### 1. Wrong Host Configuration (Multi-Tenant)
**Problem**: Using `cloud.getdbt.com` instead of `te240.us1.dbt.com`
**Diagnosis**:
```bash
tail /tmp/dbt-mcp-debug.log | grep DBT_HOST
# Should show: DBT_HOST=te240.us1.dbt.com
# NOT: DBT_HOST=cloud.getdbt.com
```

**Fix**:
```bash
# Edit scripts/launch-dbt-mcp.sh
# Line 18 should be:
export DBT_HOST="te240.us1.dbt.com"

# Restart Claude Code (full quit + relaunch)
```

**Reference**: `.claude/memory/patterns/dbt-cloud-multi-tenant-host-pattern.md`

#### 2. Missing/Invalid API Token
**Problem**: DBT_CLOUD_API_TOKEN not loaded or expired
**Diagnosis**:
```bash
echo "Token length: ${#DBT_CLOUD_API_TOKEN}"
# Should be: 55 characters
# If 0: Token not loaded
```

**Fix**:
```bash
# Reload 1Password secrets
source ~/dotfiles/load-secrets-from-1password.sh

# Verify token loaded
echo "Token starts with: ${DBT_CLOUD_API_TOKEN:0:4}"
# Should show: dbtu

# If still failing, regenerate token in dbt Cloud UI
```

#### 3. MCP Connection Lost
**Problem**: dbt-mcp process died or Claude lost connection
**Diagnosis**:
```bash
ps aux | grep dbt-mcp | grep -v grep
# Should show running process
# If empty: Process died
```

**Fix**:
```bash
# Kill existing process (if any)
pkill -f dbt-mcp

# Restart Claude Code completely
# MCP servers connect on launch, not during session
```

### orchestra-mcp

**Symptoms**:
- Connection failures
- "Failed to connect" in health check
- Tool calls timeout

**Root Causes & Fixes**:

#### 1. Local Development Server Path Issue
**Problem**: Can't find local orchestra-mcp source
**Diagnosis**:
```bash
ls -la projects/active/feature-build-orchestra-mcp-server-*/src/orchestra_mcp/
# Should exist
# If not: Project directory missing or renamed
```

**Fix**:
```bash
# Verify project directory exists
ORCHESTRA_DIR="projects/active/feature-build-orchestra-mcp-server-enable-ai-agents-to-interact-with-orchestra-orchestration-platform-via-mcp-provides-tools-for-querying-pipeline-runs-task-runs-artifacts-and-triggering-pipelines-follows-dbtmcp-pattern-using-fastmcp-framework"
cd "$ORCHESTRA_DIR" || echo "Directory not found!"

# Check pyproject.toml exists
ls -l pyproject.toml
```

#### 2. Orchestra API Key Invalid
**Problem**: ORCHESTRA_API_KEY missing or expired
**Diagnosis**:
```bash
tail /tmp/orchestra-mcp-debug.log
# Check for: "ORCHESTRA_API_KEY is set: yes"
# If no: Key not loaded
```

**Fix**:
```bash
# Reload 1Password secrets
source ~/dotfiles/load-secrets-from-1password.sh

# Verify key loaded
echo "Key length: ${#ORCHESTRA_API_KEY}"
# Should be > 0
```

### snowflake-mcp

**Status**: ⏸️ KNOWN ISSUE - Connection failing
**Symptoms**: Always shows "✗ Failed to connect"

**Current Workarounds**:
1. Use `scripts/debug-snowflake.sh` for direct Snowflake queries
2. Use Snowflake web UI for manual queries
3. Fix planned but deferred (lower priority than other MCPs)

**Diagnostic Commands**:
```bash
tail /tmp/snowflake-mcp-debug.log
# Check for authentication errors
```

**Note**: Do NOT block user work on Snowflake MCP failure - it's a known issue.

### aws-api & aws-docs

**Symptoms**:
- Connection failures
- Permission errors
- Tool calls fail

**Root Causes & Fixes**:

#### 1. AWS Credentials Not Configured
**Problem**: ~/.aws/credentials missing or invalid
**Diagnosis**:
```bash
aws sts get-caller-identity
# Should return account info
# If error: Credentials not configured
```

**Fix**:
```bash
# Configure AWS credentials
aws configure

# Or check 1Password for AWS credentials
# Store in ~/.aws/credentials
```

#### 2. Wrong Region
**Problem**: Resources in different region than us-west-2
**Diagnosis**: Check .mcp.json for AWS_REGION setting

**Fix**:
```json
// In .mcp.json
"aws-api": {
  "env": {
    "AWS_REGION": "us-west-2"  // Change if needed
  }
}
```

### github

**Symptoms**:
- 401/403 authentication errors
- "Bad credentials" messages
- Rate limiting errors

**Root Causes & Fixes**:

#### 1. Missing/Invalid GitHub PAT
**Problem**: GITHUB_PERSONAL_ACCESS_TOKEN not loaded
**Diagnosis**:
```bash
echo "Token length: ${#GITHUB_PERSONAL_ACCESS_TOKEN}"
# Should be > 0
```

**Fix**:
```bash
# Reload 1Password secrets
source ~/dotfiles/load-secrets-from-1password.sh

# Verify scopes in 1Password:
# - repo
# - read:org
# - read:project
```

#### 2. Rate Limiting
**Problem**: Too many API calls
**Diagnosis**: GitHub returns "rate limit exceeded"

**Fix**:
```bash
# Wait for rate limit to reset (1 hour)
# Or use authenticated requests (higher limit)
# Check: https://api.github.com/rate_limit
```

### slack

**Symptoms**:
- Can't list channels
- Can't post messages
- "invalid_auth" errors

**Root Causes & Fixes**:

#### 1. Invalid Slack Bot Token
**Problem**: SLACK_BOT_TOKEN expired or wrong
**Diagnosis**:
```bash
echo "Token starts: ${SLACK_BOT_TOKEN:0:4}"
# Should start with: xoxb
```

**Fix**:
```bash
# Reload 1Password
source ~/dotfiles/load-secrets-from-1password.sh

# Verify team ID
echo "Team ID: $SLACK_TEAM_ID"
# Should be: TSQABERKL (GraniteRock)
```

#### 2. Insufficient Bot Scopes
**Problem**: Bot lacks required permissions
**Required Scopes**:
- `channels:read`
- `chat:write`
- `users:read`

**Fix**: Update bot in Slack admin UI, regenerate token

## Tool-Specific Issues

### Problem: MCP Server Shows "Connected" But Tools Fail

**Diagnosis Pattern**:
```bash
# 1. Verify connection
claude mcp list | grep {server}
# Shows: ✓ Connected

# 2. Try actual tool call
# Still fails → Authentication or configuration issue

# 3. Check debug log for actual error
tail -50 /tmp/{server}-mcp-debug.log
```

**Common Causes**:
1. **Wrong API endpoint**: Server connects but uses wrong host (dbt-mcp example)
2. **Invalid credentials**: Server starts but API rejects requests
3. **Missing environment variables**: Server runs but doesn't have required config

**Fix Pattern**:
1. Check launch script for correct configuration
2. Verify all environment variables are set and exported
3. Test API directly (curl/Python) to isolate MCP vs API issue
4. Restart Claude Code after any launch script changes

### Problem: Empty/Null Responses from MCP Tools

**Diagnosis**:
```python
# Call returns successfully but data is empty
result = mcp__dbt-mcp__list_jobs()
# Returns: {} or None
```

**Common Causes**:
1. **Authentication silent failure**: API returns empty instead of error
2. **Wrong account ID**: Querying wrong dbt Cloud account
3. **Permissions issue**: Token lacks required permissions

**Fix Pattern**:
1. Test same API call with curl/Python directly
2. Verify account IDs, environment IDs in configuration
3. Check token permissions in service UI
4. Compare working curl command vs MCP configuration

### Problem: Timeout Errors

**Symptoms**: "Request timed out" or long waits then failure

**Common Causes**:
1. **Large dataset**: Querying all models in huge dbt project
2. **Network issues**: Slow connection to cloud APIs
3. **Server overload**: Too many concurrent MCP requests

**Fixes**:
- Use selective queries (not `get_all_models()`)
- Add pagination to large requests
- Check network connection
- Restart Claude Code if MCP server is hung

## Restart Protocol

**When to fully restart Claude Code**:
- After ANY launch script changes
- After MCP configuration changes in .mcp.json
- After killing/restarting MCP processes
- When MCP connection is lost mid-session

**How to restart properly**:
1. **Quit Claude Code completely** (Cmd+Q or equivalent)
2. **Wait 5 seconds** (ensure all processes terminate)
3. **Relaunch Claude Code** (MCP servers reconnect on launch)
4. **Verify**: Run `./scripts/check-mcp-health.sh`

**DO NOT**:
- Just close the chat window
- Kill MCP processes without restarting Claude
- Assume restarting chat session = restarting MCPs

## Prevention Checklist

**Before claiming "MCP is working"**:
- [ ] Run `./scripts/check-mcp-health.sh` - all expected servers ✓
- [ ] Actually CALL at least one tool from the MCP
- [ ] Verify tool returns expected data (not empty/error)
- [ ] Check debug log shows correct configuration
- [ ] Document any gotchas discovered

**Before deploying MCP changes**:
- [ ] Test launch script manually
- [ ] Verify environment variables are set
- [ ] Check debug log for errors
- [ ] Test with actual tool calls
- [ ] Document configuration in mapping document
- [ ] Update this runbook with any new patterns

## Escalation Path

**If troubleshooting fails after 30 minutes**:

1. **Document what you tried**:
   - Commands run
   - Error messages
   - Debug log output
   - Configuration checked

2. **Create fallback approach**:
   - Direct API calls (curl/Python)
   - Alternative tools
   - Manual queries

3. **Continue user work**:
   - Don't block on MCP issues
   - Use workarounds
   - Document MCP issue for later fix

4. **Create improvement issue**:
   - Document problem
   - Proposed fix
   - Testing plan

## Success Metrics

**Healthy MCP ecosystem**:
- ✅ Health check passes at session start
- ✅ All tools return expected data
- ✅ No 401/403 authentication errors
- ✅ Response times < 10 seconds
- ✅ Debug logs show correct configuration

**Problem indicators**:
- ❌ Repeated health check failures
- ❌ Empty responses from tools
- ❌ Frequent "retry" or "timeout" messages
- ❌ Authentication errors after credential reload
- ❌ Same problem recurring across sessions

## Related Documentation

- **MCP Server Mapping**: `.claude/memory/patterns/mcp-server-specialist-mapping.md`
- **dbt Multi-Tenant**: `.claude/memory/patterns/dbt-cloud-multi-tenant-host-pattern.md`
- **MCP Addition Protocol**: `.claude/memory/patterns/mcp-server-addition-protocol.md`
- **GitHub Repo Resolution**: `.claude/memory/patterns/github-repo-context-resolution.md`

## Contribution Protocol

**When you discover a new MCP issue**:
1. Add it to this runbook under appropriate section
2. Include symptoms, diagnosis, and fix
3. Reference any related patterns
4. Update last modified date
5. Commit with message: `docs: Add MCP troubleshooting pattern for {issue}`

**This runbook is living documentation** - keep it current!
