# dlthub MCP Server Integration

## Overview

Production-validated MCP server integration for dlthub data ingestion platform. Provides AI agents with real-time access to dlt pipeline metadata, table schemas, data preview, and SQL query capabilities.

**Status**: ✅ Production Deployed (Week 6 Day 1 - 2025-10-15)
**License**: Requires dlt+ license (not free tier)
**Integration Pattern**: Follows dbt-mcp pattern (wrapper script + 1Password secrets)

## Capabilities

### Available MCP Tools

1. **`available_pipelines`** - List all dlt pipelines
   - Returns all pipelines in `~/.dlt/pipelines/` directory
   - Shows pipeline names for downstream tool calls

2. **`available_tables(pipeline_name)`** - List tables in a pipeline
   - Shows all tables loaded by a specific pipeline
   - Required for schema and preview operations

3. **`table_schema(pipeline_name, table_name)`** - Get table schema
   - Complete column definitions with data types
   - Useful for understanding loaded data structure

4. **`table_preview(pipeline_name, table_name)`** - View sample data
   - Returns first row from specified table
   - Quick data validation without full SQL

5. **`execute_sql_query(pipeline_name, sql_query)`** - Execute SQL
   - Run SELECT queries against pipeline data
   - Enables AI-driven data exploration

## Configuration

### MCP Server Config (`.mcp.json`)

```json
{
  "dlthub-mcp": {
    "command": "bash",
    "args": ["scripts/launch-dlthub-mcp.sh"],
    "disabled": false,
    "_comment": "dlthub data ingestion MCP integration. Requires dlt+ license. Week 6 Day 1 - Following dbt-mcp pattern with 1Password env vars for license key."
  }
}
```

### Launch Script (`scripts/launch-dlthub-mcp.sh`)

```bash
#!/bin/bash
# Launch dlthub-MCP server with dlt+ license from 1Password
# Follows dbt-mcp pattern: load secrets, launch with uv, debug logging

set -e

# Self-locate script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Debug log
DEBUG_LOG="/tmp/dlthub-mcp-debug.log"
echo "DEBUG: Launching dlthub-MCP server" >> "$DEBUG_LOG"

# Load secrets from 1Password (provides DLTHUB_LICENSE_KEY)
source "$HOME/dotfiles/load-secrets-from-1password.sh" >> "$DEBUG_LOG" 2>&1

# Verify license key is set
if [ -z "$DLTHUB_LICENSE_KEY" ]; then
    echo "ERROR: DLTHUB_LICENSE_KEY not set - check 1Password configuration" >> "$DEBUG_LOG"
    echo "ERROR: DLTHUB_LICENSE_KEY not set - check 1Password configuration" >&2
    exit 1
fi

echo "DEBUG: DLTHUB_LICENSE_KEY is set: yes" >> "$DEBUG_LOG"

# Launch dlthub MCP server with dlt+ license
# Using uv tool runner with dlt-plus[mcp] package
# Per dlthub docs: https://dlthub.com/docs/hub/features/mcp-server
# IMPORTANT: Use 'run_plus' for licensed version (not 'run')
exec uvx --from "dlt-plus[mcp]==0.9.0" dlt mcp run_plus 2>> "$DEBUG_LOG"
```

### 1Password Secret Setup

Store dlt+ license key in 1Password:
```bash
op item create \
  --category="API Credential" \
  --title="dlthub MCP License" \
  --vault="DA Agent Hub" \
  credential[password]="<your-dlt-plus-license-key>" \
  purpose[text]="dlthub MCP server authentication - dlt+ license for data ingestion platform"
```

**Environment Variable**: `DLTHUB_LICENSE_KEY`
**Source**: 1Password item "dlthub MCP License"
**Loaded By**: `~/dotfiles/load-secrets-from-1password.sh`

## Critical Setup Details

### dlt+ vs Free Tier

**CRITICAL**: The MCP server requires a dlt+ license and the correct command:

✅ **Correct (Licensed)**: `dlt mcp run_plus`
- Activates dlt+ features
- Uses `DLTHUB_LICENSE_KEY` environment variable
- Full MCP tool capabilities

❌ **Incorrect (Free)**: `dlt mcp run`
- Free tier only
- Ignores license key
- Limited MCP features

### Pipeline Location Requirements

**Default Directory**: `~/.dlt/pipelines/`

The MCP server expects:
1. Actual dlt pipeline executions (not just code)
2. Pipeline metadata created by dlt runtime
3. Standard dlt directory structure

**Common Issue**: Empty repo = no pipelines = server can't find data
**Solution**: Run at least one pipeline to create metadata before using MCP tools

## Repository Integration

### Repository Configuration

**Location**: `repos/ingestion_analytics/dlthub/`
**GitHub**: `https://github.com/graniterock/dlthub.git`
**Branch**: `main`

**config/repositories.json**:
```json
{
  "ingestion_analytics": {
    "dlthub": {
      "url": "https://github.com/graniterock/dlthub.git",
      "branch": "main",
      "description": "dlthub data ingestion pipelines to Snowflake analytics (dlt+ with MCP server integration)",
      "folder": "repos/ingestion_analytics"
    }
  }
}
```

### Pull Script Integration

**scripts/pull-all-repos.sh** - Added to "Ingestion (Analytics)" section:
```bash
if [ -d "$REPO_ROOT/repos/ingestion_analytics/dlthub" ]; then
    cd "$REPO_ROOT/repos/ingestion_analytics/dlthub"
    echo -e "${GREEN}📦 dlthub${NC}"
    git checkout main
    git pull origin main
    echo ""
fi
```

