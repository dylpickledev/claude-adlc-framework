# dbt-mcp Server Capabilities - Comprehensive Documentation

**Research Date:** 2025-10-08
**Version:** Based on dbt-mcp official documentation and blog posts
**Official Repo:** https://github.com/dbt-labs/dbt-mcp
**PyPI Package:** https://pypi.org/project/dbt-mcp/

---

## Executive Summary

The **dbt Model Context Protocol (MCP) server** is an official dbt Labs product that provides AI agents with structured, governed access to dbt-managed data assets. It exposes various tools across seven categories: Discovery, Semantic Layer, Administrative API, SQL Execution, CLI Commands, Fusion (advanced lineage), and Code Generation.

**Key Value Propositions:**
- **Discovery**: Autonomous metadata exploration (models, relationships, column-level lineage)
- **Semantic Layer**: Query validated business metrics directly from source of truth
- **SQL Execution**: Text-to-SQL generation and execution with governance
- **CLI Access**: Run dbt commands (build, test, run, compile) through AI agents
- **Administration**: Trigger and monitor dbt Cloud jobs programmatically
- **Code Generation**: Automate boilerplate YAML generation for sources and models
- **Fusion**: Advanced column-level lineage analysis (Fusion engine exclusive)

---

## Server Architectures

### Local MCP Server

**Purpose**: Development-focused, runs locally on developer machine
**Best For**: IDE integrations (Cursor, Claude Code, VS Code)
**Configuration**: Environment variables in `.env` file
**Requirements**: Python, uv package manager, local dbt project

**Pros:**
- Access to local dbt project state (uncommitted changes)
- Full dbt CLI command support
- Lower latency for local development
- No dbt Cloud plan requirements for CLI/Discovery features

**Cons:**
- Single-tenant (one user at a time)
- Requires local infrastructure setup
- Limited to development workflows

### Remote MCP Server

**Purpose**: Production-ready, multi-tenant hosted by dbt Cloud
**Best For**: Web applications, server-side agents, team collaboration
**Configuration**: HTTP headers for authentication
**Requirements**: dbt Starter, Enterprise, or Enterprise+ plan

**Pros:**
- No local installation required
- Multi-tenant with isolated connections
- Supports long-running tasks
- Accessible via web applications
- Managed infrastructure by dbt Labs

**Cons:**
- Requires paid dbt Cloud plan
- Limited Fusion tool access compared to local
- Network latency for API calls

**Key Architectural Difference:**
- Local: Configured via environment variables
- Remote: Configured via HTTP headers with direct API connections

---

## Complete Tool Inventory

### 1. Discovery API Tools

**Purpose**: Metadata exploration and project structure understanding
**Enable/Disable**: `DISABLE_DISCOVERY` environment variable (default: `false` - enabled)
**Plan Requirements**: Available in all dbt Cloud plans

#### `get_all_models`
**Description**: Provides complete inventory of all models in dbt project
**Parameters**: None
**Returns**: List of all model names and descriptions
**Use Cases**:
- Initial project exploration
- Comprehensive model cataloging
- AI agent project structure learning

**Example Use**:
```
Agent: "What models are available in this dbt project?"
→ get_all_models returns: [customers, orders, order_items, products, ...]
```

---

#### `get_mart_models`
**Description**: Identifies presentation layer models for end-user consumption
**Parameters**: None
**Returns**: List of mart model names and descriptions
**Use Cases**:
- Finding business-facing models
- Identifying consumption layer assets
- Determining which models to expose to BI tools

**Example Use**:
```
Agent: "Which models are ready for business users?"
→ get_mart_models returns: [fct_orders, dim_customers, agg_monthly_revenue, ...]
```

---

#### `get_model_details`
**Description**: Retrieves comprehensive information about a specific model
**Parameters**:
- `model_name` (required): Name of the model to inspect

**Returns**:
- Compiled SQL
- Description
- Column names
- Column descriptions
- Data types
- Other metadata

**Use Cases**:
- Understanding model logic
- Analyzing transformation steps
- Documenting model behavior
- Code review and analysis

**Example Use**:
```
Agent: "Show me details for the fct_orders model"
→ get_model_details(model_name="fct_orders") returns:
  {
    "compiled_sql": "SELECT ...",
    "description": "Fact table of all orders",
    "columns": [
      {"name": "order_id", "type": "NUMBER", "description": "Primary key"},
      {"name": "customer_id", "type": "NUMBER", "description": "FK to dim_customers"},
      ...
    ]
  }
```

---

#### `get_model_parents`
**Description**: Identifies upstream dependencies for a specific model
**Parameters**:
- `model_name` (required): Name of the model to analyze

**Returns**: List of parent models that the specified model depends on
**Use Cases**:
- Impact analysis (what feeds this model?)
- Debugging data flow issues
- Understanding transformation lineage
- Planning model updates

**Example Use**:
```
Agent: "What models does fct_orders depend on?"
→ get_model_parents(model_name="fct_orders") returns: [stg_orders, stg_customers, stg_products]
```

---

#### `get_model_children`
**Description**: Identifies downstream models that depend on a specific model
**Parameters**:
- `model_name` (required): Name of the model to analyze

**Returns**: List of child models that depend on the specified model
**Use Cases**:
- Impact analysis (what will break if I change this model?)
- Change management
- Dependency mapping
- Refactoring planning

