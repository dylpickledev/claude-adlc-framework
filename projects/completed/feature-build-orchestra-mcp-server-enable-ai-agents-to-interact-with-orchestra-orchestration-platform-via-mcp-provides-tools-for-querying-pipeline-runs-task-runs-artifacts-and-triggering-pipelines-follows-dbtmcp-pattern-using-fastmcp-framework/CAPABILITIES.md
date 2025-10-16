# Orchestra MCP Server - Capabilities & Limitations

**Last Updated**: 2025-10-15
**Status**: Production-Ready (with documented limitations)
**Testing**: Validated against production Orchestra API

## Executive Summary

The orchestra-mcp server provides **read-only pipeline run monitoring** with the ability to trigger new runs. It **CANNOT** access task-level error details, logs, or artifacts due to Orchestra Metadata API tier limitations.

## What It CAN Do (Verified Working)

### ✅ Pipeline Run Query & Monitoring

**Tool**: `mcp__orchestra-mcp__list_pipeline_runs`

**Capabilities**:
- Query recent pipeline execution history (default: last 7 days without time filters)
- Get paginated results (50 per page, up to 1000 total per query)
- Retrieve comprehensive run metadata:
  - Run ID, Pipeline ID, Pipeline Name
  - Run Status (CREATED, RUNNING, SUCCEEDED, WARNING, FAILED, CANCELLING, CANCELLED)
  - Timing information (created, started, completed timestamps)
  - Duration calculations
  - Trigger information (SCHEDULED, WEBHOOK, SENSOR)
  - Git information (branch, commit) - if pipeline has git integration
  - Generic failure message: "Pipeline failed - a task is in failed state"

**Limitations**:
- ⚠️ **FastMCP parameter exposure issue**: `status` and `pipeline_run_ids` parameters exist in Python client but are NOT exposed in the MCP tool schema
- ⚠️ **Time filter constraints**: Must use both `time_from` AND `time_to` together (max 7-day range)
- ⚠️ **No error details**: Only generic failure message, no specific task errors
- ⚠️ **No task breakdown**: Cannot see which specific task failed

**Workaround**: Use `scripts/find_run.py` to bypass FastMCP limitations and access full API parameters

**Example Query**:
```python
# Via MCP tool (limited parameters)
mcp__orchestra-mcp__list_pipeline_runs(
    time_from="2025-10-15T00:00:00Z",
    time_to="2025-10-16T00:00:00Z",
    limit=100
)

# Via workaround script (full parameters)
python3 scripts/find_run.py \
    --status "FAILED" \
    --pipeline-name "Sales Journal" \
    --time-from "2025-10-15T00:00:00Z" \
    --time-to "2025-10-16T00:00:00Z"
```

**Returns**:
```json
{
  "page": 1,
  "pageSize": 50,
  "total": 38,
  "results": [
    {
      "id": "8e808ad7-70c7-4718-8b60-ee4c915c34de",
      "pipelineId": "daa39221-b30f-4b27-a8ee-a1b98ca28d0f",
      "pipelineName": "Sales Journal - Full Refresh DBT Models",
      "runStatus": "FAILED",
      "message": "Pipeline failed - a task is in failed state.",
      "createdAt": "2025-10-15T20:41:19.895010+00:00",
      "startedAt": "2025-10-15T20:41:20.270764+00:00",
      "completedAt": "2025-10-15T20:50:12.898968+00:00",
      "triggeredBy": [{"triggerType": "WEBHOOK"}],
      "branch": null,
      "commit": null
    }
  ]
}
```

### ✅ Pipeline Run Triggering

**Tool**: `mcp__orchestra-mcp__trigger_pipeline`

**Capabilities**:
- Manually trigger pipeline execution via webhook
- Provide custom cause/description for audit trail
- Returns new pipeline run ID and initial status

**Limitations**:
- ⚠️ Cannot pass runtime parameters to the pipeline
- ⚠️ No way to validate if pipeline exists before triggering
- ⚠️ No synchronous wait for completion (returns immediately)

**Example**:
```python
mcp__orchestra-mcp__trigger_pipeline(
    pipeline_id="daa39221-b30f-4b27-a8ee-a1b98ca28d0f",
    cause="Manual trigger to test fix for sales journal error"
)
```

**Returns**:
```json
{
  "id": "new-run-id-12345",
  "status": "CREATED",
  "message": "Pipeline run created successfully"
}
```

## What It CANNOT Do (API Limitations)

### ❌ Task-Level Details

**Attempted Tool**: `mcp__orchestra-mcp__list_task_runs`

**Status**: **404 Not Found** - Endpoint not available in current Orchestra tier/API version

**Impact**: Cannot determine:
- Which specific task failed in a pipeline
- Task execution order
- Individual task timing
- Task status breakdown
- Task error messages