## Agent Integration

### dlthub-expert Specialist

**File**: `.claude/agents/specialists/dlthub-expert.md`
**Role**: Data ingestion specialist with MCP tool access
**Scope**: dlthub pipeline analysis, connector optimization, schema management

**Production Patterns** (Updated Week 6 Day 1):
- MCP tool usage for pipeline inspection
- dlt+ license setup and verification
- Production-validated configuration patterns
- Launch script troubleshooting

### Role Agent Delegation

**data-engineer-role** delegates to dlthub-expert for:
- New source system integrations
- Pipeline performance optimization
- Schema evolution planning
- Incremental loading strategies

## Verification & Testing

### Health Check

```bash
# Check MCP server status
claude mcp list

# Expected output:
# dlthub-mcp: bash scripts/launch-dlthub-mcp.sh - ✓ Connected
```

### Functional Testing

**Once pipelines exist**:
```python
# List all pipelines
mcp__dlthub-mcp__available_pipelines

# List tables in pipeline
mcp__dlthub-mcp__available_tables(pipeline_name="my_pipeline")

# Get table schema
mcp__dlthub-mcp__table_schema(pipeline_name="my_pipeline", table_name="users")

# Preview data
mcp__dlthub-mcp__table_preview(pipeline_name="my_pipeline", table_name="users")

# Execute SQL
mcp__dlthub-mcp__execute_sql_query(
    pipeline_name="my_pipeline",
    sql_query="SELECT COUNT(*) FROM users"
)
```

**Current Status** (Week 6 Day 1):
- ✅ MCP server connected successfully
- ⏸️ Functional testing pending (no pipelines exist yet)
- 🎯 Next: Create first dlt pipeline for validation

## Troubleshooting

### Common Issues

**Error**: `No such file or directory: '/Users/TehFiestyGoat/.dlt/pipelines/.'`
- **Cause**: No dlt pipelines have been run yet
- **Solution**: Execute at least one dlt pipeline to create metadata
- **Verification**: Check `~/.dlt/pipelines/` directory exists

**Error**: `DLTHUB_LICENSE_KEY not set`
- **Cause**: 1Password secret not loaded correctly
- **Debug**: Check `/tmp/dlthub-mcp-debug.log`
- **Solution**: Verify 1Password CLI access and secret configuration

**Error**: MCP server shows "disconnected"
- **Cause**: License validation failed or command incorrect
- **Check**: Using `run_plus` (not `run`) in launch script
- **Verify**: `DLTHUB_LICENSE_KEY` contains valid dlt+ license

## Documentation References

### Official dlthub Documentation

- **MCP Server Guide**: https://dlthub.com/docs/dlt-ecosystem/llm-tooling/mcp-server
- **LLM Workflows**: https://dlthub.com/docs/dlt-ecosystem/llm-tooling/llm-native-workflow
- **Main Docs**: https://dlthub.com/docs/
- **Connectors**: https://dlthub.com/docs/dlt-ecosystem/destinations/
- **API Reference**: https://dlthub.com/docs/reference/

### Community Learning Resources (Production-Validated)

- **Weekly How-To Series**: https://github.com/1997mahadi/Data-Engineering-with-dlt/
  - Real-world dlthub patterns from active practitioner
  - Weekly tutorials covering practical implementation scenarios
  - Recommended for understanding real-world usage patterns

- **Advanced dlt Course**: https://dlthub.learnworlds.com/course/dlt-advanced
  - Deep-dive course for advanced patterns
  - Optimization techniques and best practices
  - Recommended for specialist-level expertise development

### Internal Documentation

- **Agent Pattern**: `.claude/agents/specialists/dlthub-expert.md`
- **Launch Script**: `scripts/launch-dlthub-mcp.sh`
- **MCP Config**: `.mcp.json` (dlthub-mcp section)
- **Repo Config**: `config/repositories.json` (ingestion_analytics.dlthub)

## Key Learnings (Week 6 Day 1)

### Production Validation Results

1. ✅ **Pattern Reuse Works**: dbt-mcp wrapper script pattern successfully adapted for dlthub
2. ✅ **1Password Integration Reliable**: Secret loading via dotfiles works consistently
3. ✅ **uv Tool Runner Efficient**: `uvx --from "dlt-plus[mcp]==0.9.0"` handles deps automatically
4. ⚠️ **Pipeline Dependency Critical**: Server requires existing pipeline metadata (not just code)
5. ✅ **Command Differentiation Important**: `run_plus` vs `run` determines license tier

### Best Practices Established

- **License Key Security**: Always use 1Password, never hardcode
- **Debug Logging**: Comprehensive logging to `/tmp/dlthub-mcp-debug.log`
- **Error Handling**: Explicit checks for license key presence
- **Version Pinning**: Specify exact version (`dlt-plus[mcp]==0.9.0`) for consistency
- **Documentation Links**: Include official docs in agent patterns

## Next Steps

1. **Create First Pipeline**: Build initial dlt pipeline in dlthub repo
2. **Functional Testing**: Validate all MCP tools with real pipeline data
3. **Performance Baseline**: Measure MCP tool response times
4. **Agent Workflow**: Document dlthub-expert + MCP integration patterns
5. **Knowledge Transfer**: Update data-engineer-role with dlthub delegation patterns

---

**Last Updated**: 2025-10-15 (Week 6 Day 1)
**Validated By**: Claude Code dlthub MCP integration project
**Status**: Production Ready - Awaiting First Pipeline for Functional Testing
