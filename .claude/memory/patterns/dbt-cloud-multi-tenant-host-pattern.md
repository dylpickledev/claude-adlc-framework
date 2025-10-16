# dbt Cloud Multi-Tenant Host Configuration Pattern

**Pattern Type:** Integration Configuration
**Confidence:** 0.95 (Production validated 2025-10-15)
**Last Updated:** 2025-10-15
**Related Agents:** dbt-expert, analytics-engineer-role

## Problem

dbt Cloud API calls fail with 401 "Invalid token" errors despite having valid credentials. This occurs when your dbt Cloud instance is hosted on a **multi-tenant deployment** rather than the default single-tenant cloud.getdbt.com host.

### Symptoms
- `401 Unauthorized` or "Invalid token header. No credentials provided" errors
- dbt-mcp tools fail silently with empty errors
- Direct API calls to `cloud.getdbt.com` fail
- Token is valid when tested on correct host

### Root Cause
dbt Cloud has multiple deployment architectures:
- **Single-tenant (default)**: `cloud.getdbt.com` or `{region}.dbt.com`
- **Multi-tenant**: `{instance}.us1.dbt.com` (e.g., `te240.us1.dbt.com`)

Most documentation and tools assume single-tenant hosting. If your instance is multi-tenant, API calls to the wrong host will fail authentication.

## Solution

### 1. Identify Your dbt Cloud Host

**Check your dbt Cloud URL when logged in:**
```
https://te240.us1.dbt.com/...     → Multi-tenant host: te240.us1.dbt.com
https://cloud.getdbt.com/...      → Single-tenant host: cloud.getdbt.com
https://emea.dbt.com/...          → Regional single-tenant host
```

**The subdomain before `.dbt.com` is your host identifier.**

### 2. Configure dbt-mcp with Custom Host

**For MCP server (scripts/launch-dbt-mcp.sh):**
```bash
# Set DBT_HOST explicitly BEFORE launching dbt-mcp
export DBT_HOST="te240.us1.dbt.com"  # Replace with YOUR instance host
export DBT_TOKEN="${DBT_CLOUD_API_TOKEN}"
export DBT_PROD_ENV_ID="${DBT_CLOUD_PROD_ENV_ID:-12333}"

uvx --python 3.12 dbt-mcp
```

**For direct API calls:**
```bash
# Use your specific host, not cloud.getdbt.com
curl -s "https://te240.us1.dbt.com/api/v2/accounts/{account_id}/..." \
  -H "Authorization: Token ${DBT_CLOUD_API_TOKEN}"
```

### 3. Update Launch Script (Permanent Fix)

**File:** `scripts/launch-dbt-mcp.sh`

```bash
#!/bin/bash
set -e

# Source 1Password secrets
if [ -f "$HOME/dotfiles/load-secrets-from-1password.sh" ]; then
    source "$HOME/dotfiles/load-secrets-from-1password.sh" 2>/dev/null || true
fi

# CRITICAL: Set host BEFORE launching dbt-mcp
# Multi-tenant instances use {instance}.us1.dbt.com format
export DBT_HOST="te240.us1.dbt.com"  # ← CUSTOMIZE THIS
export DBT_TOKEN="${DBT_CLOUD_API_TOKEN}"
export DBT_PROD_ENV_ID="${DBT_CLOUD_PROD_ENV_ID:-12333}"
export DBT_PATH="/usr/local/bin/dbt"

# Debug logging
echo "DEBUG: DBT_HOST=$DBT_HOST" >> /tmp/dbt-mcp-debug.log

# Launch with Python 3.12 (Python 3.13 has asyncio stdio bug)
uvx --python 3.12 dbt-mcp
```

### 4. Restart Claude Code

**CRITICAL:** After updating the launch script, you MUST fully restart Claude Code:
1. Quit Claude Code completely (not just close chat)
2. Relaunch Claude Code
3. MCP servers reconnect on launch with new configuration

