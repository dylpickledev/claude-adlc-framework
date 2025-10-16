# MCP Server to Specialist Agent Mapping

**Pattern Type:** Integration Reference
**Confidence:** 1.0 (Definitive source of truth)
**Last Updated:** 2025-10-15
**Purpose:** Authoritative mapping of MCP servers to specialist agents - ensures agents know which tools they can use

## Critical Rule

**When you say an MCP is working, it MUST work.** This document ensures every specialist agent knows exactly which MCP tools they have access to and how to use them correctly.

## MCP Server Status & Ownership

### ✅ ACTIVE MCP Servers (Currently Deployed)

#### 1. dbt-mcp
**Status**: ✅ ACTIVE (Multi-tenant host configured)
**Launch Script**: `scripts/launch-dbt-mcp.sh`
**Host**: `te240.us1.dbt.com` (CRITICAL: GraniteRock uses multi-tenant, NOT cloud.getdbt.com)
**Primary Specialist**: `dbt-expert`
**Secondary Users**: `analytics-engineer-role`, `snowflake-expert`, `data-quality-specialist`

**Tools Available**:
- `mcp__dbt-mcp__list_jobs` - List all dbt Cloud jobs
- `mcp__dbt-mcp__list_jobs_runs` - List job runs with filtering
- `mcp__dbt-mcp__get_job_run_details` - Get detailed run information
- `mcp__dbt-mcp__get_job_run_error` - Get error details from failed runs
- `mcp__dbt-mcp__list_job_run_artifacts` - List available artifacts
- `mcp__dbt-mcp__get_all_models` - Get all dbt models
- `mcp__dbt-mcp__get_mart_models` - Get mart layer models
- `mcp__dbt-mcp__show` - Execute dbt show command

**Configuration Notes**:
- Uses Python 3.12 (Python 3.13 has asyncio stdio bug)
- Loads credentials from 1Password via `load-secrets-from-1password.sh`
- Debug logs: `/tmp/dbt-mcp-debug.log`
- **MUST restart Claude Code after updating launch script** (MCP connects on launch)

**Troubleshooting**:
- 401 errors → Check `DBT_HOST` is set to multi-tenant instance (`te240.us1.dbt.com`)
- Empty tool responses → Verify token length: `echo ${#DBT_CLOUD_API_TOKEN}`
- Connection failures → Check debug log: `tail /tmp/dbt-mcp-debug.log`
- See: `.claude/memory/patterns/dbt-cloud-multi-tenant-host-pattern.md`

#### 2. orchestra-mcp
**Status**: ✅ ACTIVE
**Launch Script**: `scripts/launch-orchestra-mcp.sh`
**Base URL**: `https://app.getorchestra.io/api/engine/public/`
**Primary Specialist**: `orchestra-expert`
**Secondary Users**: `data-engineer-role`, `prefect-expert`

**Tools Available**:
- `mcp__orchestra-mcp__list_pipeline_runs` - List pipeline runs with time filtering
- `mcp__orchestra-mcp__get_pipeline_run_status` - Get run status
- `mcp__orchestra-mcp__get_pipeline_run_details` - Get comprehensive run details
- `mcp__orchestra-mcp__list_task_runs` - List task runs within pipeline
- `mcp__orchestra-mcp__get_task_run_artifacts` - List task artifacts
- `mcp__orchestra-mcp__download_task_artifact` - Download specific artifact
- `mcp__orchestra-mcp__trigger_pipeline` - Trigger pipeline via webhook

**Configuration Notes**:
- Uses Python 3.12 (same asyncio issue)
- Local development server from project directory
- Debug logs: `/tmp/orchestra-mcp-debug.log`

#### 3. aws-api
**Status**: ✅ ACTIVE
**Type**: Official AWS Labs MCP
**Command**: `uvx awslabs.aws-api-mcp-server@latest`
**Primary Specialist**: `aws-expert`
**Secondary Users**: `ui-ux-developer-role`, `streamlit-expert`, `react-expert`

**Tools Available**:
- `mcp__aws-api__suggest_aws_commands` - Natural language → AWS CLI suggestions
- `mcp__aws-api__call_aws` - Execute AWS CLI commands directly

**Configuration Notes**:
- Region: `us-west-2` (default)
- Profile: `default`
- READ_OPERATIONS_ONLY: `true` (safety)
- Uses AWS credentials from `~/.aws/credentials`

#### 4. aws-docs
**Status**: ✅ ACTIVE
**Type**: Official AWS Labs MCP
**Command**: `uvx awslabs.aws-documentation-mcp-server@latest`
**Primary Specialist**: `aws-expert`
**Secondary Users**: All specialists needing AWS documentation

**Tools Available**:
- `mcp__aws-docs__search_documentation` - Search AWS docs
- `mcp__aws-docs__read_documentation` - Read specific doc pages
- `mcp__aws-docs__recommend` - Get related documentation

**Configuration Notes**:
- Partition: `aws` (US commercial cloud)
- No authentication required (public docs)

