# Project Specification: Orchestra MCP Server

## End Goal

Create a Model Context Protocol (MCP) server that enables AI agents to interact with the Orchestra orchestration platform. This server will provide standardized tools for querying pipeline runs, task runs, artifacts, and triggering pipelines - following the proven dbt-mcp pattern using the FastMCP framework.

**Business Value**: Enable AI-powered troubleshooting, monitoring, and automation of Orchestra workflows through standardized MCP integration with Claude and other AI agents.

## Success Criteria

- [ ] MCP server successfully connects to Orchestra Metadata API
- [ ] All 7 core tools implemented and functional
- [ ] Authentication via Bearer token from 1Password
- [ ] Integrated into `.mcp.json` with launch script
- [ ] Successfully diagnoses the failed Orchestra run from earlier (run `8e808ad7`)
- [ ] `orchestra-expert` specialist agent created and documented
- [ ] Knowledge base documentation complete with usage examples

## Scope

### Included
- **MCP Server**: Python package using FastMCP framework
- **7 Core Tools**: Pipeline runs, task runs, artifacts, triggering, error analysis
- **Authentication**: Bearer token from 1Password (Orchestra API key)
- **Launch Script**: Bash wrapper for environment variable loading
- **Integration**: `.mcp.json` configuration for Claude Code
- **Specialist Agent**: `orchestra-expert.md` with MCP tool guidance
- **Documentation**: Knowledge base entry with architecture and examples

### Excluded
- Orchestra webhook configuration (users handle via Orchestra UI)
- Historical data warehousing (separate dlt/Snowflake integration)
- Orchestra Snowflake Native App integration
- Write operations beyond triggering pipelines (read-focused for safety)

## Implementation Plan

### Phase 1: MCP Server Core (`orchestra-mcp` package)
**Location**: `projects/active/feature-build-orchestra-mcp-server-.../src/orchestra_mcp/`

#### 1.1: Package Structure
```
src/orchestra_mcp/
├── __init__.py          # Package exports
├── server.py            # FastMCP server implementation
├── client.py            # Orchestra API client
├── tools.py             # MCP tool definitions
└── models.py            # Pydantic models for API responses
```

#### 1.2: Core MCP Tools (7 tools)
1. **`list_pipeline_runs`** - Query runs with time filters
   - Parameters: `time_from`, `time_to`, `limit`, `status_filter`
   - Returns: List of pipeline runs with metadata

2. **`get_pipeline_run_status`** - Get specific run status
   - Parameters: `pipeline_run_id`
   - Returns: Run status, duration, timestamps

3. **`get_pipeline_run_details`** - Comprehensive run information
   - Parameters: `pipeline_run_id`
   - Returns: Full run metadata, configuration, results

4. **`list_task_runs`** - Query task runs within pipeline run
   - Parameters: `pipeline_run_id`
   - Returns: List of task runs with status

5. **`get_task_run_artifacts`** - List available artifacts
   - Parameters: `pipeline_run_id`, `task_run_id`
   - Returns: Available artifact files

6. **`download_task_artifact`** - Download specific artifact
   - Parameters: `pipeline_run_id`, `task_run_id`, `filename`
   - Returns: Artifact content

7. **`trigger_pipeline`** - Start pipeline via webhook
   - Parameters: `pipeline_id`, `cause` (optional)
   - Returns: Triggered run information

#### 1.3: Orchestra API Client
- **Base URL**: `https://app.getorchestra.io/api/engine/public/`
- **Authentication**: Bearer token header
- **Rate Limiting**: Handle 429 responses with retry logic
- **Pagination**: Support 1000 items per page
- **Error Handling**: Comprehensive error messages for API failures

#### 1.4: Configuration
```python
# Environment Variables
ORCHESTRA_API_KEY=<from-1password>
ORCHESTRA_API_BASE_URL=https://app.getorchestra.io/api/engine/public/
```

### Phase 2: Integration & Launch Script

