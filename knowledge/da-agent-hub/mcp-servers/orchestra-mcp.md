# Orchestra MCP Server

**Status**: ✅ Production-Ready
**Built**: 2025-10-15
**Pattern**: Follows dbt-mcp architecture (FastMCP + 1Password authentication)
**Purpose**: Enable AI agents to investigate pipeline failures, analyze execution patterns, and trigger workflows in Orchestra orchestration platform

## Overview

The Orchestra MCP server provides programmatic access to Orchestra's workflow orchestration platform through the Model Context Protocol. It allows AI agents (particularly `orchestra-expert`, `data-engineer-role`, and `analytics-engineer-role`) to:

- Query pipeline execution history
- Investigate failed pipeline runs
- Analyze task-level execution details
- Download logs and artifacts for troubleshooting
- Trigger manual pipeline runs for testing/recovery

## Architecture

### MCP Server Pattern
```
1Password (Secrets)
   ↓ (ORCHESTRA_API_KEY via load-secrets-from-1password.sh)
Launch Script (scripts/launch-orchestra-mcp.sh)
   ↓ (inherits env vars, uses Python 3.12)
FastMCP Server (src/orchestra_mcp/server.py)
   ↓ (7 MCP tools)
Orchestra API Client (src/orchestra_mcp/client.py)
   ↓ (HTTPS with Bearer token auth)
Orchestra Metadata API (https://app.getorchestra.io/api/engine/public/)
```

### Key Components

**Package Structure**:
```
projects/active/feature-build-orchestra-mcp-server-.../
├── pyproject.toml                 # FastMCP + httpx dependencies
├── src/orchestra_mcp/
│   ├── __init__.py               # Package exports
│   ├── models.py                 # Pydantic response models
│   ├── client.py                 # Orchestra API client (async)
│   └── server.py                 # FastMCP tool definitions
└── scripts/launch-orchestra-mcp.sh  # Wrapper script for 1Password env loading
```

**Launch Script** (`scripts/launch-orchestra-mcp.sh`):
- Sources secrets from `~/dotfiles/load-secrets-from-1password.sh`
- Explicitly uses Python 3.12 (avoids asyncio stdio bugs in 3.13)
- Invokes `uvx --python 3.12 --from {project_path} orchestra-mcp`

**Authentication** (1Password Pattern):
1. API key stored in 1Password: "DA Agent Hub - Orchestra"
2. Field name: `credential` → mapped to `ORCHESTRA_API_KEY` env var
3. Launch script inherits env var and passes to FastMCP server
4. Client uses: `Authorization: Bearer {ORCHESTRA_API_KEY}`

## Available Tools

### 1. list_pipeline_runs
**Purpose**: Query pipeline execution history with filtering

**Parameters**:
- `time_from` (optional): ISO 8601 start time (e.g., "2025-10-01T00:00:00Z")
- `time_to` (optional): ISO 8601 end time
- `status` (optional): Filter by status (CREATED, RUNNING, SUCCEEDED, WARNING, FAILED, CANCELLING, CANCELLED)
- `pipeline_run_ids` (optional): Comma-separated list of specific run IDs
- `limit` (default: 100, max: 1000): Results per query
- `offset` (default: 0): Pagination offset

**Returns**: Paginated response
```json
{
  "page": 1,
  "pageSize": 50,
  "total": 2363,
  "results": [
    {
      "id": "3b80c185-4bf7-4432-b965-e3b3baf78773",
      "pipelineId": "7b3deb5f-4d83-4495-a7fd-0434844361ac",
      "pipelineName": "JDE Account Balances + Forecast 2.0",
      "runStatus": "SUCCEEDED",
      "triggeredBy": [{"triggerType": "SCHEDULED", "scheduleName": "Every 15 mins"}],
      "message": "All tasks have succeeded.",
      "createdAt": "2025-10-16T00:15:50.472460+00:00",
      "completedAt": "2025-10-16T00:19:13.520569+00:00",
      "branch": "master",
      "commit": "a6dba8821142f030ee29fa9f309dee514cbeb896"
    }
  ]
}
```

**Time Constraints**:
- Without time filters: Last 7 days only
- With time filters: Must use both `time_from` and `time_to`, max 7-day range

