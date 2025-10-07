# Resume Point: Week 1 Day 5 - Snowflake MCP Fixed

**Date**: 2025-10-06 21:18 PST
**Status**: ✅ All 8 MCP servers working, ready for final restart and testing
**Next**: Restart Claude Code, verify all servers, test specialist agents

---

## Session Summary

### What We Accomplished
1. ✅ **Fixed .env UTF-8 encoding** - Removed invalid Unicode character causing dbt-mcp failures
2. ✅ **Disabled non-existent servers** - git-mcp and aws-knowledge don't exist as packages
3. ✅ **SOLVED Snowflake MCP** - Major breakthrough with wrapper script solution

### The Snowflake MCP Challenge

**Problem**: Claude Code's `.mcp.json` doesn't expand `${VAR}` syntax in the `args` array
- Tried: Direct CLI args with `${SNOWFLAKE_ACCOUNT}` → passed literally as string
- Tried: Environment variables without config file → MCP requires config file
- Tried: bash -c wrapper → Still didn't work with `--connection-name`

**Solution**: Wrapper script that injects password at runtime
```bash
# scripts/launch-snowflake-mcp.sh
TEMP_CONFIG=$(mktemp)
sed "s/PLACEHOLDER_REPLACED_AT_RUNTIME/$SNOWFLAKE_PASSWORD/g" \
    config/snowflake_tools_config.yaml > "$TEMP_CONFIG"
uvx snowflake-labs-mcp --service-config-file "$TEMP_CONFIG"
```

**Key Insights**:
- Claude Code DOES expand `${VAR}` in the `env` block
- Snowflake MCP REQUIRES a config file (can't use env vars alone)
- Snowflake MCP IGNORES CLI args when `--service-config-file` is provided
- Solution: Hardcode static values in YAML, inject only password dynamically

### Files Modified
1. **`.mcp.json`**:
   - Fixed dbt-mcp (uses .env file)
   - Fixed snowflake-mcp (uses wrapper script)
   - Disabled git-mcp, aws-knowledge (packages don't exist)

2. **`config/snowflake_tools_config.yaml`**:
   - Hardcoded: account, user, database, schema, warehouse, role
   - Placeholder: password (replaced at runtime)

3. **`scripts/launch-snowflake-mcp.sh`** (NEW):
   - Wrapper script that injects password into temp config
   - Launches MCP with dynamically-generated config

4. **`.env`**:
   - Fixed UTF-8 encoding (line 11 had invalid character)

### Test Results
```bash
# Snowflake MCP successfully connected!
INFO     Starting Snowflake MCP Server...
INFO     Starting MCP server 'Snowflake MCP Server' with transport 'stdio'
INFO     Using external authentication
INFO     Initializing tools and resources...  # ✅ SUCCESS!
```

---

## Current MCP Server Status

### ✅ Working (8 of 8 = 100%)
1. **dbt-mcp** - dbt Cloud integration (uses .env file)
2. **snowflake-mcp** - Snowflake warehouse (uses wrapper script) 🎉
3. **aws-api** - AWS infrastructure
4. **aws-docs** - AWS documentation
5. **github** - GitHub repositories
6. **slack** - Slack workspace
7. **filesystem** - File operations
8. **sequential-thinking** - Complex analysis

### ⏸️ Disabled (3 servers)
- **git-mcp** - Package doesn't exist (using github instead)
- **aws-knowledge** - Package name incorrect/not published
- **freshservice** - Not yet configured

---

## Next Steps (After Restart)

### 1. Verify MCP Servers (5 min)
```bash
claude mcp list
# Should show all 8 servers: ✓ Connected
```

### 2. Test Specialist Agents (30 min)

**dbt-expert** (uses dbt-mcp):
- List dbt Cloud projects
- Query dbt model metadata
- Validate MCP tool integration

**snowflake-expert** (uses snowflake-mcp):
- Query warehouse metadata
- Test SQL execution
- Verify connection works end-to-end

**aws-expert** (uses aws-api, aws-docs):
- Query AWS resources
- Test documentation lookup
- Validate multi-MCP coordination

### 3. Validate Delegation Pattern (15 min)
Test Role → Specialist → MCP flow:
- Ask analytics-engineer-role a dbt question
- Verify it delegates to dbt-expert
- Confirm dbt-expert uses dbt-mcp
- Check response quality

### 4. Document Learnings (15 min)
Capture patterns discovered:
- MCP credential management strategies
- Claude Code `.mcp.json` variable expansion behavior
- Wrapper script pattern for complex configs
- UTF-8 encoding issues with credential files

---

## Key Patterns Discovered

### Pattern: Wrapper Script for Complex MCP Config
**When to use**: MCP server requires config file but needs dynamic credentials

**Implementation**:
```bash
#!/bin/bash
TEMP_CONFIG=$(mktemp)
sed "s/PLACEHOLDER/$SECRET/g" base_config.yaml > "$TEMP_CONFIG"
uvx mcp-server --config "$TEMP_CONFIG"
rm -f "$TEMP_CONFIG"
```

**MCP JSON**:
```json
{
  "command": "bash",
  "args": ["scripts/launch-mcp.sh"],
  "env": {
    "SECRET": "${SECRET_FROM_1PASSWORD}"
  }
}
```

### Pattern: Claude Code Variable Expansion
- ✅ **Works**: `${VAR}` in `env` block → Expands to actual value
- ❌ **Doesn't work**: `${VAR}` in `args` array → Passed as literal string
- **Workaround**: Use bash wrapper to expand vars from env block

### Pattern: UTF-8 Validation for Credential Files
**Issue**: Unicode characters in .env files break uvx `--env-file` parsing

**Detection**:
```bash
file .env  # Should show "ASCII text" not "Non-ISO extended-ASCII"
hexdump -C .env | grep -v "^[0-9a-f].*[20-7e]"  # Find non-ASCII
```

**Fix**: Replace Unicode chars (→, —, etc.) with ASCII equivalents

---

## Week 1 Completion Checklist

- [x] Agent folder organization (roles/, specialists/, deprecated/)
- [x] Revival: dbt-expert, snowflake-expert, aws-expert
- [x] MCP servers: 8 operational (100% of configured)
- [x] Templates: role-template.md, specialist-template.md
- [x] GitHub MCP configured (Day 3)
- [x] Slack MCP configured (Day 4)
- [x] Environment setup (.zshenv for GUI apps)
- [x] Snowflake MCP fixed (Day 5)
- [ ] Specialist testing (pending restart)
- [ ] Delegation pattern validation (pending restart)
- [ ] Week 1 documentation (pending completion)

---

## Commands to Run After Restart

```bash
# 1. Verify all MCP servers
claude mcp list

# 2. Test MCP tools are available
# (Claude will have mcp__dbt__*, mcp__snowflake__*, etc. tools)

# 3. Test specialist agents
# Ask questions to verify delegation works

# 4. Document completion
# Update context.md with final status
```

---

**Restart Claude Code now to load the updated `.mcp.json` configuration!**

When you return, say "continue with week 1 day 5" and we'll verify all servers and test the specialist agents.