#### 2.1: Launch Script (`scripts/launch-orchestra-mcp.sh`)
```bash
#!/bin/bash
# Orchestra-MCP Launcher with Environment Variable Authentication
# Passes authentication via environment variables from 1Password

set -e

# Self-locate and navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Source 1Password secrets (provides ORCHESTRA_API_KEY)
if [ -f "$HOME/dotfiles/load-secrets-from-1password.sh" ]; then
    source "$HOME/dotfiles/load-secrets-from-1password.sh" 2>/dev/null || true
fi

# Map 1Password variable names to orchestra-mcp expected names
export ORCHESTRA_API_KEY="${ORCHESTRA_API_KEY}"
export ORCHESTRA_API_BASE_URL="https://app.getorchestra.io/api/engine/public/"

# Debug logging
echo "DEBUG: Launching orchestra-MCP server" >> /tmp/orchestra-mcp-debug.log
echo "DEBUG: ORCHESTRA_API_KEY is set: ${ORCHESTRA_API_KEY:+yes}" >> /tmp/orchestra-mcp-debug.log
echo "DEBUG: ORCHESTRA_API_BASE_URL=$ORCHESTRA_API_BASE_URL" >> /tmp/orchestra-mcp-debug.log

# Launch orchestra-MCP with Python 3.12 (Python 3.13 has asyncio stdio bug)
uvx --python 3.12 orchestra-mcp
```

#### 2.2: .mcp.json Configuration
```json
{
  "mcpServers": {
    "orchestra-mcp": {
      "command": "bash",
      "args": ["scripts/launch-orchestra-mcp.sh"],
      "disabled": false,
      "_comment": "Orchestra orchestration platform MCP integration. Provides pipeline run querying, task run analysis, and artifact access."
    }
  }
}
```

#### 2.3: 1Password Secret Setup
**Item Name**: `DA Agent Hub - Orchestra`
**Vault**: `GRC`
**Fields**:
- `credential`: Orchestra API Key (from Settings → API Key)
- `base_url`: `https://app.getorchestra.io/api/engine/public/`

### Phase 3: Specialist Agent & Documentation

#### 3.1: Orchestra Expert Specialist
**File**: `.claude/agents/specialists/orchestra-expert.md`

**Key Sections**:
- Role & Expertise (workflow orchestration specialist)
- Core Responsibilities (pipeline monitoring, troubleshooting, optimization)
- MCP Tools Integration (all 7 tools with confidence levels)
- Collaboration with other specialists (dbt-expert, data-engineer-role, etc.)
- Common troubleshooting patterns
- Performance optimization strategies

#### 3.2: Knowledge Base Documentation
**Location**: `knowledge/da-agent-hub/development/orchestra-mcp-server.md`

**Contents**:
- Architecture overview
- MCP tool catalog with examples
- Authentication setup
- Common usage patterns
- Troubleshooting guide
- Integration with existing workflows

## Technical Requirements

### Systems Involved
- **Orchestra Platform**: https://app.getorchestra.io
- **Orchestra Metadata API**: REST API for pipeline/task run data
- **1Password**: Secure credential storage
- **Claude Code**: MCP client integration via .mcp.json
- **DA Agent Hub**: Integration point for all MCP servers

### Tools & Technologies
- **FastMCP**: Python MCP server framework
- **httpx**: Async HTTP client for Orchestra API
- **Pydantic**: Data validation and API models
- **uvx**: Python package runner (like npx for Python)
- **Python 3.12**: Avoid 3.13 due to asyncio stdio bugs

### Dependencies
- `fastmcp` - MCP server framework
- `httpx` - HTTP client
- `pydantic` - Data models
- `python-dotenv` - Environment variable loading (optional)

## Acceptance Criteria

### Functional Requirements
- [ ] All 7 MCP tools execute successfully with valid Orchestra credentials
- [ ] Error handling provides clear, actionable messages
- [ ] Authentication works via 1Password credential loading
- [ ] Pagination handles large result sets (>1000 items)
- [ ] Time filtering works correctly for historical queries
- [ ] Artifact download handles binary and text files
- [ ] Pipeline triggering returns run ID for monitoring

