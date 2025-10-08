# Snowflake MCP Fix Required (Network Policy)

**Created**: 2025-10-07
**Priority**: HIGH (blocks Snowflake queries via Claude)
**Status**: ⚠️ Waiting for network policy resolution

## What's Blocking

**Your Snowflake account has IP allowlisting** - local machine IP is not on the approved list.

**Error**: `250001 (08001): Network policy is required`

## Quick Fix (5 Minutes Active Work)

### Option A: Add Your IP to Snowflake Network Policy (Recommended)

**Step 1**: Get your current IP
```bash
curl ifconfig.me
```

**Step 2**: Contact Snowflake administrator (or run yourself if you have ACCOUNTADMIN):
```sql
-- As ACCOUNTADMIN in Snowflake
ALTER NETWORK POLICY <your_policy_name>
  SET ALLOWED_IP_LIST = ('existing.ips', '<your-ip-from-step-1>');
```

**Step 3**: Restart Claude Code to test
```bash
# Exit Claude Code, then relaunch
# Run: claude mcp list
# Expected: snowflake-mcp: ✓ Connected
```

### Option B: Use VPN (If Available)

If you have corporate VPN:
1. Connect to VPN
2. Verify VPN IP range is already allowlisted
3. Restart Claude Code
4. Test with `claude mcp list`

## What I Fixed Already

✅ **Updated `.claude/mcp.json`** to use wrapper script (proper Week 1 configuration)

**Before** (broken):
```json
"command": "uvx",
"args": ["snowflake-labs-mcp", "--service-config-file", "config/snowflake_tools_config.yaml"]
```

**After** (correct):
```json
"command": "bash",
"args": ["scripts/launch-snowflake-mcp.sh"]
```

## What Happens After You Fix Network Policy

**I'll be able to**:
1. Query Snowflake task failures via snowflake-expert
2. Analyze warehouse utilization via snowflake-expert
3. Optimize queries via snowflake-expert
4. Provide data-driven Snowflake recommendations (not guessing)

**snowflake-expert will use**:
- snowflake-mcp tools for real-time data
- Official Snowflake docs for best practices
- Production-validated patterns from Week 3-4 testing

## For Right Now (Manual Approach)

**To answer your original question**, run this in Snowflake UI:

```sql
-- Check for task failures in last 24 hours
SELECT
    NAME as task_name,
    DATABASE_NAME,
    SCHEMA_NAME,
    STATE,
    ERROR_CODE,
    ERROR_MESSAGE,
    SCHEDULED_TIME,
    COMPLETED_TIME
FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY
WHERE START_TIME >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
  AND STATE = 'FAILED'
ORDER BY SCHEDULED_TIME DESC;
```

**If query returns 0 rows**: All tasks healthy ✅
**If query returns rows**: Share results and I'll delegate to snowflake-expert for analysis

## Timeline

- **Config fix**: ✅ Done (committed)
- **Network policy fix**: ⏳ Requires your action (5 min + admin approval)
- **Testing & docs**: ⏳ After network policy fixed (30 min)

---

**Next step**: Fix network policy (add IP or use VPN), then we can properly test snowflake-mcp and document real capabilities.