**Why restart is required:**
- MCP servers connect when Claude Code starts, not when chat sessions start
- Killing/restarting dbt-mcp process alone won't work
- Claude Code maintains connection to original process
- Full restart forces MCP reconnection

## Verification

### Test MCP Connection
```bash
# After restart, test dbt-mcp tools
claude mcp list  # Should show "dbt-mcp: ✓ Connected"
```

### Test Direct API Call
```bash
# Verify host configuration
TOKEN="${DBT_CLOUD_API_TOKEN}"
curl -s "https://te240.us1.dbt.com/api/v2/accounts/2672/jobs/" \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool | head -20

# Should return JSON with job list, not 401 error
```

### Check Debug Logs
```bash
tail -10 /tmp/dbt-mcp-debug.log

# Should show:
# DEBUG: DBT_HOST=te240.us1.dbt.com
# (Not cloud.getdbt.com)
```

## Prevention

### 1. Document Your Instance Type
Add to project documentation:
```markdown
## dbt Cloud Configuration
- **Instance Type:** Multi-tenant
- **Host:** te240.us1.dbt.com
- **Account ID:** 2672
- **Region:** US East (us1)
```

### 2. Update Agent Knowledge
Add to `.claude/agents/specialists/dbt-expert.md`:
```markdown
## Known Patterns

### dbt Cloud Multi-Tenant Configuration
**Confidence:** 0.95 (Production validated)
**Pattern:** GraniteRock uses multi-tenant dbt Cloud (te240.us1.dbt.com)
**Reference:** `.claude/memory/patterns/dbt-cloud-multi-tenant-host-pattern.md`
```

### 3. Add to Onboarding Checklist
When setting up new developers:
- [ ] Identify dbt Cloud host from login URL
- [ ] Update `scripts/launch-dbt-mcp.sh` with correct DBT_HOST
- [ ] Test API connection before troubleshooting
- [ ] Document instance type in team docs

## Related Patterns

- **MCP Server Addition Protocol:** `.claude/memory/patterns/mcp-server-addition-protocol.md`
- **Agent MCP Integration:** `.claude/memory/patterns/agent-mcp-integration-guide.md`
- **Testing Patterns:** `.claude/memory/patterns/testing-patterns.md`

## Common Pitfalls

### ❌ Assuming cloud.getdbt.com Works for All Instances
**Wrong:**
```bash
export DBT_HOST="cloud.getdbt.com"  # Only works for single-tenant
```

**Right:**
```bash
# Check your login URL first, then set accordingly
export DBT_HOST="te240.us1.dbt.com"  # Multi-tenant instance
```

### ❌ Restarting MCP Process Without Restarting Claude
**Wrong:**
```bash
pkill dbt-mcp
bash scripts/launch-dbt-mcp.sh  # Claude still connected to OLD process
```

**Right:**
```bash
# Update launch script, then fully quit/restart Claude Code
```

### ❌ Testing with Wrong curl Syntax
**Wrong:**
```bash
# Bash can mangle Authorization header with certain variable expansions
curl -H "Authorization: Token $TOKEN"  # May fail unpredictably
```

**Right:**
```bash
# Use explicit variable assignment or Python for testing
TOKEN="${DBT_CLOUD_API_TOKEN}"
curl -H "Authorization: Token $TOKEN"
```

## Success Metrics

After applying this pattern:
- ✅ dbt-mcp tools work without authentication errors
- ✅ Direct API calls return valid JSON (not 401)
- ✅ Debug logs show correct host configuration
- ✅ MCP server shows "✓ Connected" in `claude mcp list`

## Production Validation

**Validated:** 2025-10-15
**Instance:** GraniteRock dbt Cloud (te240.us1.dbt.com)
**Outcome:** Fixed persistent 401 errors, enabled all dbt-mcp tools
**Time to Resolution:** ~30 minutes (would be 5 minutes with this pattern)
