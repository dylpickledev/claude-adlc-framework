# Snowflake-MCP Quick Reference Card

**Purpose**: Fast lookup for common snowflake-mcp operations
**Primary Users**: snowflake-expert, analytics-engineer-role, qa-engineer-role, dba-role
**Server**: snowflake-mcp (uvx package: snowflake-labs-mcp)

---

## 🚀 Most Common Operations

### 1. Object Discovery & Metadata

**List databases**:
```bash
mcp__snowflake-mcp__list_objects object_type="database"
```

**List schemas in database**:
```bash
mcp__snowflake-mcp__list_objects object_type="schema" database_name="ANALYTICS_DW"
```

**List tables in schema**:
```bash
mcp__snowflake-mcp__list_objects \
  object_type="table" \
  database_name="ANALYTICS_DW" \
  schema_name="PROD_SALES_DM"
```

**Search tables by name**:
```bash
mcp__snowflake-mcp__list_objects \
  object_type="table" \
  database_name="ANALYTICS_DW" \
  schema_name="PROD_SALES_DM" \
  like="%FACT%"
```

**List views**:
```bash
mcp__snowflake-mcp__list_objects \
  object_type="view" \
  database_name="ANALYTICS_DW" \
  schema_name="PROD_SALES_DM"
```

**List warehouses**:
```bash
mcp__snowflake-mcp__list_objects object_type="warehouse"
```

**List compute pools**:
```bash
mcp__snowflake-mcp__list_objects object_type="compute_pool"
```

---

### 2. Object Details & Schema

**Describe table** (columns, data types):
```bash
mcp__snowflake-mcp__describe_object \
  object_type="table" \
  target_object={"database_name": "ANALYTICS_DW", "schema_name": "PROD_SALES_DM", "name": "FCT_ORDERS"}
```

**Describe view**:
```bash
mcp__snowflake-mcp__describe_object \
  object_type="view" \
  target_object={"database_name": "ANALYTICS_DW", "schema_name": "PROD_SALES_DM", "name": "VW_REVENUE_SUMMARY"}
```

**Describe warehouse**:
```bash
mcp__snowflake-mcp__describe_object \
  object_type="warehouse" \
  target_object={"name": "TABLEAU_WH"}
```

---

### 3. Query Execution & Data Validation

**Execute simple query**:
```bash
mcp__snowflake-mcp__run_snowflake_query \
  statement="SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()"
```

**Data validation query**:
```bash
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  COUNT(*) as total_rows,
  COUNT(DISTINCT customer_id) as unique_customers,
  MAX(order_date) as latest_order
FROM ANALYTICS_DW.PROD_SALES_DM.FCT_ORDERS
WHERE order_date >= CURRENT_DATE - 7
"
```

**Cost analysis query** (warehouse usage):
```bash
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  warehouse_name,
  SUM(credits_used) as total_credits,
  SUM(credits_used) * 4.00 as estimated_cost_usd
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY total_credits DESC
LIMIT 10
"
```

**Query history** (performance analysis):
```bash
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  query_id,
  query_text,
  execution_time / 1000 as execution_seconds,
  warehouse_name,
  user_name
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
  AND execution_time > 60000
ORDER BY execution_time DESC
LIMIT 10
"
```

---

### 4. Semantic Views (Governed Metrics)

**List semantic views**:
```bash
mcp__snowflake-mcp__list_semantic_views \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC"
```

**Describe semantic view**:
```bash
mcp__snowflake-mcp__describe_semantic_view \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC" \
  view_name="SALES_METRICS"
```

**Show semantic dimensions**:
```bash
mcp__snowflake-mcp__show_semantic_dimensions \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC" \
  view_name="SALES_METRICS"
```

**Show semantic metrics**:
```bash
mcp__snowflake-mcp__show_semantic_metrics \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC" \
  view_name="SALES_METRICS"
```

**Query semantic view**:
```bash
mcp__snowflake-mcp__query_semantic_view \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC" \
  view_name="SALES_METRICS" \
  dimensions=[{"table": "time", "name": "order_month"}] \
  metrics=[{"table": "revenue", "name": "total_revenue"}] \
  limit=12
```

---

## 🎯 Common Workflows