### Non-Functional Requirements
- [ ] Response time <2 seconds for typical queries
- [ ] Handles API rate limiting gracefully (retry with backoff)
- [ ] Comprehensive error messages for troubleshooting
- [ ] Debug logging for MCP connection issues
- [ ] Works with Python 3.12 (tested compatibility)

### Testing & Validation
- [ ] Successfully queries the failed run `8e808ad7` from earlier
- [ ] Extracts detailed error information from that run
- [ ] Lists all pipeline runs from last 7 days
- [ ] Downloads task artifacts successfully
- [ ] Triggers test pipeline (if available)

## Orchestra API Reference

### Base URL
```
https://app.getorchestra.io/api/engine/public/
```

### Authentication
```
Authorization: Bearer {api_key}
```

### Key Endpoints
```
GET  /pipeline_runs
GET  /pipeline_runs/{pipeline_run_id}/status
GET  /pipeline_runs/{pipeline_run_id}
GET  /pipeline_runs/{pipeline_run_id}/task_runs
GET  /pipeline_runs/{pipeline_run_id}/task_runs/{task_run_id}/artifacts
GET  /pipeline_runs/{pipeline_run_id}/task_runs/{task_run_id}/artifacts/download?filename={filepath}
POST /pipelines/{pipeline-id}/start
```

### Query Parameters
- `time_from`: ISO 8601 timestamp (e.g., `2025-04-01T00:00:00Z`)
- `time_to`: ISO 8601 timestamp
- `limit`: Max results per page (default: 1000)
- `offset`: Pagination offset

### Data Retention
- Without date filters: **7 days only**
- With date filters: Historical data available

## Risk Assessment

### High Risk
- **API Key Exposure**: Mitigated by 1Password + environment variables
- **Rate Limiting**: Mitigated by retry logic and backoff strategies
- **API Changes**: Mitigated by comprehensive error handling and logging

### Medium Risk
- **Python 3.13 Compatibility**: Avoid 3.13, use 3.12 explicitly (asyncio stdio bug)
- **Large Result Sets**: Handle pagination properly
- **Binary Artifacts**: Ensure proper encoding for downloads

### Dependencies
- **Orchestra Platform Access**: Requires Enterprise plan for Metadata API
- **1Password CLI**: Must be installed and authenticated
- **FastMCP Framework**: Dependency on external package

## Timeline Estimate

- **Phase 1 (MCP Server Core)**: 2-3 hours
  - Package structure: 30 minutes
  - API client: 45 minutes
  - Tool implementations: 1.5 hours
  - Testing: 30 minutes

- **Phase 2 (Integration)**: 1 hour
  - Launch script: 20 minutes
  - .mcp.json configuration: 10 minutes
  - 1Password setup: 10 minutes
  - End-to-end testing: 20 minutes

- **Phase 3 (Documentation)**: 1.5 hours
  - orchestra-expert.md: 45 minutes
  - Knowledge base documentation: 45 minutes

- **Total Estimated**: 4-5 hours

## Implementation Notes

### Pattern: Following dbt-mcp
- Same authentication approach (1Password → env vars → MCP server)
- Same launch script pattern (bash wrapper with source loading)
- Same .mcp.json integration approach
- Similar tool naming conventions
- Consistent error handling and logging patterns

### Immediate Use Case
Once implemented, we'll use this to diagnose the Orchestra pipeline failure:
```python
# Get failed run details
get_pipeline_run_details(pipeline_run_id="8e808ad7...")

# List task runs to find which failed
list_task_runs(pipeline_run_id="8e808ad7...")

# Download error artifacts
download_task_artifact(
  pipeline_run_id="8e808ad7...",
  task_run_id="...",
  filename="error.log"
)
```

---

*This specification remains stable. Working context and progress tracking in context.md*