**Example Use**:
```
Agent: "What models depend on stg_orders?"
→ get_model_children(model_name="stg_orders") returns: [fct_orders, fct_returns, int_order_metrics]
```

---

### 2. Semantic Layer Tools

**Purpose**: Query validated business metrics and dimensions
**Enable/Disable**: `DISABLE_SEMANTIC_LAYER` environment variable (default: `false` - enabled)
**Plan Requirements**: dbt Cloud Team or Enterprise (Semantic Layer access required)

#### `list_metrics`
**Description**: Provides inventory of metrics in dbt Semantic Layer
**Parameters**: None
**Returns**: Complete list of metric names, types, labels, descriptions
**Use Cases**:
- Discovering available metrics
- Understanding metric definitions
- Cataloging business KPIs

**Example Use**:
```
Agent: "What metrics are available for revenue analysis?"
→ list_metrics returns:
  [
    {"name": "revenue", "type": "sum", "label": "Total Revenue", "description": "Sum of order totals"},
    {"name": "avg_order_value", "type": "average", "label": "Average Order Value", "description": "Average revenue per order"},
    ...
  ]
```

---

#### `get_dimensions`
**Description**: Identifies available dimensions for specified metrics
**Parameters**:
- `metric_names` (required): List of metric names to query

**Returns**: List of dimensions for grouping/filtering metrics
**Use Cases**:
- Determining how to slice metrics
- Building dynamic filters
- Understanding metric granularity

**Example Use**:
```
Agent: "How can I break down revenue metrics?"
→ get_dimensions(metric_names=["revenue", "avg_order_value"]) returns:
  ["customer_region", "product_category", "order_date", "customer_segment"]
```

---

#### `query_metrics`
**Description**: Executes queries against metrics in dbt Semantic Layer
**Parameters**:
- `metrics` (required): List of metric names to query
- `group_by` (optional): List of dimensions to group by
- `where` (optional): Filter conditions (e.g., "customer_region = 'West'")
- `start_time` (optional): Date range start
- `end_time` (optional): Date range end
- `limit` (optional): Maximum rows to return
- `order_by` (optional): Sort specification

**Returns**: Query results based on specified metrics, dimensions, filters
**Use Cases**:
- Answering metric-focused questions
- Building reports from governed metrics
- Analyzing KPI trends
- Executive dashboards

**Example Use**:
```
Agent: "Show last quarter's revenue trends by region"
→ query_metrics(
    metrics=["revenue"],
    group_by=["customer_region", "order_date__month"],
    where="order_date >= '2024-07-01' AND order_date <= '2024-09-30'",
    order_by="-order_date__month"
  ) returns:
  [
    {"customer_region": "West", "month": "2024-09", "revenue": 125000},
    {"customer_region": "East", "month": "2024-09", "revenue": 98000},
    ...
  ]
```

---

#### `get_metrics_compiled_sql`
**Description**: Returns the compiled SQL generated for specified metrics and groupings WITHOUT executing the query
**Parameters**:
- `metrics` (required): List of metric names
- `group_by` (optional): List of dimensions

**Returns**: Compiled SQL query text
**Use Cases**:
- Understanding metric calculations
- Debugging metric logic
- Sharing SQL with non-MCP tools
- Documentation and training

**Example Use**:
```
Agent: "Show me the SQL behind the revenue metric"
→ get_metrics_compiled_sql(metrics=["revenue"], group_by=["customer_region"]) returns:
  "SELECT customer_region, SUM(order_total) as revenue FROM fct_orders GROUP BY customer_region"
```

---

### 3. SQL Execution Tools

**Purpose**: Natural language to SQL and direct SQL execution
**Enable/Disable**: `DISABLE_SQL` environment variable (default: `true` - disabled by default for safety)
**Plan Requirements**: dbt Cloud account with appropriate database permissions
**Authentication Note**: Requires Personal Access Token (PAT), NOT service token

⚠️ **CRITICAL SECURITY NOTE**: SQL execution tools can modify data. Enable only when necessary and with appropriate governance.

#### `text_to_sql`
**Description**: Generates SQL from natural language requests
**Parameters**:
- `question` (required): Natural language query description
- `context` (optional): Additional context about tables/schemas

**Returns**: Generated SQL query
**Use Cases**:
- Rapid query prototyping
- Ad-hoc analysis by non-SQL users
- Exploration of unfamiliar datasets

**Example Use**:
```
Agent: "Create SQL to find top 10 customers by total revenue"
→ text_to_sql(question="top 10 customers by total revenue") returns:
  "SELECT customer_id, SUM(order_total) as total_revenue
   FROM fct_orders
   GROUP BY customer_id
   ORDER BY total_revenue DESC
   LIMIT 10"
```

---

#### `execute_sql`
**Description**: Executes SQL on the dbt platform's backend infrastructure with support for Semantic Layer SQL syntax
**Parameters**:
- `sql` (required): SQL query to execute
- `timeout` (optional): Execution timeout in seconds

**Returns**: Query results
**Use Cases**:
- Running generated SQL queries
- Ad-hoc data exploration
- Validation of model outputs
- Custom analysis

**Example Use**:
```
Agent: "Run this query: SELECT COUNT(*) FROM fct_orders WHERE order_date = CURRENT_DATE"
→ execute_sql(sql="SELECT COUNT(*) FROM fct_orders WHERE order_date = CURRENT_DATE") returns:
  [{"count": 42}]
```