**Tested Endpoint**: `GET /api/engine/public/task_runs`
**Result**: 404 error consistently across all parameters

### ❌ Error Details & Logs

**What's Missing**:
- Specific error messages from failed tasks (e.g., "Database Error in model X")
- Stack traces or error details
- Task execution logs
- Snowflake/dbt error codes
- Compilation errors

**What You Get Instead**:
- Generic message: "Pipeline failed - a task is in failed state"
- No indication of WHICH task or WHY it failed

**Tested Endpoints**:
- `GET /api/engine/public/pipeline_runs/{run_id}` → 404
- `GET /api/engine/public/pipeline_runs/{run_id}/tasks` → 404
- `GET /api/engine/public/pipeline_runs/{run_id}/logs` → 404
- `GET /api/engine/public/pipeline_runs/{run_id}/events` → 404

**Confirmed**: Error details visible in Orchestra UI are **NOT** exposed via Metadata API

### ❌ Artifact Access

**Attempted Tools**:
- `mcp__orchestra-mcp__get_task_run_artifacts`
- `mcp__orchestra-mcp__download_task_artifact`

**Status**: **Cannot Test** - Requires task_run_id which we cannot obtain (task_runs endpoint returns 404)

**Impact**: Cannot access:
- Task output files
- Execution logs
- Generated artifacts
- Debug information

### ❌ Individual Run Details Endpoint

**Missing**: Direct endpoint for single run details

**Current Workaround**: Use `list_pipeline_runs` with client-side filtering (via scripts/find_run.py)

**Why It Matters**:
- `pipeline_run_ids` parameter exists but FastMCP doesn't expose it
- Must query all runs and filter client-side
- Less efficient for targeted queries

## Specialist Agent Capabilities

### orchestra-expert Specialist

**What It CAN Do**:
1. **Query recent pipeline executions** via `list_pipeline_runs`
2. **Identify failed pipeline runs** by status and timing
3. **Analyze execution patterns** (frequency, timing, trigger types)
4. **Track pipeline health** over time
5. **Trigger manual pipeline runs** for testing
6. **Correlate failures** with timing/schedule changes

**What It CANNOT Do**:
1. ❌ **Determine root cause of failures** - no access to error messages
2. ❌ **Identify which task failed** - no task-level API
3. ❌ **Access execution logs** - not exposed via API
4. ❌ **Debug specific errors** - only generic failure message
5. ❌ **Analyze task dependencies** - no task graph access

**Confidence Levels** (WITH MCP tools):
- Pipeline failure detection: **HIGH (0.95)** - Can accurately find failed runs
- Performance analysis: **HIGH (0.90)** - Good timing/duration data
- Root cause analysis: **LOW (0.30)** - No access to error details
- Error troubleshooting: **LOW (0.25)** - Must defer to UI inspection

### Delegation Pattern

When `orchestra-expert` encounters a failed pipeline:

1. ✅ **Can Report**:
   - Pipeline name, run ID, status
   - Execution timing (start, end, duration)
   - Trigger type and schedule
   - Git information (if available)
   - Generic failure message

2. ❌ **Cannot Report** (Must Defer):
   - Specific task that failed
   - Error message details
   - Root cause analysis
   - Remediation recommendations

