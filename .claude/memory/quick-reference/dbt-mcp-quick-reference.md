# dbt-MCP Quick Reference Card

**Purpose**: Fast lookup for common dbt-mcp operations
**Primary Users**: analytics-engineer-role, dbt-expert, qa-engineer-role, bi-developer-role
**Server**: dbt-mcp (uvx package)

---

## 🚀 Most Common Operations

### 1. Explore Metrics (Semantic Layer)

**List all available metrics**:
```bash
mcp__dbt-mcp__list_metrics
```

**Search metrics by keyword**:
```bash
mcp__dbt-mcp__list_metrics search="revenue"
```

**Get metric dimensions**:
```bash
mcp__dbt-mcp__get_dimensions metrics=["total_revenue"]
```

**Get metric entities**:
```bash
mcp__dbt-mcp__get_entities metrics=["total_revenue"]
```

**Query metrics with dimensions**:
```bash
mcp__dbt-mcp__query_metrics \
  metrics=["total_revenue"] \
  group_by=[{"name": "customer_region", "type": "dimension", "grain": null}] \
  limit=10
```

---

### 2. Model Discovery & Analysis

**List all models**:
```bash
mcp__dbt-mcp__get_all_models
```

**List only mart models** (safer, smaller result):
```bash
mcp__dbt-mcp__get_mart_models
```

**Get model details** (compiled SQL, dependencies):
```bash
mcp__dbt-mcp__get_model_details model_name="fct_orders"
```

**Get model parents** (upstream dependencies):
```bash
mcp__dbt-mcp__get_model_parents model_name="fct_orders"
```

**Get model children** (downstream dependencies):
```bash
mcp__dbt-mcp__get_model_children model_name="fct_orders"
```

**Check model health** (last run, tests, freshness):
```bash
mcp__dbt-mcp__get_model_health model_name="fct_orders"
```

---

### 3. Testing & Validation

**Run dbt tests** (specific model):
```bash
mcp__dbt-mcp__test selector="fct_orders"
```

**Run dbt tests** (all models):
```bash
mcp__dbt-mcp__test
```

**Execute validation query**:
```bash
mcp__dbt-mcp__show sql_query="
SELECT
  COUNT(*) as total_rows,
  MAX(order_date) as latest_order
FROM {{ ref('fct_orders') }}
" limit=5
```

**Note**: Requires dbt CLI setup, not just dbt Cloud API

---

### 4. Job Management (dbt Cloud)

**List all jobs**:
```bash
mcp__dbt-mcp__list_jobs
```

**Get job details**:
```bash
mcp__dbt-mcp__get_job_details job_id=12345
```

**List job runs**:
```bash
mcp__dbt-mcp__list_jobs_runs job_id=12345 status="error" limit=10
```

**Get run details**:
```bash
mcp__dbt-mcp__get_job_run_details run_id=67890
```

**Get run errors** (focused error analysis):
```bash
mcp__dbt-mcp__get_job_run_error run_id=67890
```

**Trigger job run**:
```bash
mcp__dbt-mcp__trigger_job_run job_id=12345 cause="Manual trigger for testing"
```

**Cancel running job**:
```bash
mcp__dbt-mcp__cancel_job_run run_id=67890
```

**Retry failed job**:
```bash
mcp__dbt-mcp__retry_job_run run_id=67890
```

---

## 🎯 Common Workflows

### Workflow 1: Metric Exploration
```bash
# 1. List metrics in semantic layer
mcp__dbt-mcp__list_metrics

# 2. Get dimensions for specific metric
mcp__dbt-mcp__get_dimensions metrics=["revenue"]

# 3. Query metric with dimension breakdown
mcp__dbt-mcp__query_metrics \
  metrics=["revenue"] \
  group_by=[{"name": "metric_time", "type": "time_dimension", "grain": "MONTH"}] \
  order_by=[{"name": "metric_time", "descending": true}] \
  limit=12
```

### Workflow 2: Model Impact Analysis
```bash
# 1. Get model details
mcp__dbt-mcp__get_model_details model_name="dim_customers"

# 2. Check upstream dependencies
mcp__dbt-mcp__get_model_parents model_name="dim_customers"

# 3. Check downstream dependencies (blast radius)
mcp__dbt-mcp__get_model_children model_name="dim_customers"

# 4. Check model health
mcp__dbt-mcp__get_model_health model_name="dim_customers"
```

### Workflow 3: Job Troubleshooting
```bash
# 1. List recent failed runs
mcp__dbt-mcp__list_jobs_runs job_id=12345 status="error" order_by="-created_at" limit=5

# 2. Get focused error analysis
mcp__dbt-mcp__get_job_run_error run_id=67890

# 3. Retry the failed run
mcp__dbt-mcp__retry_job_run run_id=67890
```

