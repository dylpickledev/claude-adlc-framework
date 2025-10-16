# Orchestra MCP Server

Model Context Protocol server for Orchestra orchestration platform.

**Production deployment** - See `knowledge/da-agent-hub/mcp-servers/orchestra-mcp.md` for complete documentation.

## Quick Start

Launched automatically via `.mcp.json` configuration:
```bash
bash scripts/launch-orchestra-mcp.sh
```

## Authentication

Configured via 1Password → environment variables:
- `ORCHESTRA_API_KEY` (required)
- `ORCHESTRA_API_BASE_URL` (defaults to https://app.getorchestra.io/api/engine/public/)

## Available Tools

- `list_pipeline_runs` - Query pipeline execution history
- `get_pipeline_run_status` - Get specific run status
- `get_pipeline_run_details` - Get comprehensive run details
- `list_task_runs` - List task executions
- `get_task_run_artifacts` - List available artifacts
- `download_task_artifact` - Download specific artifacts
- `trigger_pipeline` - Trigger new pipeline runs

## Documentation

**Complete reference**: `knowledge/da-agent-hub/mcp-servers/orchestra-mcp.md`

**Capabilities & limitations**: See project CAPABILITIES.md in completed projects archive

**Production validation**: All tools tested against production Orchestra API