#### 5. github
**Status**: ✅ ACTIVE
**Type**: Official Anthropic MCP
**Command**: `npx -y @modelcontextprotocol/server-github`
**Primary Specialist**: `github-sleuth-expert`
**Secondary Users**: All role agents, `documentation-expert`

**Tools Available**:
- `mcp__github__search_repositories` - Search GitHub repos
- `mcp__github__create_repository` - Create new repo
- `mcp__github__get_file_contents` - Read files from repos
- `mcp__github__push_files` - Push multiple files in single commit
- `mcp__github__create_issue` - Create new issue
- `mcp__github__list_issues` - List issues with filtering
- `mcp__github__get_issue` - Get issue details
- `mcp__github__update_issue` - Update existing issue
- `mcp__github__add_issue_comment` - Add comment to issue
- `mcp__github__search_code` - Search code across repos
- `mcp__github__search_issues` - Search issues/PRs
- `mcp__github__create_pull_request` - Create PR
- `mcp__github__get_pull_request` - Get PR details
- `mcp__github__list_pull_requests` - List PRs
- `mcp__github__create_pull_request_review` - Review PR
- `mcp__github__merge_pull_request` - Merge PR
- `mcp__github__get_pull_request_files` - Get PR file changes
- `mcp__github__get_pull_request_status` - Get PR CI status
- `mcp__github__update_pull_request_branch` - Update PR branch
- And more...

**Configuration Notes**:
- Uses GitHub PAT from 1Password
- Scopes: `repo`, `read:org`, `read:project`
- See: `.claude/memory/patterns/github-repo-context-resolution.md` for repo resolution

#### 6. slack
**Status**: ✅ ACTIVE
**Type**: Official Anthropic MCP
**Command**: `npx -y @modelcontextprotocol/server-slack`
**Primary Specialist**: `business-context`
**Secondary Users**: `documentation-expert`, role agents for stakeholder communication

**Tools Available**:
- `mcp__slack__slack_list_channels` - List workspace channels
- `mcp__slack__slack_post_message` - Post to channel
- `mcp__slack__slack_reply_to_thread` - Reply to thread
- `mcp__slack__slack_add_reaction` - Add emoji reaction
- `mcp__slack__slack_get_channel_history` - Get recent messages
- `mcp__slack__slack_get_thread_replies` - Get thread messages
- `mcp__slack__slack_get_users` - List workspace users
- `mcp__slack__slack_get_user_profile` - Get user profile

**Configuration Notes**:
- Workspace: GraniteRock (TSQABERKL)
- Bot token from 1Password
- Scopes: `channels:read`, `chat:write`, `users:read`

#### 7. filesystem
**Status**: ✅ ACTIVE
**Type**: Official Anthropic MCP
**Command**: `npx -y @modelcontextprotocol/server-filesystem`
**Allowed Paths**: `/Users/TehFiestyGoat/da-agent-hub` (project root)
**Primary Users**: ALL agents (for project file operations)

**Tools Available**:
- `mcp__filesystem__read_text_file` - Read text files
- `mcp__filesystem__read_media_file` - Read images/audio
- `mcp__filesystem__read_multiple_files` - Batch file reads
- `mcp__filesystem__write_file` - Write/overwrite files
- `mcp__filesystem__edit_file` - Line-based edits
- `mcp__filesystem__create_directory` - Create directories
- `mcp__filesystem__list_directory` - List directory contents
- `mcp__filesystem__list_directory_with_sizes` - List with file sizes
- `mcp__filesystem__directory_tree` - Recursive tree view
- `mcp__filesystem__move_file` - Move/rename files
- `mcp__filesystem__search_files` - Search by pattern
- `mcp__filesystem__get_file_info` - Get file metadata
- `mcp__filesystem__list_allowed_directories` - List accessible paths

**Configuration Notes**:
- Scoped to da-agent-hub project only
- Cannot access files outside project root

#### 8. sequential-thinking
**Status**: ✅ ACTIVE
**Type**: Official Anthropic MCP
**Command**: `npx -y @modelcontextprotocol/server-sequential-thinking`
**Primary Users**: ALL specialists for complex problem-solving

**Tools Available**:
- `mcp__sequential-thinking__sequentialthinking` - Step-by-step reasoning with dynamic thought adjustment

**Configuration Notes**:
- Use for breaking down complex problems
- Supports hypothesis generation and verification
- Can revise previous thoughts mid-analysis

### ⏸️ KNOWN ISSUES

#### snowflake-mcp
**Status**: ⏸️ CONNECTION FAILING
**Launch Script**: `scripts/launch-snowflake-mcp.sh`
**Primary Specialist**: `snowflake-expert`
**Issue**: Authentication or connection problem (needs investigation)
**Workaround**: Use `scripts/debug-snowflake.sh` for direct Snowflake queries

**Expected Tools** (when fixed):
- `mcp__snowflake-mcp__run_snowflake_query` - Execute SQL queries
- `mcp__snowflake-mcp__list_objects` - List databases/schemas/tables

**Action Required**: Debug and fix Snowflake MCP connection

### 🚧 NOT YET DEPLOYED