---

#### `compile_sql`
**Description**: Compiles a SQL statement in the context of the current project and environment WITHOUT executing
**Parameters**:
- `sql` (required): SQL to compile (can include Jinja/macros)

**Returns**: Compiled SQL text
**Use Cases**:
- Validating Jinja macro expansion
- Understanding ref() and source() resolution
- Debugging compilation errors
- Learning dbt SQL patterns

**Example Use**:
```
Agent: "Compile this dbt SQL: SELECT * FROM {{ ref('stg_orders') }}"
→ compile_sql(sql="SELECT * FROM {{ ref('stg_orders') }}") returns:
  "SELECT * FROM analytics.staging.stg_orders"
```

---

### 4. dbt CLI Commands

**Purpose**: Execute standard dbt CLI operations through AI agents
**Enable/Disable**: `DISABLE_DBT_CLI` environment variable (default: `false` - enabled)
**Plan Requirements**: dbt Core or dbt Cloud with local project access
**Local MCP Only**: Full CLI support primarily available in local MCP server

#### `build`
**Description**: Executes models, tests, snapshots, and seeds in dependency order
**Parameters**:
- `selector` (optional): dbt selector syntax (e.g., "tag:daily")
- `full_refresh` (optional): Boolean for full refresh
- Additional standard dbt CLI flags

**Use Cases**:
- Full project builds
- Coordinated execution of all dbt resources
- Production deployment workflows

**Example Use**:
```
Agent: "Build all models tagged 'daily'"
→ build(selector="tag:daily")
```

---

#### `run`
**Description**: Executes your compiled SQL models against target database
**Parameters**:
- `selector` (optional): dbt selector syntax
- `full_refresh` (optional): Boolean
- `models` (optional): Specific models to run

**Use Cases**:
- Running specific models
- Incremental model updates
- Scheduled transformations

**Example Use**:
```
Agent: "Run the fct_orders model"
→ run(models="fct_orders")
```

---

#### `test`
**Description**: Runs data tests defined on models, sources, snapshots, seeds
**Parameters**:
- `selector` (optional): dbt selector syntax
- `models` (optional): Test specific models

**Use Cases**:
- Data quality validation
- Pre-deployment testing
- Regression detection

**Example Use**:
```
Agent: "Test all staging models"
→ test(selector="staging.*")
```

---

#### `compile`
**Description**: Generates executable SQL from models, tests, and analyses without running them
**Parameters**:
- `selector` (optional): dbt selector syntax
- `models` (optional): Specific models to compile

**Use Cases**:
- Validating SQL logic
- Reviewing generated queries
- Debugging compilation errors

**Example Use**:
```
Agent: "Compile the fct_orders model"
→ compile(models="fct_orders")
```

---

#### `parse`
**Description**: Parses the project and checks if your project is correctly structured
**Parameters**: None
**Use Cases**:
- Project validation
- CI/CD pre-checks
- Dependency resolution

---

#### `show`
**Description**: Compiles the dbt-SQL definition and previews results for a single model/test/analysis
**Parameters**:
- `selector` (required): Specific resource to show

**Use Cases**:
- Quick data previews
- Ad-hoc model testing
- Development iteration

**Example Use**:
```
Agent: "Show me preview of stg_customers"
→ show(selector="stg_customers")
```

---

#### `list`
**Description**: Lists all resources in dbt project
**Parameters**:
- `resource_type` (optional): Filter by type (models, tests, sources, etc.)

**Use Cases**:
- Project inventory
- Resource discovery
- Documentation generation

---

### 5. Administrative API Tools

**Purpose**: Manage dbt Cloud jobs and runs programmatically
**Enable/Disable**: `DISABLE_ADMIN_API` environment variable (default: `false` - enabled)
**Plan Requirements**: dbt Cloud with API access
**Authentication**: Service token or Personal Access Token

#### `trigger_job_run`
**Description**: Triggers a dbt Cloud job run with optional parameter overrides
**Parameters**:
- `job_id` (required): ID of the job to trigger
- `git_branch` (optional): Override Git branch
- `schema_override` (optional): Override target schema
- `dbt_version_override` (optional): Override dbt version
- `threads_override` (optional): Override thread count
- `target_name_override` (optional): Override target name
- `generate_docs_override` (optional): Boolean to generate docs
- `timeout_seconds_override` (optional): Override timeout
- `steps_override` (optional): Override execution steps

**Returns**: Job run ID and initial status
**Use Cases**:
- Scheduled orchestration
- Event-driven pipeline triggers
- Testing with different configurations
- Parameterized deployments

**Example Use**:
```
Agent: "Trigger daily_analytics job on feature branch"
→ trigger_job_run(job_id=12345, git_branch="feature/new-metrics") returns:
  {"run_id": 67890, "status": "Running"}
```

---

#### `list_jobs_runs`
**Description**: Lists runs in an account with optional filtering
**Parameters**:
- `job_id` (optional): Filter by specific job
- `status` (optional): Filter by status (Success, Error, Cancelled, Running)
- `order_by` (optional): Sort specification
- `limit` (optional): Maximum runs to return

**Returns**: List of job runs with metadata
**Use Cases**:
- Monitoring pipeline health
- Historical analysis
- Failure investigation
- Performance tracking

