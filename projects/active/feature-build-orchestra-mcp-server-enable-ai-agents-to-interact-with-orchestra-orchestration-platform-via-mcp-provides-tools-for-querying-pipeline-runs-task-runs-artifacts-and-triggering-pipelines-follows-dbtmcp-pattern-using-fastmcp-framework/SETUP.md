# Orchestra MCP Server - Setup Guide

## Prerequisites

- Orchestra Enterprise plan (for Metadata API access)
- 1Password CLI installed and authenticated
- Python 3.12+ (avoid 3.13 due to asyncio stdio bugs)
- `uvx` installed (Python package runner)

## Step 1: Get Orchestra API Key

1. Log into Orchestra: https://app.getorchestra.io
2. Navigate to **Settings → API Key**
3. Copy your API key (format: `orch_...`)

## Step 2: Store in 1Password

Create a new item in 1Password with the following details:

```
Item Name: DA Agent Hub - Orchestra
Vault: GRC
Type: API Credential

Fields:
- credential: <paste your Orchestra API key>
- base_url: https://app.getorchestra.io/api/engine/public/
```

**Via 1Password CLI** (if authenticated):
```bash
op item create \
  --category="API Credential" \
  --title="DA Agent Hub - Orchestra" \
  --vault="GRC" \
  credential="<your-orchestra-api-key>" \
  base_url[text]="https://app.getorchestra.io/api/engine/public/"
```

**Via 1Password App**:
1. Open 1Password app
2. Select "GRC" vault
3. Click "+ New Item"
4. Select "API Credential" type
5. Fill in the fields as shown above
6. Save

## Step 3: Update load-secrets Script

Add Orchestra credential loading to `~/dotfiles/load-secrets-from-1password.sh`:

```bash
# Orchestra orchestration platform
export ORCHESTRA_API_KEY=$(op item get "DA Agent Hub - Orchestra" --vault="GRC" --fields label=credential --reveal 2>/dev/null || echo "")
```

## Step 4: Reload Environment

```bash
# Reload secrets
source ~/dotfiles/load-secrets-from-1password.sh

# Verify credential loaded
echo "Orchestra API Key set: ${ORCHESTRA_API_KEY:+yes}"
```

## Step 5: Restart Claude Code

For MCP changes to take effect:

1. Quit Claude Code completely
2. Reopen Claude Code
3. The orchestra-mcp server will start automatically

## Step 6: Verify MCP Server

```bash
# Check orchestra-mcp is listed
claude mcp list | grep orchestra-mcp

# Check debug log for startup issues
tail -f /tmp/orchestra-mcp-debug.log
```

## Step 7: Test MCP Tools

In Claude Code, try these commands:

```markdown
# List recent pipeline runs
Use orchestra-mcp tool: list_pipeline_runs(limit=10)

# Get specific run details
Use orchestra-mcp tool: get_pipeline_run_details(pipeline_run_id="8e808ad7-...")

# List task runs for a pipeline
Use orchestra-mcp tool: list_task_runs(pipeline_run_id="8e808ad7-...")
```

## Troubleshooting

### MCP Server Not Starting

Check debug log:
```bash
tail -20 /tmp/orchestra-mcp-debug.log
```

Common issues:
- `ORCHESTRA_API_KEY` not set → Verify 1Password item and reload secrets
- Python 3.13 asyncio bug → Ensure launch script uses `--python 3.12`
- Package not installed → Run `uvx --python 3.12 orchestra-mcp` manually to see errors

### API Authentication Errors

```bash
# Test API key directly
curl -H "Authorization: Bearer $ORCHESTRA_API_KEY" \
  https://app.getorchestra.io/api/engine/public/pipeline_runs?limit=5

# Should return JSON with pipeline runs
# If 401: API key invalid or expired
# If 403: Enterprise plan required for Metadata API
```

### MCP Tools Timeout

- Orchestra API may have rate limits
- Large result sets may take time
- Use pagination parameters (limit, offset) for better performance

## Environment Variable Reference

**Required**:
- `ORCHESTRA_API_KEY` - Orchestra API key from Settings → API Key

**Optional**:
- `ORCHESTRA_API_BASE_URL` - Base URL for Orchestra API (default: https://app.getorchestra.io/api/engine/public/)

## Architecture

```
1Password (GRC vault)
  ↓
~/dotfiles/load-secrets-from-1password.sh
  ↓
Environment: ORCHESTRA_API_KEY
  ↓
scripts/launch-orchestra-mcp.sh
  ↓
uvx --python 3.12 orchestra-mcp
  ↓
FastMCP Server (7 tools)
  ↓
Orchestra Metadata API
```

## Next Steps

Once setup is complete:
1. **Test with failed run**: Use MCP tools to investigate run `8e808ad7` from earlier
2. **Agent integration**: Use `orchestra-expert` specialist for workflow troubleshooting
3. **Knowledge base**: Reference `knowledge/da-agent-hub/development/orchestra-mcp-server.md`