### Workflow 1: Table Discovery & Schema Analysis
```bash
# 1. List all tables in schema
mcp__snowflake-mcp__list_objects \
  object_type="table" \
  database_name="ANALYTICS_DW" \
  schema_name="PROD_SALES_DM"

# 2. Search for specific table pattern
mcp__snowflake-mcp__list_objects \
  object_type="table" \
  database_name="ANALYTICS_DW" \
  schema_name="PROD_SALES_DM" \
  like="%CUSTOMER%"

# 3. Describe table schema
mcp__snowflake-mcp__describe_object \
  object_type="table" \
  target_object={"database_name": "ANALYTICS_DW", "schema_name": "PROD_SALES_DM", "name": "DIM_CUSTOMERS"}

# 4. Validate data freshness
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  MAX(updated_at) as last_update,
  DATEDIFF(hour, MAX(updated_at), CURRENT_TIMESTAMP()) as hours_since_update,
  COUNT(*) as total_rows
FROM ANALYTICS_DW.PROD_SALES_DM.DIM_CUSTOMERS
"
```

### Workflow 2: Cost Analysis & Optimization
```bash
# 1. List all warehouses
mcp__snowflake-mcp__list_objects object_type="warehouse"

# 2. Get warehouse credit usage (last 7 days)
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  warehouse_name,
  SUM(credits_used) as total_credits,
  SUM(credits_used) * 4.00 as estimated_cost_usd,
  COUNT(*) as execution_count,
  AVG(credits_used) as avg_credits_per_query
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY total_credits DESC
"

# 3. Identify expensive queries
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  query_id,
  LEFT(query_text, 100) as query_preview,
  execution_time / 1000 as execution_seconds,
  warehouse_name,
  credits_used_cloud_services
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND execution_time > 60000
ORDER BY execution_time DESC
LIMIT 10
"

# 4. Describe warehouse configuration
mcp__snowflake-mcp__describe_object \
  object_type="warehouse" \
  target_object={"name": "TABLEAU_WH"}
```

### Workflow 3: Data Quality Validation
```bash
# 1. Check row counts and freshness
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  'FCT_ORDERS' as table_name,
  COUNT(*) as total_rows,
  MAX(order_date) as latest_date,
  DATEDIFF(day, MAX(order_date), CURRENT_DATE) as days_behind
FROM ANALYTICS_DW.PROD_SALES_DM.FCT_ORDERS
"

# 2. Check for duplicates
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  order_id,
  COUNT(*) as duplicate_count
FROM ANALYTICS_DW.PROD_SALES_DM.FCT_ORDERS
GROUP BY order_id
HAVING COUNT(*) > 1
LIMIT 10
"

# 3. Validate referential integrity
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  COUNT(*) as orphaned_records
FROM ANALYTICS_DW.PROD_SALES_DM.FCT_ORDERS o
LEFT JOIN ANALYTICS_DW.PROD_SALES_DM.DIM_CUSTOMERS c
  ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL
"

# 4. Check for NULLs in critical columns
mcp__snowflake-mcp__run_snowflake_query \
  statement="
SELECT
  COUNT(*) as total_rows,
  SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) as null_order_ids,
  SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) as null_customer_ids,
  SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) as null_order_dates
FROM ANALYTICS_DW.PROD_SALES_DM.FCT_ORDERS
"
```

### Workflow 4: Semantic Layer Exploration
```bash
# 1. List semantic views
mcp__snowflake-mcp__list_semantic_views \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC"

# 2. Describe specific semantic view
mcp__snowflake-mcp__describe_semantic_view \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC" \
  view_name="SALES_METRICS"

# 3. Show available dimensions
mcp__snowflake-mcp__show_semantic_dimensions \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC" \
  view_name="SALES_METRICS"

# 4. Show available metrics
mcp__snowflake-mcp__show_semantic_metrics \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC" \
  view_name="SALES_METRICS"

# 5. Query metrics with dimensions
mcp__snowflake-mcp__query_semantic_view \
  database_name="ANALYTICS_DW" \
  schema_name="SEMANTIC" \
  view_name="SALES_METRICS" \
  dimensions=[{"table": "time", "name": "order_month"}] \
  metrics=[{"table": "revenue", "name": "total_revenue"}] \
  order_by="order_month DESC" \
  limit=12
```

---

## ⚠️ Important Notes

### Security & Permissions

**Read-Only by Default**:
- ✅ SELECT queries
- ✅ DESCRIBE operations
- ✅ USE commands (database, schema, warehouse)
- ❌ INSERT, UPDATE, DELETE (disabled)
- ❌ CREATE, ALTER, DROP (disabled)
- ❌ TRUNCATE, MERGE (disabled)