**Example Use**:
```
Agent: "Show last 10 failed runs"
→ list_jobs_runs(status="Error", limit=10, order_by="-finished_at")
```

---

#### `get_job_run_details`
**Description**: Gets comprehensive run information including execution details, steps, artifacts, debug logs
**Parameters**:
- `run_id` (required): ID of the run to inspect

**Returns**:
- Run status and timing
- Execution steps
- Artifact references
- Debug logs
- Error messages (if any)

**Use Cases**:
- Debugging failed runs
- Performance analysis
- Audit logging
- Root cause analysis

**Example Use**:
```
Agent: "Why did run 67890 fail?"
→ get_job_run_details(run_id=67890) returns detailed failure context
```

---

#### `cancel_job_run`
**Description**: Cancels a running job to stop execution
**Parameters**:
- `run_id` (required): ID of the run to cancel

**Use Cases**:
- Stopping runaway jobs
- Emergency pipeline halts
- Resource management

---

#### `retry_job_run`
**Description**: Retries a failed or cancelled job run
**Parameters**:
- `run_id` (required): ID of the run to retry

**Use Cases**:
- Recovering from transient failures
- Resuming cancelled jobs

---

#### `list_job_run_artifacts`
**Description**: Lists all available artifacts for a job run (manifest.json, catalog.json, logs, etc.)
**Parameters**:
- `run_id` (required): ID of the run

**Returns**: List of artifact names and paths
**Use Cases**:
- Artifact discovery
- Automated artifact processing
- Documentation generation

**Example Use**:
```
Agent: "What artifacts are available from run 67890?"
→ list_job_run_artifacts(run_id=67890) returns:
  ["manifest.json", "catalog.json", "run_results.json", "compiled/", "logs/"]
```

---

#### `get_job_run_artifact`
**Description**: Downloads specific artifact files from job runs for analysis or integration
**Parameters**:
- `run_id` (required): ID of the run
- `artifact_path` (required): Path to artifact (e.g., "manifest.json")

**Returns**: Artifact content
**Use Cases**:
- Automated lineage extraction
- Documentation generation
- External tool integration
- Historical analysis

**Example Use**:
```
Agent: "Get the manifest from run 67890"
→ get_job_run_artifact(run_id=67890, artifact_path="manifest.json") returns JSON manifest
```

---

### 6. Code Generation (Codegen) Tools

**Purpose**: Automate boilerplate YAML generation for dbt projects
**Enable/Disable**: `DISABLE_DBT_CODEGEN` environment variable (default: `true` - disabled)
**Requirements**: dbt-codegen package installed in dbt project
**Plan Requirements**: Works with dbt Core and dbt Cloud

⚠️ **Important**: These tools require installing the dbt-codegen package in your dbt project:
```yaml
# packages.yml
packages:
  - package: dbt-labs/codegen
    version: 0.12.1
```

#### `generate_source`
**Description**: Creates source YAML definitions from database schemas
**Parameters**:
- `schema_name` (required): Database schema to document
- `database_name` (optional): Database name
- `generate_columns` (optional): Boolean to include column definitions (default: true)
- `include_descriptions` (optional): Boolean to include description placeholders

**Returns**: Generated source YAML text
**Use Cases**:
- Onboarding new data sources
- Documenting existing schemas
- Reducing manual YAML writing
- Standardizing source definitions

**Example Use**:
```
Agent: "Generate source YAML for the raw_shopify schema"
→ generate_source(schema_name="raw_shopify") returns:
  version: 2
  sources:
    - name: raw_shopify
      tables:
        - name: orders
          columns:
            - name: id
            - name: customer_id
            - name: order_date
        - name: customers
          columns:
            - name: id
            - name: email
```

---

#### `generate_model_yaml`
**Description**: Generates documentation YAML for existing dbt models
**Parameters**:
- `model_names` (required): List of model names to document
- `upstream_descriptions` (optional): Boolean to pull descriptions from upstream models

**Returns**: Generated model documentation YAML
**Use Cases**:
- Kickstarting documentation efforts
- Standardizing model YAML structure
- Migrating undocumented models
- Documentation templates

**Example Use**:
```
Agent: "Generate documentation YAML for fct_orders and dim_customers"
→ generate_model_yaml(model_names=["fct_orders", "dim_customers"]) returns:
  version: 2
  models:
    - name: fct_orders
      columns:
        - name: order_id
        - name: customer_id
        - name: order_date
    - name: dim_customers
      columns:
        - name: customer_id
        - name: customer_name
```

---

#### `generate_staging_model`
**Description**: Creates staging SQL models from sources to transform raw source data into clean staging models
**Parameters**:
- `source_name` (required): Name of the source
- `table_name` (required): Name of the table within the source

**Returns**: Generated staging model SQL
**Use Cases**:
- Accelerating staging layer development
- Standardizing staging patterns
- Onboarding new sources
- Reducing boilerplate code

**Example Use**:
```
Agent: "Generate staging model for raw_shopify.orders"
→ generate_staging_model(source_name="raw_shopify", table_name="orders") returns:
  with source as (
    select * from {{ source('raw_shopify', 'orders') }}
  ),
  renamed as (
    select
      id as order_id,
      customer_id,
      order_date,
      ...
    from source
  )
  select * from renamed
```

---

### 7. Fusion Tools (Advanced Lineage)