### Workflow 4: Data Quality Validation
```bash
# 1. Check model health (tests + freshness)
mcp__dbt-mcp__get_model_health model_name="fct_orders"

# 2. Run dbt tests
mcp__dbt-mcp__test selector="fct_orders"

# 3. Validate data with custom query
mcp__dbt-mcp__show sql_query="
SELECT
  DATE(order_date) as order_day,
  COUNT(*) as order_count,
  SUM(order_total) as daily_revenue
FROM {{ ref('fct_orders') }}
WHERE order_date >= CURRENT_DATE - 7
GROUP BY DATE(order_date)
ORDER BY order_day DESC
" limit=10
```

---

## ⚠️ Important Notes

### Security & Permissions

**SQL Execution Tools** (DISABLED by default):
- `mcp__dbt-mcp__compile` - Requires dbt CLI
- `mcp__dbt-mcp__run` - Requires dbt CLI
- `mcp__dbt-mcp__build` - Requires dbt CLI
- `mcp__dbt-mcp__test` - Requires dbt CLI
- `mcp__dbt-mcp__show` - Requires dbt CLI

**Why disabled**: SQL execution can MODIFY data (incremental models, snapshots)

**How to enable**:
1. Set `DISABLE_SQL=false` in `.mcp.json`
2. Use dbt Cloud PAT (not Service Token)
3. Requires local `~/.dbt/dbt_cloud.yml` configuration

### Authentication Methods

**Service Token** (Read-only API):
- Discovery API ✅
- Semantic Layer ✅
- Administrative API ✅
- CLI Commands ❌ (requires PAT)

**Personal Access Token** (Full access):
- Discovery API ✅
- Semantic Layer ✅
- Administrative API ✅
- CLI Commands ✅ (with local dbt setup)

### Performance Considerations

**Large Result Sets**:
- `get_all_models` can return 1000+ models (use cautiously)
- Prefer `get_mart_models` for smaller, targeted results
- Use `limit` parameter on query operations
- Filter job runs by status/date to reduce results

**Rate Limits**:
- dbt Cloud API: Reasonable limits (not documented publicly)
- Use pagination for large queries
- Batch operations when possible

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: "Auth UserPool not configured"
- **Cause**: Using Service Token when PAT required
- **Fix**: Switch to Personal Access Token for CLI operations

**Issue**: "Model not found"
- **Cause**: Incorrect model name or project
- **Fix**: Use `get_all_models` to list available models, check exact naming

**Issue**: "SQL execution disabled"
- **Cause**: `DISABLE_SQL=true` (default security setting)
- **Fix**: Set `DISABLE_SQL=false` in `.mcp.json` (requires PAT)

**Issue**: "Query timeout"
- **Cause**: Large semantic layer query without limits
- **Fix**: Add `limit` parameter, use more specific dimensions/filters

**Issue**: "Job run not found"
- **Cause**: Run ID doesn't exist or wrong job
- **Fix**: Use `list_jobs_runs` to find valid run IDs

---

## 📊 Confidence Levels

| Operation | Confidence | Notes |
|-----------|------------|-------|
| List metrics | HIGH (0.95) | Core semantic layer operation |
| Get model details | HIGH (0.95) | Core discovery operation |
| Query metrics | HIGH (0.92) | Production-validated patterns |
| Model health | HIGH (0.90) | Comprehensive health checks |
| Job management | HIGH (0.88) | Standard admin operations |
| CLI commands | MEDIUM (0.70) | Requires local dbt setup |
| SQL execution | MEDIUM (0.65-0.70) | Security-restricted, validation needed |

---

## 🎓 When to Delegate to dbt-expert

**Direct use OK** (analytics-engineer-role):
- ✅ List metrics, get model details
- ✅ Simple metric queries
- ✅ Model discovery and exploration
- ✅ Job status checks

**Delegate to specialist** (confidence <0.60):
- ❌ Complex semantic layer queries
- ❌ Performance optimization
- ❌ Model health analysis (with dependencies)
- ❌ Job troubleshooting (error analysis)
- ❌ Advanced testing frameworks

---

## 📚 Related Resources

- **Full dbt-mcp Documentation**: `knowledge/mcp-servers/dbt-mcp/`
- **dbt-expert Agent**: `.claude/agents/specialists/dbt-expert.md`
- **MCP Integration Guide**: `.claude/memory/patterns/agent-mcp-integration-guide.md`
- **dbt Cloud Docs**: https://docs.getdbt.com/docs/cloud/about-cloud/access-regions-ip-addresses

---

*Created: 2025-10-08*
*Last Updated: 2025-10-08*
*Quick Reference for rapid MCP tool lookup*