#### prefect-mcp
**Status**: 🚧 PLANNED (Week 6+)
**Primary Specialist**: `prefect-expert`
**Rationale**: Deferred - Prefect Cloud API complexity requires more research

#### tableau-mcp
**Status**: 🚧 PLANNED (Future)
**Primary Specialist**: `tableau-expert`
**Rationale**: No official Tableau MCP exists; would need custom development

#### dlthub-mcp / airbyte-mcp
**Status**: 🚧 CONCEPTUAL
**Primary Specialist**: `dlthub-expert`
**Rationale**: Ingestion tools have less need for real-time MCP access

## Specialist → MCP Tool Matrix

| Specialist | Primary MCP Servers | Secondary MCP Servers |
|---|---|---|
| **dbt-expert** | dbt-mcp, snowflake-mcp | github, sequential-thinking |
| **snowflake-expert** | snowflake-mcp, dbt-mcp | sequential-thinking |
| **orchestra-expert** | orchestra-mcp | github, sequential-thinking |
| **aws-expert** | aws-api, aws-docs | github, sequential-thinking |
| **github-sleuth-expert** | github | filesystem, sequential-thinking |
| **business-context** | slack | github (for issue context) |
| **documentation-expert** | github, slack | filesystem |
| **data-quality-specialist** | dbt-mcp, snowflake-mcp | github, sequential-thinking |
| **cost-optimization-specialist** | snowflake-mcp, aws-api, dbt-mcp | sequential-thinking |
| **prefect-expert** | (future: prefect-mcp) | github, sequential-thinking |
| **tableau-expert** | (future: tableau-mcp) | snowflake-mcp, dbt-mcp |
| **react-expert** | github, aws-api | filesystem |
| **streamlit-expert** | github, aws-api | filesystem |
| **dlthub-expert** | github | sequential-thinking |

## MCP Health Check Protocol

### At Session Start

**MANDATORY**: Run MCP health check at the start of EVERY Claude Code session:

```bash
claude mcp list
```

**Expected Output**:
```
dbt-mcp: ✓ Connected
orchestra-mcp: ✓ Connected
snowflake-mcp: ✗ Failed to connect (KNOWN ISSUE)
aws-api: ✓ Connected
aws-docs: ✓ Connected
github: ✓ Connected
slack: ✓ Connected
filesystem: ✓ Connected
sequential-thinking: ✓ Connected
```

**If ANY unexpected failures**:
1. Check launch script: `tail /tmp/{server}-mcp-debug.log`
2. Verify credentials: `echo ${#CREDENTIAL_VAR_NAME}` (should be >0)
3. Test manually: `bash scripts/launch-{server}-mcp.sh` (watch for errors)
4. See troubleshooting runbook: `.claude/memory/patterns/mcp-troubleshooting-runbook.md`

### Ongoing Verification

When specialists use MCP tools:
1. **First call to tool**: If it fails, immediately check `claude mcp list`
2. **Document pattern**: If failure repeats, add to troubleshooting runbook
3. **Report to user**: Never claim MCP is working if tools fail

## Common Mistakes & Fixes

### ❌ Mistake 1: Assuming cloud.getdbt.com for All Instances
**Wrong**: Using default dbt Cloud host
**Right**: Check login URL to determine multi-tenant vs single-tenant
**Fix**: Set `DBT_HOST` in launch script based on actual instance

### ❌ Mistake 2: Not Restarting Claude After Launch Script Changes
**Wrong**: Killing MCP process and relaunching
**Right**: Fully quit and restart Claude Code application
**Why**: MCP servers connect on Claude Code launch, not chat session start

### ❌ Mistake 3: Saying "MCP is working" Without Testing
**Wrong**: Checking `claude mcp list` shows "Connected" and assuming tools work
**Right**: Actually call an MCP tool and verify response
**Why**: Connection != functional tools (see dbt-mcp 401 error example)

### ❌ Mistake 4: Not Checking Debug Logs on Failure
**Wrong**: Retrying tool call repeatedly
**Right**: Immediately check `/tmp/{server}-mcp-debug.log` for error details
**Why**: Debug logs reveal root cause (wrong host, missing credentials, etc.)

## References

- **Multi-tenant dbt Cloud**: `.claude/memory/patterns/dbt-cloud-multi-tenant-host-pattern.md`
- **GitHub Repo Resolution**: `.claude/memory/patterns/github-repo-context-resolution.md`
- **MCP Addition Protocol**: `.claude/memory/patterns/mcp-server-addition-protocol.md`
- **Agent MCP Integration**: `.claude/memory/patterns/agent-mcp-integration-guide.md`

## Enforcement

**This document is the source of truth for MCP-Specialist mappings.**
When specialists are consulted, they MUST:
1. Know which MCP servers they have access to
2. Use those MCP tools for real-time data validation
3. Report tool failures immediately (don't silently fall back)
4. Reference this document when uncertain about available tools

**When updating**:
- Add new MCP servers here FIRST
- Update specialist agent files to reference this mapping
- Test thoroughly before claiming "MCP is working"
- Document any gotchas in troubleshooting section