3. 🔄 **Handoff Required**:
   - User must check Orchestra UI for error details
   - Or: User provides error message from UI
   - Then: Specialist can analyze the specific error (if it's Snowflake, dbt, etc.)

## Workarounds for Limitations

### Workaround 1: Manual Error Extraction

**Process**:
1. Use orchestra-mcp to identify failed run
2. User opens Orchestra UI to view error details
3. User provides error message to Claude
4. Claude routes to appropriate specialist (snowflake-expert, dbt-expert, etc.)

**Tools**:
```bash
# Step 1: Find failed run
python3 scripts/find_run.py --status FAILED --pipeline-name "Sales Journal"

# Step 2: User opens UI and copies error message

# Step 3: User provides error to Claude
"The error was: Database Error in model rpt_sales_journal_analysis..."
```

### Workaround 2: Cross-System Correlation

**For dbt pipelines**:
1. Get Orchestra run timing from MCP
2. Query dbt Cloud API for runs in that time window
3. Match by timing and get dbt error details

**For Snowflake errors**:
1. Get Orchestra run timing
2. Query Snowflake QUERY_HISTORY for errors in that window
3. Match by timing and database/schema

**Limitation**: Requires assumptions about system integration

### Workaround 3: Parameter Access via Script

**Problem**: FastMCP doesn't expose `status` and `pipeline_run_ids` parameters

**Solution**: Use `scripts/find_run.py` which directly calls OrchestraClient

```bash
# Full parameter support
python3 scripts/find_run.py \
    --run-id "8e808ad7-70c7-4718-8b60-ee4c915c34de" \
    --status "FAILED" \
    --time-from "2025-10-15T00:00:00Z" \
    --time-to "2025-10-16T00:00:00Z"
```

## Outstanding Questions for Orchestra Support

When contacting Orchestra about API capabilities, ask:

1. **Error Details Access**:
   - Is there an API endpoint that returns task-level error messages?
   - How does the UI get error details that aren't in the Metadata API?
   - Is there a GraphQL endpoint with richer error information?

2. **Task Run Access**:
   - Is `GET /api/engine/public/task_runs` available in all tiers?
   - What tier/plan is required for task-level API access?
   - Are there alternative endpoints for task information?

3. **Individual Run Endpoint**:
   - Is `GET /api/engine/public/pipeline_runs/{run_id}` supposed to work?
   - Why does `pipeline_run_ids` parameter exist if it doesn't filter results?
   - Is there a better way to get single run details?

4. **Artifact Access**:
   - Are artifact endpoints available: `/pipeline_runs/{run_id}/task_runs/{task_id}/artifacts`?
   - What tier/plan enables artifact access?
   - Can we download task logs via API?

5. **API Documentation**:
   - Is there comprehensive API documentation beyond what's at docs.getorchestra.io?
   - Are there undocumented endpoints that might help?
   - Is there a Swagger/OpenAPI spec available?

## Implementation Notes

### FastMCP Schema Generation Issue

**Problem**: FastMCP's automatic schema generation doesn't expose all function parameters

**Affected Parameters**:
- `list_pipeline_runs`: `status`, `pipeline_run_ids` not exposed
- All others seem to work correctly

**Root Cause**: Unknown - may be FastMCP bug or intentional type validation issue

**Impact**:
- MCP tool calls validate against generated schema
- Parameters in function signature but not in schema → validation error
- Must use workaround script to access full API

**Future Fix**:
- Report to FastMCP maintainers
- Or: Manually define schema instead of relying on auto-generation
- Or: Wait for FastMCP framework update

### API Response Format

**All endpoints return paginated responses**:
```json
{
  "page": 1,
  "pageSize": 50,
  "total": 2363,
  "results": [...]
}
```

**Claude Code expects simple arrays**, so validation errors appear but data is accessible in error output.

**Not a blocker**: The "validation error" is cosmetic - actual data is correctly returned and usable.

## Testing Protocol

To verify orchestra-mcp capabilities:

```bash
# 1. Check MCP server connection
./scripts/check-mcp-health.sh | grep orchestra-mcp
# Expected: ✓ orchestra-mcp (CONNECTED)

# 2. Test basic query (no parameters)
mcp__orchestra-mcp__list_pipeline_runs(limit=5)
# Expected: Paginated response with recent runs

# 3. Test time filtering
mcp__orchestra-mcp__list_pipeline_runs(
    time_from="2025-10-15T00:00:00Z",
    time_to="2025-10-16T00:00:00Z"
)
# Expected: Runs from that window

# 4. Test parameter script workaround
python3 scripts/find_run.py --status FAILED --limit 10
# Expected: JSON output with failed runs

# 5. Test task_runs (expect failure)
mcp__orchestra-mcp__list_task_runs(pipeline_run_id="<any-id>")
# Expected: 404 error

# 6. Test trigger
mcp__orchestra-mcp__trigger_pipeline(
    pipeline_id="<test-pipeline-id>",
    cause="Testing MCP trigger functionality"
)
# Expected: New run ID returned
```

## Recommendations

### For Current Use

1. **Pipeline Monitoring**: ✅ Use orchestra-mcp - works well
2. **Failure Detection**: ✅ Use orchestra-mcp - can identify failed runs accurately
3. **Error Investigation**: ❌ Manual UI check required
4. **Performance Analysis**: ✅ Use orchestra-mcp - good timing data
5. **Manual Triggering**: ✅ Use orchestra-mcp - works reliably

### For Future Enhancement

1. **Request Orchestra API improvements**: Task-level endpoints, error details
2. **Build JavaScript-capable scraper**: Extract UI data programmatically
3. **Fix FastMCP parameter exposure**: Report issue or manually define schemas
4. **Cross-system correlation**: Link Orchestra → dbt Cloud → Snowflake for fuller picture
5. **Monitoring integration**: Set up alerts based on what orchestra-mcp CAN detect

## Version History

- **2025-10-15**: Initial capabilities documentation
  - Production testing completed
  - API limitations confirmed
  - Workarounds documented
  - FastMCP schema issue identified

---

**Maintainer**: DA Agent Hub platform team
**Status**: Production-ready with documented limitations
**Next Review**: After Orchestra support response on API capabilities