**Purpose**: Advanced column-level lineage analysis
**Enable/Disable**: Cannot be disabled (always available when Fusion engine active)
**Requirements**: dbt Fusion engine (dbt Cloud Enterprise feature)
**Plan Requirements**: dbt Cloud Enterprise with Fusion enabled

⚠️ **Fusion Exclusive**: These tools ONLY work with the dbt Fusion execution engine, not standard dbt Core.

#### `get_column_lineage`
**Description**: Gets column lineage information across a project DAG for a specific column
**Parameters**:
- `model_name` (required): Model containing the column
- `column_name` (required): Column to trace lineage for

**Returns**: Complete column lineage graph showing upstream sources and transformations
**Use Cases**:
- Impact analysis at column level
- Regulatory compliance (data lineage requirements)
- Understanding derived calculations
- Data governance documentation
- Root cause analysis for data quality issues

**Example Use**:
```
Agent: "Show me the lineage for the revenue column in fct_orders"
→ get_column_lineage(model_name="fct_orders", column_name="revenue") returns:
  {
    "target": {"model": "fct_orders", "column": "revenue"},
    "lineage": [
      {"model": "stg_orders", "column": "order_total", "transformation": "direct"},
      {"model": "raw_shopify.orders", "column": "total_price", "transformation": "renamed"},
      ...
    ]
  }
```

---

## Setup and Configuration

### Local MCP Server Setup

#### 1. Install Prerequisites
```bash
# Install uv (universal Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dbt-mcp
pip install dbt-mcp
```

#### 2. Create `.env` Configuration File

**Location**: Create `.env` file in your project or home directory

**Required Variables** (choose based on your use case):

**For dbt Cloud Platform Access:**
```bash
# dbt Cloud connection
DBT_HOST=cloud.getdbt.com
DBT_TOKEN=your-personal-access-token-or-service-token

# Environment identifiers
DBT_PROD_ENV_ID=12345
DBT_DEV_ENV_ID=67890

# User/Account context
DBT_USER_ID=your-user-id
DBT_ACCOUNT_ID=your-account-id

# Optional: Multi-cell instances
MULTICELL_ACCOUNT_PREFIX=your-account-prefix
```

**For Local dbt Core Projects:**
```bash
# Local project path
DBT_PROJECT_DIR=/path/to/your/dbt/project

# dbt executable path
DBT_PATH=/path/to/dbt/executable
```

**Tool Control Variables** (optional):
```bash
# Disable specific tool categories (set to 'true' to disable)
DISABLE_DBT_CLI=false           # dbt CLI commands
DISABLE_SEMANTIC_LAYER=false    # Semantic Layer tools
DISABLE_DISCOVERY=false         # Discovery API tools
DISABLE_ADMIN_API=false         # Administrative API tools
DISABLE_SQL=true                # SQL execution (disabled by default for safety)
DISABLE_DBT_CODEGEN=true        # Codegen tools (disabled by default, requires dbt-codegen package)
```

#### 3. Test Configuration
```bash
# Validate setup
uvx --env-file /path/to/.env dbt-mcp
```

#### 4. Configure MCP Client (Claude Desktop Example)

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "dbt-mcp": {
      "command": "uvx",
      "args": [
        "--env-file",
        "/Users/you/.env",
        "dbt-mcp"
      ]
    }
  }
}
```

### Remote MCP Server Setup

**Prerequisites**: dbt Starter, Enterprise, or Enterprise+ plan

**Configuration** (HTTP headers instead of env vars):
```python
import os
from mcp import ClientSession

url = f"https://{os.environ.get('DBT_HOST')}/api/ai/v1/mcp/"
headers = {
  "x-dbt-user-id": os.environ.get("DBT_USER_ID"),
  "x-dbt-prod-environment-id": os.environ.get("DBT_PROD_ENV_ID"),
  "x-dbt-dev-environment-id": os.environ.get("DBT_DEV_ENV_ID"),
  "Authorization": f"token {os.environ.get('DBT_TOKEN')}",
}

