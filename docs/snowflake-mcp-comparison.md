# Snowflake MCP Server Comparison: Community vs Managed

## Overview

Snowflake provides **two distinct MCP approaches** for integrating AI assistants with Snowflake data:

1. **Community Server** (`snowflake-labs-mcp`) - Open-source, locally-run server
2. **Managed Server** - Snowflake-hosted, Cortex-focused service

This document compares both approaches to help determine the best integration strategy.

---

## Community Server (`snowflake-labs-mcp`)

### What It Is
Open-source MCP server from Snowflake Labs that runs locally and provides comprehensive Snowflake API access through the Model Context Protocol.

### Architecture
```
Claude Code (MCP Host)
    ↓
Local MCP Client
    ↓
snowflake-labs-mcp (Local Server via uvx)
    ↓
Snowflake REST API + Connector
    ↓
Snowflake Account
```

### Authentication
- **Key Pair Authentication** (RSA private key)
- **OAuth** (via JWT tokens)
- Environment variables for credentials
- More secure for developer workflows

### Configuration
```json
// .claude/mcp.json
{
  "snowflake-mcp": {
    "command": "bash",
    "args": ["scripts/launch-snowflake-mcp.sh"],
    "disabled": false
  }
}
```

```yaml
# config/snowflake_tools_config.yaml
connection:
  database: ANALYTICS_DW
  schema: PROD_SALES_DM
  warehouse: TABLEAU_WH
  role: DEVELOPER

agent_services: []
search_services: []
analyst_services: []

other_services:
  object_manager: true
  query_manager: true
  semantic_manager: true

sql_statement_permissions:
  Select: true
  Describe: true
  Use: true
  # ... restrictive by default
```

### Available Tools (26+)
- **Object Management**: Database, schema, table, view operations
- **Query Execution**: Direct SQL execution with permission controls
- **Semantic Views**: Discovery and querying of semantic models
- **Cortex Services**: Agent, Search, Analyst (if configured)
- **Metadata Access**: Information schema queries
- **Data Operations**: INSERT, UPDATE, DELETE (if enabled)

### Pros
✅ **Comprehensive access** to all Snowflake objects and operations
✅ **Granular permission control** via SQL statement permissions
✅ **Works with any Snowflake account** (no special setup required)
✅ **Offline configuration** (runs locally, no additional costs)
✅ **Open-source** and community-supported
✅ **Key pair authentication** (more secure than PAT for dev workflows)
✅ **Full SQL capabilities** (DDL, DML, DQL with controls)
✅ **Works with Claude Code, Cursor, Anthropic Desktop**

### Cons
❌ **Local dependency** (requires uvx/uv installation)
❌ **Manual setup** (key pair generation, environment config)
❌ **YAML configuration** can be error-prone (as we discovered)
❌ **No native Cortex integration** (requires manual service setup)
❌ **Version management** (need to update via uvx)

### Best For
- **Data engineers** building dbt models, managing schemas
- **Analytics engineers** exploring data, writing SQL transformations
- **Developers** needing full Snowflake API access
- **Security-conscious teams** (key pair auth, local control)
- **Production automation** (scheduled tasks, orchestration)

---

## Managed MCP Server (Snowflake-Hosted)

### What It Is
Snowflake-managed MCP service accessed via REST API, purpose-built for Cortex AI tools (Analyst, Search, Agent).

### Architecture
```
Claude Code/Cursor (MCP Host)
    ↓
MCP Client (REST)
    ↓
Snowflake MCP REST API Endpoint
    ↓
Snowflake-Managed MCP Server
    ↓
Cortex Services (Analyst, Search, Agent)
```

### Authentication
- **Programmatic Access Token (PAT)** via SQL
- Service user with role restrictions
- Network policy required (IP allowlisting)