**Permission Control**:
- Configured via SQL statement permissions in `.mcp.json`
- Granular control over allowed operations
- Default: Read-only for safety

**Write Operations** (Disabled by Default):
- `create_object` - Create databases, schemas, tables, views, warehouses
- `drop_object` - Drop Snowflake objects
- `create_or_alter_object` - Modify existing objects

**Why disabled**: Write operations can MODIFY production data/infrastructure

### Authentication Methods

**OAuth** (Recommended):
- Snowflake OAuth flow
- Most secure, enterprise-grade
- Token refresh handled automatically

**Password** (Current):
- Username + password authentication
- Password injected at runtime (not in config)
- Wrapper script: `scripts/launch-snowflake-mcp.sh`

**Key Pair** (Alternative):
- Private key authentication
- Enterprise security standard
- Requires key setup

### Performance Considerations

**Query Limits**:
- No built-in result set limits
- Add `LIMIT` clause to queries manually
- Large result sets can cause timeout

**Account Usage Views**:
- `SNOWFLAKE.ACCOUNT_USAGE.*` views have latency (45 min - 3 hours)
- Use `INFORMATION_SCHEMA` for real-time metadata
- Account Usage for historical analysis only

**Warehouse Selection**:
- Queries run on current warehouse (set via `USE WAREHOUSE`)
- Small queries can use small warehouse (lower cost)
- Large queries require appropriately sized warehouse

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: "Object does not exist or not authorized"
- **Cause**: Incorrect database/schema/table name OR missing permissions
- **Fix**: Verify object names with `list_objects`, check role permissions

**Issue**: "SQL compilation error"
- **Cause**: Syntax error in SQL statement
- **Fix**: Test query in Snowflake UI first, check column/table names

**Issue**: "Query timeout"
- **Cause**: Large query without limits OR small warehouse
- **Fix**: Add LIMIT clause, use larger warehouse for complex queries

**Issue**: "Authentication failed"
- **Cause**: Incorrect password OR expired OAuth token
- **Fix**: Verify credentials in 1Password, check wrapper script

**Issue**: "Write operation denied"
- **Cause**: Attempting DDL/DML when write operations disabled
- **Fix**: Use read-only queries OR enable write operations (with caution)

---

## 📊 Confidence Levels

| Operation | Confidence | Notes |
|-----------|------------|-------|
| List objects | HIGH (0.95) | Core discovery operation |
| Describe objects | HIGH (0.95) | Schema inspection |
| SELECT queries | HIGH (0.90) | Read-only data access |
| Cost analysis | HIGH (0.88) | ACCOUNT_USAGE queries |
| Semantic views | MEDIUM (0.75) | Requires Cortex setup |
| Write operations | LOW (0.40) | Disabled by default, high risk |

---

## 🎓 When to Delegate to snowflake-expert

**Direct use OK** (analytics-engineer-role, qa-engineer-role):
- ✅ List objects (databases, schemas, tables)
- ✅ Describe object schemas
- ✅ Simple SELECT queries (data validation, row counts)
- ✅ Cost queries (warehouse usage, query history)

**Delegate to specialist** (confidence <0.60):
- ❌ Warehouse cost optimization (detailed analysis)
- ❌ Query performance tuning (Snowflake-specific features)
- ❌ Clustering/partitioning strategy
- ❌ Semantic views (complex Cortex integration)
- ❌ Write operations (DDL, data modification)

---

## 📚 Related Resources

- **Full Snowflake-MCP Documentation**: `knowledge/mcp-servers/snowflake-mcp/`
- **snowflake-expert Agent**: `.claude/agents/specialists/snowflake-expert.md`
- **MCP Integration Guide**: `.claude/memory/patterns/agent-mcp-integration-guide.md`
- **Snowflake Docs**: https://docs.snowflake.com/

---

## 🔗 Integration with dbt-mcp

**Complementary Use**:
- **dbt-mcp**: Model metadata, compiled SQL, transformation logic
- **snowflake-mcp**: Raw data queries, cost analysis, warehouse performance

**Common Pattern**:
1. Use dbt-mcp to get model details and compiled SQL
2. Use snowflake-mcp to profile query performance
3. Delegate to snowflake-expert for optimization recommendations

---

*Created: 2025-10-08*
*Last Updated: 2025-10-08*
*Quick Reference for rapid MCP tool lookup*