# Connect to remote MCP server
session = ClientSession(url, headers=headers)
```

---

## Authentication & Security

### Token Types

#### Personal Access Token (PAT)
**Purpose**: User-specific authentication
**Required For**: SQL execution tools (text_to_sql, execute_sql)
**Permissions**: Inherits user's dbt Cloud permissions
**Creation**: Account Settings → API Tokens → Personal Tokens
**Best For**: Development, individual workflows, IDE integrations

**Security Considerations**:
- Tied to individual user account
- Expires when user is removed
- Should not be shared
- Good for development, not production automation

#### Service Account Token
**Purpose**: System-level authentication
**Required For**: Most MCP operations (except SQL execution)
**Permissions**: Configurable with narrow permission sets
**Creation**: Account Settings → API Tokens → Service Tokens
**Best For**: Production automation, CI/CD pipelines, team-shared agents

**Security Considerations**:
- Not tied to individual user
- Persists across user changes
- Can have restricted permissions
- Ideal for production systems

### ⚠️ Critical Security Notes

1. **SQL Execution Risk**: `execute_sql` and `text_to_sql` tools CAN MODIFY DATA
   - Default: DISABLED (`DISABLE_SQL=true`)
   - Only enable with appropriate governance
   - Requires PAT (Personal Access Token), not service token
   - Consider read-only database roles where possible

2. **Token Management**:
   - NEVER commit `.env` files to version control
   - Use environment-specific tokens (dev vs prod)
   - Rotate tokens regularly
   - Monitor token usage in dbt Cloud

3. **Network Security**:
   - Local MCP: Runs on localhost (http://127.0.0.1)
   - Remote MCP: Uses HTTPS with dbt Cloud
   - Ensure secure transport for sensitive data

---

## Tool Availability Matrix

| Tool Category | Local MCP | Remote MCP | Plan Requirements | Default State |
|--------------|-----------|------------|-------------------|---------------|
| Discovery API | ✅ Full | ✅ Full | All plans | Enabled |
| Semantic Layer | ✅ Full | ✅ Full | Team/Enterprise | Enabled |
| SQL Execution | ✅ Full | ✅ Full | All plans + PAT | **Disabled** |
| dbt CLI Commands | ✅ Full | ⚠️ Limited | All plans | Enabled |
| Administrative API | ✅ Full | ✅ Full | All plans | Enabled |
| Code Generation | ✅ Full | ⚠️ Limited | All plans + codegen pkg | **Disabled** |
| Fusion Lineage | ✅ Full | ⚠️ Limited | Enterprise + Fusion | Always enabled |

**Legend**:
- ✅ Full: Complete feature support
- ⚠️ Limited: Partial support or reduced capabilities
- **Disabled**: Not enabled by default (must explicitly enable)

---

## Practical Use Cases by Role

### Analytics Engineer
**Primary Tools**: Discovery API, dbt CLI, Code Generation
**Common Workflows**:
1. Model exploration: `get_all_models` → `get_model_details`
2. Impact analysis: `get_model_parents` → `get_model_children`
3. Testing: `test` → `get_job_run_details`
4. Documentation: `generate_model_yaml` → commit to repo

**Example Session**:
```
"Show me all mart models" → get_mart_models
"What are the dependencies for fct_orders?" → get_model_parents
"Run tests on staging models" → test(selector="staging.*")
"Generate documentation for fct_orders" → generate_model_yaml
```

---

### Data Engineer
**Primary Tools**: Administrative API, dbt CLI, Discovery API
**Common Workflows**:
1. Pipeline orchestration: `trigger_job_run` with parameters
2. Monitoring: `list_jobs_runs` → filter failures → `get_job_run_details`
3. Artifact retrieval: `get_job_run_artifact` for manifest/catalog
4. Incident response: `cancel_job_run` for runaway jobs

**Example Session**:
```
"Trigger daily pipeline on production" → trigger_job_run
"Show me failed runs from last 24 hours" → list_jobs_runs(status="Error")
"Why did run 12345 fail?" → get_job_run_details(run_id=12345)
"Get the manifest from last successful run" → get_job_run_artifact
```

---

### Business Analyst
**Primary Tools**: Semantic Layer, SQL Execution
**Common Workflows**:
1. Metric discovery: `list_metrics` → filter by category
2. Data exploration: `text_to_sql` → `execute_sql`
3. Report building: `query_metrics` with dimensions
4. Validation: `get_metrics_compiled_sql` to understand calculations

**Example Session**:
```
"What revenue metrics are available?" → list_metrics
"Show me monthly revenue by region for Q3" → query_metrics
"Generate SQL to find top customers" → text_to_sql
"What's the calculation for avg_order_value?" → get_metrics_compiled_sql
```

---

### Data Architect
**Primary Tools**: Fusion Lineage, Discovery API, Administrative API
**Common Workflows**:
1. Lineage analysis: `get_column_lineage` for compliance
2. Project structure review: `get_all_models` → analyze patterns
3. Performance optimization: `get_job_run_details` → analyze timings
4. Governance: Review artifact contents for standards compliance

**Example Session**:
```
"Show column lineage for customer_id in fct_orders" → get_column_lineage
"What models feed into our revenue dashboard?" → get_model_children
"Analyze job performance trends" → list_jobs_runs + artifact analysis
```

---

### DevOps/Platform Engineer
**Primary Tools**: Administrative API, dbt CLI
**Common Workflows**:
1. CI/CD integration: `trigger_job_run` with branch overrides
2. Health monitoring: `list_jobs_runs` → alert on failures
3. Artifact archival: `get_job_run_artifact` → store in S3/GCS
4. Emergency response: `cancel_job_run` → investigate → `retry_job_run`

**Example Session**:
```
"Trigger job on feature branch for PR validation" → trigger_job_run(git_branch="feature/x")
"Monitor pipeline health" → list_jobs_runs(limit=50, order_by="-finished_at")
"Archive production artifacts" → get_job_run_artifact → upload to object storage
```

---

## Limitations and Edge Cases

### General Limitations

1. **Rate Limiting**
   - dbt Cloud API has rate limits
   - Excessive MCP calls may be throttled
   - Implement retry logic with exponential backoff

2. **Performance Considerations**
   - `get_all_models` can be slow on large projects (1000+ models)
   - `query_metrics` performance depends on underlying data platform
   - Discovery API calls require project compilation (can take 10-30s)

3. **Data Freshness**
   - Discovery API uses cached artifacts (may be stale)
   - Semantic Layer queries use production environment by default
   - Real-time updates require job re-runs

### Tool-Specific Edge Cases

#### Discovery API
- **Limitation**: Requires successful job run to have artifact data
- **Edge Case**: Newly created models won't appear until first run
- **Workaround**: Run `dbt parse` or `compile` locally to generate artifacts

#### Semantic Layer
- **Limitation**: Only available with dbt Cloud Team/Enterprise plans
- **Edge Case**: Metrics not in Semantic Layer won't appear in `list_metrics`
- **Workaround**: Use Discovery API + custom SQL for non-SL metrics

#### SQL Execution
- **Limitation**: Requires PAT, not service token
- **Edge Case**: Query timeouts on long-running queries
- **Security Risk**: Can modify data (INSERT/UPDATE/DELETE)
- **Workaround**: Use read-only database roles, implement query review

#### dbt CLI (Local MCP)
- **Limitation**: Requires local dbt project setup
- **Edge Case**: Environment differences (local vs dbt Cloud)
- **Workaround**: Use dbt Cloud development environments

#### Administrative API
- **Limitation**: Job runs are asynchronous (trigger != completion)
- **Edge Case**: Run status must be polled with `get_job_run_details`
- **Workaround**: Implement polling loop with timeout

#### Code Generation
- **Limitation**: Requires dbt-codegen package installed
- **Edge Case**: Generated YAML may need manual cleanup
- **Workaround**: Treat as starting point, not final output

#### Fusion Lineage
- **Limitation**: ONLY works with Fusion engine (not dbt Core)
- **Edge Case**: Complex macros may not show full lineage
- **Workaround**: Fall back to `get_model_parents/children` for DAG-level lineage

---

## Comparison with Alternative Approaches

### vs. Direct dbt Cloud API
**dbt-mcp Advantages**:
- Standardized MCP protocol (works with any MCP client)
- Simplified authentication (env vars vs API key management)
- AI-optimized tool descriptions
- Built-in error handling

**dbt Cloud API Advantages**:
- More granular control
- Full REST API flexibility
- Language-agnostic (any HTTP client)

**Use MCP When**: Building AI agents, using MCP-compatible tools (Claude, Cursor)
**Use Direct API When**: Custom integrations, non-AI automation, specific API features not in MCP

---

### vs. dbt Cloud CLI
**dbt-mcp Advantages**:
- Accessible from AI agents
- No local CLI installation needed (remote MCP)
- Programmatic access to metadata
- Semantic Layer integration

**dbt Cloud CLI Advantages**:
- Interactive terminal experience
- Full dbt CLI feature parity
- Local-first development
- Offline capabilities

**Use MCP When**: AI-driven workflows, programmatic access, web applications
**Use CLI When**: Manual development, debugging, local iteration

---

### vs. dbt Docs
**dbt-mcp Advantages**:
- Programmatic metadata access
- Real-time queries via Semantic Layer
- Automated workflow integration
- AI agent consumption

**dbt Docs Advantages**:
- Visual exploration
- Human-friendly presentation
- Static hosting (no API calls)
- Comprehensive project overview

**Use MCP When**: Building on metadata, automated analysis, AI exploration
**Use Docs When**: Manual exploration, stakeholder communication, onboarding

---

## Best Practices

### Development Workflow
1. **Start with Discovery**: Use `get_all_models` to understand project structure
2. **Validate Before Execute**: Use `compile` before `run` for new models
3. **Test Incrementally**: Use selectors to test subsets (`test --select tag:critical`)
4. **Generate Then Refine**: Use codegen tools as starting points, not final outputs

### Production Operations
1. **Monitor Continuously**: Set up `list_jobs_runs` polling for failures
2. **Collect Artifacts**: Archive manifests and catalogs for historical analysis
3. **Parameterize Triggers**: Use `trigger_job_run` parameters for flexible deployments
4. **Implement Retries**: Handle transient failures with `retry_job_run`

### Security & Governance
1. **Disable SQL by Default**: Only enable when necessary (`DISABLE_SQL=true`)
2. **Use Service Tokens for Automation**: Reserve PATs for human users
3. **Implement Read-Only Roles**: Limit SQL execution to read-only operations
4. **Audit Token Usage**: Monitor dbt Cloud for unexpected API activity

### Performance Optimization
1. **Cache Discovery Results**: Discovery API responses can be cached (5-10min TTL)
2. **Use Selectors Efficiently**: Target specific models instead of full project operations
3. **Batch Artifact Requests**: Download multiple artifacts in parallel
4. **Implement Pagination**: Use `limit` parameters for large result sets

---

## Future Roadmap (Planned Features)

Based on dbt Labs blog posts and documentation:

1. **OAuth Authentication** (Planned)
   - Eliminates need for static tokens
   - Improved security posture
   - Better multi-tenant support

2. **Expanded Remote MCP Features** (In Progress)
   - More Fusion tools in remote server
   - Enhanced CLI command support
   - Improved multi-cell routing

3. **Enhanced Lineage Capabilities**
   - Cross-project lineage
   - BI tool integration (Tableau, Power BI)
   - Exposure tracking

4. **Streaming/Real-Time Features**
   - Job run event subscriptions
   - Real-time metric updates
   - Live log streaming

---

## Troubleshooting Guide

### Common Issues

#### "Tool not found" Error
**Cause**: Tool category disabled via environment variable
**Solution**: Check `.env` for `DISABLE_*` variables, set to `false` to enable

#### "Authentication failed" Error
**Cause**: Invalid or expired token
**Solution**:
1. Verify `DBT_TOKEN` in `.env`
2. Check token permissions in dbt Cloud
3. Ensure PAT (not service token) for SQL tools

#### "Semantic Layer unavailable" Error
**Cause**: Plan doesn't include Semantic Layer access
**Solution**: Upgrade to dbt Cloud Team or Enterprise plan

#### "Artifact not found" Error
**Cause**: No successful job run to generate artifacts
**Solution**: Run `dbt compile` or trigger a job run to generate artifacts

#### "SQL execution timeout" Error
**Cause**: Query exceeds timeout limit
**Solution**:
1. Optimize query (add filters, reduce data scanned)
2. Increase timeout parameter
3. Break into smaller queries

---

## Additional Resources

### Official Documentation
- **dbt MCP Overview**: https://docs.getdbt.com/docs/dbt-ai/about-mcp
- **Local Setup Guide**: https://docs.getdbt.com/docs/dbt-ai/setup-local-mcp
- **GitHub Repository**: https://github.com/dbt-labs/dbt-mcp
- **Blog Post**: https://docs.getdbt.com/blog/introducing-dbt-mcp-server

### Community Resources
- **Slack Channel**: #tools-dbt-mcp in dbt Community Slack
- **GitHub Issues**: Report bugs and feature requests
- **MCP Protocol**: https://modelcontextprotocol.io/

### Related Tools
- **dbt-codegen**: https://github.com/dbt-labs/dbt-codegen (required for codegen tools)
- **dbt Fusion**: https://docs.getdbt.com/docs/fusion/about-fusion (required for column lineage)

---

## Appendix: Environment Variable Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DBT_HOST` | ✅ (Cloud) | - | dbt Cloud hostname (e.g., cloud.getdbt.com) |
| `DBT_TOKEN` | ✅ | - | Personal Access Token or Service Token |
| `DBT_PROJECT_DIR` | ✅ (Local) | - | Path to local dbt project |
| `DBT_PATH` | ✅ (Local) | - | Path to dbt executable |
| `DBT_PROD_ENV_ID` | ⚠️ (Platform) | - | Production environment ID |
| `DBT_DEV_ENV_ID` | ⚠️ (Platform) | - | Development environment ID |
| `DBT_USER_ID` | ⚠️ (Platform) | - | User ID for dbt Cloud |
| `DBT_ACCOUNT_ID` | ⚠️ (Platform) | - | Account ID for dbt Cloud |
| `MULTICELL_ACCOUNT_PREFIX` | ❌ | - | Multi-cell instance prefix |
| `DISABLE_DBT_CLI` | ❌ | `false` | Disable dbt CLI commands |
| `DISABLE_SEMANTIC_LAYER` | ❌ | `false` | Disable Semantic Layer tools |
| `DISABLE_DISCOVERY` | ❌ | `false` | Disable Discovery API tools |
| `DISABLE_ADMIN_API` | ❌ | `false` | Disable Administrative API tools |
| `DISABLE_SQL` | ❌ | `true` | Disable SQL execution tools |
| `DISABLE_DBT_CODEGEN` | ❌ | `true` | Disable code generation tools |