### Configuration
```sql
-- Step 1: Create service user and PAT
CREATE USER CORTEX_USER TYPE=SERVICE;
GRANT ROLE CORTEX_ROLE TO USER CORTEX_USER;

ALTER USER cortex_user ADD PROGRAMMATIC ACCESS TOKEN mcp_token
  ROLE_RESTRICTION = 'CORTEX_ROLE';

-- Step 2: Create MCP Server in Snowflake
USE SNOWFLAKE_INTELLIGENCE.TOOLS;

CREATE OR REPLACE MCP SERVER snowflake_mcp_server
FROM SPECIFICATION $$
tools:
  - name: "Snowflake Documentation Search"
    identifier: "SNOWFLAKE_DOCUMENTATION.SHARED.CKE_SNOWFLAKE_DOCS_SERVICE"
    type: "CORTEX_SEARCH_SERVICE_QUERY"
    description: "Tool for Snowflake documentation and code help."

  - name: "query_semantic_view"
    type: "CORTEX_ANALYST_MESSAGE"
    identifier: "SNOWFLAKE_INTELLIGENCE.TOOLS.COST_PERFORMANCE_ASSISTANT_SVW"
    description: "Semantic view for all queries executed in Snowflake"
config:
  warehouse: "cortex_wh"
$$;
```

```json
// Cursor/Claude Code mcp.json
{
  "Snowflake": {
    "url": "https://{org}-{account}.snowflakecomputing.com/api/v2/database-mcp-servers/snowflake_mcp_server",
    "headers": {
      "Authorization": "Bearer {PAT_TOKEN}"
    }
  }
}
```

### Available Tools
- **Cortex Analyst** - Natural language to SQL queries
- **Cortex Search** - Semantic search across documentation/data
- **Cortex Agent** - Custom AI agents with tools
- **Semantic Views** - Pre-defined business logic queries

### Pros
✅ **No local setup** (hosted by Snowflake)
✅ **Zero cost** (no additional charges for MCP server)
✅ **Native Cortex integration** (Analyst, Search, Agent)
✅ **Managed updates** (Snowflake maintains the server)
✅ **REST API access** (works from any HTTP client)
✅ **Business-user friendly** (natural language queries via Cortex Analyst)
✅ **Semantic layer** (pre-defined business logic)
✅ **Governance built-in** (Snowflake RBAC applies)