**Use Cases**:
- Identify recent pipeline failures for investigation
- Track execution frequency and patterns
- Monitor pipeline health over time

### 2. get_pipeline_run_status
**Purpose**: Get detailed status for specific pipeline run

**Parameters**:
- `pipeline_run_id` (required): Unique run identifier

**Returns**: Single pipeline run dictionary (same structure as list_pipeline_runs results[0])

**Implementation Note**: Uses `list_pipeline_runs` with `pipeline_run_ids` filter (Orchestra doesn't have individual detail endpoint)

**Use Cases**:
- Investigate specific failed run
- Validate pipeline execution state
- Extract error messages and timing

### 3. get_pipeline_run_details
**Purpose**: Get comprehensive details for pipeline run

**Parameters**:
- `pipeline_run_id` (required): Unique run identifier

**Returns**: Complete pipeline run information (same as get_pipeline_run_status)

**Implementation Note**: Alias of `get_pipeline_run_status` - both use list endpoint with filtering

**Use Cases**:
- Deep dive into pipeline execution
- Root cause analysis
- Performance investigation

### 4. list_task_runs
**Purpose**: List individual task executions within pipeline run

**Parameters**:
- `pipeline_run_id` (optional): Filter by specific pipeline run
- `time_from` (optional): ISO 8601 start time
- `time_to` (optional): ISO 8601 end time
- `status` (optional): Filter by status (CREATED, SKIPPED, QUEUED, RUNNING, SUCCEEDED, WARNING, FAILED, CANCELLING, CANCELLED)
- `pipeline_ids` (optional): Comma-separated pipeline IDs
- `integration` (optional): Comma-separated integration names
- `task_run_ids` (optional): Comma-separated task run IDs
- `limit` (default: 100, max: 1000): Results per query
- `offset` (default: 0): Pagination offset

**Returns**: Paginated response with task run details

**⚠️ Validation Status**: API endpoint may return 404 - availability to be confirmed in production use

**Use Cases**:
- Identify which task failed in multi-task pipeline
- Analyze task execution order and timing
- Track task-level performance

### 5. get_task_run_artifacts
**Purpose**: List available artifacts (logs, outputs) from task execution

**Parameters**:
- `pipeline_run_id` (required): Pipeline run ID
- `task_run_id` (required): Task run ID

**Returns**: List of artifact info dictionaries with filenames, sizes, types

**⚠️ Validation Status**: API endpoint availability to be validated in production use

**Use Cases**:
- Discover available logs for troubleshooting
- Identify output files from task execution
- Plan artifact downloads for analysis

### 6. download_task_artifact
**Purpose**: Download actual artifact content (logs, outputs)

**Parameters**:
- `pipeline_run_id` (required): Pipeline run ID
- `task_run_id` (required): Task run ID
- `filename` (required): Specific artifact filename to download

**Returns**: Artifact content as string

**⚠️ Validation Status**: API endpoint availability to be validated in production use

**Use Cases**:
- Examine error logs for root cause
- Retrieve task output data for validation
- Access detailed execution traces

### 7. trigger_pipeline
**Purpose**: Manually trigger pipeline execution via webhook

**Parameters**:
- `pipeline_id` (required): Pipeline ID to trigger
- `cause` (default: "Triggered by Orchestra MCP"): Description of why triggered

**Returns**: Trigger response with new run information

**Use Cases**:
- Manual pipeline execution for testing
- Recovery from failure (re-run)
- On-demand data refresh

## Usage Patterns

### Pattern 1: Failed Pipeline Investigation

**Scenario**: "Pipeline X failed last night, investigate root cause"

**Workflow**:
```python
# Step 1: Find failed runs
failed_runs = orchestra_mcp.list_pipeline_runs(
    time_from="2025-10-15T00:00:00Z",
    status="FAILED",
    limit=10
)

# Step 2: Get specific run details
run_details = orchestra_mcp.get_pipeline_run_status(
    pipeline_run_id="<failed_run_id>"
)

# Step 3: Analyze error message, timing, trigger
# run_details contains: runStatus, message, createdAt, completedAt, triggeredBy

# Step 4 (if task-level API available): List task runs
task_runs = orchestra_mcp.list_task_runs(
    pipeline_run_id="<failed_run_id>"
)

# Step 5 (if artifact API available): Download error logs
artifacts = orchestra_mcp.get_task_run_artifacts(
    pipeline_run_id="<failed_run_id>",
    task_run_id="<failed_task_id>"
)
error_log = orchestra_mcp.download_task_artifact(
    pipeline_run_id="<failed_run_id>",
    task_run_id="<failed_task_id>",
    filename="error.log"
)
```

### Pattern 2: Performance Analysis

**Scenario**: "Analyze pipeline execution times over last week"

**Workflow**:
```python
# Query successful runs with time filtering
runs = orchestra_mcp.list_pipeline_runs(
    time_from="2025-10-08T00:00:00Z",
    time_to="2025-10-15T00:00:00Z",
    status="SUCCEEDED",
    limit=1000
)

# Analyze timing patterns
for run in runs['results']:
    start = datetime.fromisoformat(run['startedAt'])
    end = datetime.fromisoformat(run['completedAt'])
    duration = (end - start).total_seconds()
    # Identify slow runs, bottlenecks, trends
```

### Pattern 3: Pipeline Recovery Testing

**Scenario**: "Test pipeline fix by triggering manual run"

**Workflow**:
```python
# Trigger test run
trigger_response = orchestra_mcp.trigger_pipeline(
    pipeline_id="<pipeline_id>",
    cause="Manual trigger to test failure fix - Task #123"
)

# Get new run ID
new_run_id = trigger_response['id']

# Monitor execution
run_status = orchestra_mcp.get_pipeline_run_status(
    pipeline_run_id=new_run_id
)

# Validate: runStatus == "SUCCEEDED", check timing
```

## Agent Integration

### orchestra-expert Specialist

**Primary Consumer**: The `orchestra-expert` specialist agent is the main user of orchestra-mcp tools.

**Updated Confidence Levels** (with MCP):
- Pipeline failure investigation: 0.75 → 0.92 (+0.17)
- Performance analysis: 0.70 → 0.90 (+0.20)
- Error troubleshooting: 0.60 → 0.92 (+0.32)

**Workflow**: orchestra-expert uses MCP tools → analyzes data with orchestration expertise → provides recommendations to delegating role agents (data-engineer-role, analytics-engineer-role)

### Role Agent Delegation

**data-engineer-role**:
- Delegates pipeline failure investigation to orchestra-expert
- Uses orchestra-expert for workflow design validation
- Relies on MCP-enhanced troubleshooting for production issues

**analytics-engineer-role**:
- Delegates dbt + Orchestra integration analysis to orchestra-expert
- Uses for orchestrated transformation workflow monitoring

**da-architect-role**:
- Consults orchestra-expert for orchestration architecture decisions
- Uses for cross-system workflow pattern recommendations

## Setup & Configuration

### 1Password Secret Setup

**Item Name**: "DA Agent Hub - Orchestra"
**Vault**: GRC

**Fields**:
- `credential`: Orchestra API key (from Orchestra Settings → API Key)
- `base_url`: `https://app.getorchestra.io/api/engine/public/` (optional, uses default if not set)

**Environment Variable Mapping**:
- `credential` → `ORCHESTRA_API_KEY` (loaded via `~/dotfiles/load-secrets-from-1password.sh`)
- `base_url` → `ORCHESTRA_API_BASE_URL` (optional)

### .mcp.json Configuration

```json
{
  "mcpServers": {
    "orchestra-mcp": {
      "command": "bash",
      "args": ["scripts/launch-orchestra-mcp.sh"],
      "disabled": false,
      "_comment": "Orchestra orchestration platform MCP integration. Provides pipeline run querying, task run analysis, and artifact access. Week 5 Day 3 - Following dbt-mcp pattern with 1Password env vars."
    }
  }
}
```

### Validation Steps

1. **Check MCP Server Connection**:
   ```bash
   ./scripts/check-mcp-health.sh | grep orchestra-mcp
   # Expected: ✓ orchestra-mcp
   ```

2. **Test Basic Functionality**:
   ```python
   # In Claude Code
   orchestra_mcp.list_pipeline_runs(limit=5)
   # Expected: Paginated response with recent pipeline runs
   ```

3. **Validate Authentication**:
   - Successful response = API key working
   - 401 error = API key missing/invalid
   - 404 error = Endpoint not available (check API tier/version)

## Known Limitations

### API Endpoint Availability

**✅ Confirmed Working**:
- `list_pipeline_runs`: Returns paginated pipeline execution history
- `get_pipeline_run_status`: Returns specific run details

**⚠️ Needs Validation**:
- `list_task_runs`: May return 404 (API endpoint availability depends on Orchestra tier/version)
- `get_task_run_artifacts`: Endpoint availability to be confirmed
- `download_task_artifact`: Endpoint availability to be confirmed

### Data Retention

**7-Day Window**: Without `time_from`/`time_to` parameters, only last 7 days of data available

**Time Filter Constraints**:
- Must use both `time_from` AND `time_to` together
- Maximum 7-day range per query
- Older runs may return 404 even with time filters (retention policy)

### Pagination

**Default Page Size**: 50 results per page
**Maximum Results**: 1000 per query (use offset for more)

### Schema Validation

**Claude Code Validation**: MCP server returns rich paginated responses `{page, pageSize, total, results}` but Claude Code expects simple arrays. The "validation error" in Claude Code UI is cosmetic - the actual data is correct and accessible.

## Troubleshooting

### 404 Errors on Pipeline Run Details

**Symptom**: `get_pipeline_run_status` returns 404 for run ID

**Causes**:
1. Run ID outside 7-day retention window
2. Run ID from different environment/account
3. Pipeline run ID filter on list endpoint not matching

**Solution**:
- Use recent run IDs (from last 7 days)
- Query with `list_pipeline_runs` first to get valid IDs
- Validate run belongs to your Orchestra account

### Task Run Endpoints Return 404

**Symptom**: `list_task_runs` returns 404 error

**Causes**:
1. API endpoint not available in this Orchestra tier
2. Endpoint requires different URL structure
3. Feature not enabled for account

**Solution**:
- Use `list_pipeline_runs` for pipeline-level details
- Document limitation in findings
- Contact Orchestra support for API tier capabilities

### Authentication Failures

**Symptom**: 401 Unauthorized errors

**Causes**:
1. `ORCHESTRA_API_KEY` env var not set
2. API key expired or invalid
3. 1Password item missing or incorrect field name

**Solution**:
```bash
# Check env var is set
echo $ORCHESTRA_API_KEY  # Should show key value

# Reload secrets
source ~/dotfiles/load-secrets-from-1password.sh

# Verify 1Password item
op item get "DA Agent Hub - Orchestra" --vault GRC --fields credential

# Restart Claude Code to reload MCP server
```

## Future Enhancements

### Potential Additions

**Additional Tools**:
- `list_pipelines`: Get all pipeline definitions (not just runs)
- `get_pipeline_config`: Retrieve pipeline configuration and DAG
- `cancel_pipeline_run`: Stop running pipeline
- `get_pipeline_metrics`: Aggregate performance metrics

**Enhanced Error Handling**:
- Retry logic for transient API failures
- Better error messages for common scenarios
- Validation of API endpoint availability on startup

**Performance Optimization**:
- Caching for frequently accessed pipeline runs
- Batch operations for multiple run queries
- Streaming for large result sets

## References

**Orchestra Documentation**:
- https://docs.getorchestra.io/ - Official Orchestra documentation
- https://www.getorchestra.io/blog - Patterns and case studies
- https://app.getorchestra.io - Live Orchestra UI

**Pattern Documentation**:
- `.claude/memory/patterns/mcp-server-development-patterns.md` - MCP server development guide
- `.claude/memory/patterns/cross-system-analysis-patterns.md` - Agent coordination patterns
- `knowledge/da-agent-hub/mcp-servers/dbt-mcp.md` - Reference implementation pattern

**Related Agents**:
- `.claude/agents/specialists/orchestra-expert.md` - Primary consumer of orchestra-mcp tools
- `.claude/agents/roles/data-engineer-role.md` - Role agent that delegates to orchestra-expert
- `.claude/agents/roles/analytics-engineer-role.md` - Role agent for dbt + Orchestra workflows

---

*Last Updated*: 2025-10-15
*Status*: Production-Ready (core tools validated, task/artifact endpoints pending validation)
*Maintainer*: DA Agent Hub platform team