**Legend**:
- ✅ Required
- ⚠️ Conditionally required
- ❌ Optional

---

## Appendix: Quick Reference - Tools by Use Case

### "I want to explore my dbt project"
- `get_all_models` - See all models
- `get_mart_models` - See presentation layer
- `get_model_details` - Deep dive on specific model
- `list_metrics` - Discover available metrics

### "I want to understand dependencies"
- `get_model_parents` - What feeds this model?
- `get_model_children` - What depends on this model?
- `get_column_lineage` - Column-level lineage (Fusion only)

### "I want to query data"
- `query_metrics` - Query governed metrics
- `text_to_sql` - Generate SQL from natural language
- `execute_sql` - Run custom SQL
- `compile_sql` - Validate SQL without running

### "I want to run dbt operations"
- `build` - Full project build
- `run` - Run specific models
- `test` - Run tests
- `compile` - Validate SQL

### "I want to manage jobs"
- `trigger_job_run` - Start a job
- `list_jobs_runs` - Monitor jobs
- `get_job_run_details` - Investigate run
- `cancel_job_run` - Stop runaway job

### "I want to generate boilerplate"
- `generate_source` - Create source YAML
- `generate_model_yaml` - Create model docs
- `generate_staging_model` - Create staging model SQL

---

## Conclusion

The dbt-mcp server provides a comprehensive, AI-native interface to dbt's data transformation platform. By organizing tools into seven logical categories and supporting both local and remote deployment modes, it enables a wide range of use cases from individual development to enterprise-scale automation.

**Key Takeaways**:
1. **Discovery First**: Start with Discovery API to understand project structure
2. **Security Conscious**: SQL tools disabled by default for good reason
3. **Authentication Matters**: PAT for SQL, Service Token for automation
4. **Local vs Remote**: Choose based on use case (development vs production)
5. **Tool Categories**: Seven categories covering full dbt lifecycle
6. **Production Ready**: Administrative API enables robust orchestration
7. **Future-Proof**: Active development with OAuth and enhanced features coming

**Recommendation for dbt-expert Agent**:
- Lead with Discovery API tools for exploration
- Use Semantic Layer for governed metric queries
- Delegate SQL execution only when necessary (with warnings)
- Leverage Administrative API for job orchestration
- Guide users on authentication requirements
- Clarify local vs remote capabilities
- Reference this document for detailed parameters and examples