### Cons
❌ **Cortex-only focus** (limited to Cortex services)
❌ **Requires Cortex setup** (Analyst, Search services must exist)
❌ **PAT authentication** (less secure than key pairs for dev)
❌ **Network policies required** (IP allowlisting overhead)
❌ **Less granular control** (can't customize SQL permissions per tool)
❌ **Requires Snowflake Intelligence schema** (additional setup)
❌ **Not suitable for DDL/DML** (read-only Cortex focus)

### Best For
- **Business users** asking natural language questions
- **BI analysts** exploring semantic models
- **Cortex-heavy workloads** (Analyst, Search, Agent)
- **Non-technical teams** (no local setup required)
- **Cursor users** (simpler REST-based integration)
- **Production analytics apps** (Streamlit + Cortex integration)

---

## Side-by-Side Comparison

| Feature | Community Server | Managed Server |
|---------|------------------|----------------|
| **Hosting** | Local (via uvx) | Snowflake-hosted |
| **Authentication** | Key pair / OAuth | PAT (Programmatic Access Token) |
| **Setup Complexity** | Medium (key pairs, YAML config) | Low (SQL + REST config) |
| **Tool Count** | 26+ comprehensive tools | 2-4 Cortex-focused tools |
| **SQL Capabilities** | Full DDL/DML/DQL (configurable) | Read-only (Cortex queries) |
| **Cortex Integration** | Manual setup | Native built-in |
| **Cost** | Free (open-source) | Free (no additional charges) |
| **Use Case** | Data engineering, development | Business analytics, BI |
| **Security Model** | Key pair (more secure) | PAT + network policy |
| **Updates** | Manual (uvx update) | Automatic (Snowflake-managed) |
| **AI Assistants** | Claude Code, Cursor, Desktop | Claude Code, Cursor, Desktop |
| **Best For** | Developers, engineers | Business users, analysts |

---

## Recommendation: Use Both

### Why Both?

**They serve different purposes:**

1. **Community Server** → Development, engineering, transformation work
   - dbt model development
   - Schema management
   - SQL exploration and testing
   - Data quality validation
   - Orchestration scripting

2. **Managed Server** → Business analytics, semantic queries, BI work
   - Natural language queries via Cortex Analyst
   - Semantic view exploration
   - Business user self-service
   - Documentation search
   - Production analytics apps

### Implementation Strategy

#### Phase 1: Community Server (Current - COMPLETE ✅)
```
Status: OPERATIONAL
- snowflake-labs-mcp configured via wrapper script
- Key pair authentication working
- 26 tools available
- YAML config fixed (removed "1#" prefix)
- Integration with snowflake-expert, dbt-expert agents
```

#### Phase 2: Managed Server (Optional - High Value)
```
Prerequisites:
1. Create Cortex Analyst service (semantic model for query history)
2. Create Cortex Search service (Snowflake docs or custom data)
3. Create service user + PAT token
4. Configure network policy

Steps:
1. Run SQL to create MCP server in Snowflake
2. Add managed server to .claude/mcp.json (separate entry)
3. Test with business-focused prompts
4. Document use cases for each server
```

### Configuration Example (Both Servers)

```json
// .claude/mcp.json
{
  "mcpServers": {
    "snowflake-mcp": {
      "command": "bash",
      "args": ["scripts/launch-snowflake-mcp.sh"],
      "disabled": false
    },
    "snowflake-cortex": {
      "url": "https://graniterock-fc41459.snowflakecomputing.com/api/v2/database-mcp-servers/cortex_mcp_server",
      "headers": {
        "Authorization": "Bearer ${SNOWFLAKE_CORTEX_PAT}"
      },
      "disabled": false
    }
  }
}
```

### Agent Delegation Strategy

**snowflake-expert agent:**
- **Primary**: Community server (full SQL, schema management)
- **Fallback**: Managed server (business queries, semantic models)

**Prompt routing:**
```
"Show me top 10 slowest queries" → Managed server (Cortex Analyst)
"CREATE TABLE sales_summary AS SELECT..." → Community server (DDL)
"What warehouse size should I use?" → Community server (metadata queries)
"Explain our revenue trends" → Managed server (semantic view)
```

---

## Known Issues & Resolutions

### Community Server

**Issue**: YAML syntax error - `expected '<document start>', but found '<block mapping start>'`
**Cause**: File started with `1# Snowflake MCP Server...` instead of `#`
**Fix**: Remove "1" prefix from first line of `config/snowflake_tools_config.yaml`

**Issue**: Claude Code MCP config doesn't expand `${VAR}` in args array
**Solution**: Created wrapper script `scripts/launch-snowflake-mcp.sh` that inherits env vars

**Issue**: Deprecation warnings from Pydantic
**Solution**: Filtered with `grep -v PydanticDeprecatedSince20` in wrapper script

### Managed Server

**Issue**: PAT token requires network policy
**Concern**: Open internet policy (`0.0.0.0/0`) is insecure
**Recommendation**: Use VPN/ISP IP ranges instead

---

## References

- **Medium Article**: "Bringing AI to Your Data: Integrating Cursor with Snowflake MCP Server" by Umesh Patel
- **Community Server**: https://github.com/Snowflake-Labs/mcp-server-snowflake
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Snowflake Cortex**: https://docs.snowflake.com/en/user-guide/snowflake-cortex

---

## Decision Log

**2025-10-08**: Snowflake community MCP operational (7/8 servers connected)
**Next**: Evaluate Cortex service setup for managed MCP integration

---

*This document will be updated as we integrate the managed server approach.*
