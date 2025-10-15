# Pattern: dbt Incremental Model Optimization

**Pattern Type**: Performance Optimization  
**Confidence**: 0.85 (High - proven pattern, needs production validation)  
**Domain**: Analytics Engineering (dbt + Snowflake)  
**Last Updated**: 2025-10-14  
**Source**: dbt-expert analysis (fct_sales_daily)

---

## When to Use This Pattern

**Indicators**:
- ✅ Fact table with 10M+ rows taking >30 minutes to refresh
- ✅ Full table materialization rebuilding ALL historical data daily
- ✅ Only small percentage of rows change daily (< 10%)
- ✅ Strong unique key exists (or can be created)
- ✅ Business tolerates 2-7 day lookback window for late arrivals

**Not Appropriate When**:
- ❌ Dimension tables (use snapshots or table materialization)
- ❌ Aggregated marts depending on full dataset (partition strategy better)
- ❌ No reliable unique key or timestamp column
- ❌ Data requires complete daily restatement

---

## Technical Implementation

### Core Configuration

```sql
{{
    config(
        materialized='incremental',
        unique_key='transaction_id',  -- Must be truly unique
        on_schema_change='fail',  -- Strict schema control for fact tables
        incremental_strategy='merge',  -- Handle late arrivals and updates
        incremental_predicates=["dbt_updated_at >= dateadd(day, -3, current_date)"],
        cluster_by=['transaction_date']  -- Snowflake-specific optimization
    )
}}

select
    transaction_id,
    transaction_date,
    -- ... other columns ...
    current_timestamp() as dbt_updated_at  -- Track processing time
from {{ ref('source_table') }}
left join {{ ref('dim_table') }} using (key_id)

{% if is_incremental() %}
    -- Critical: Filter early to limit upstream scans
    where transaction_date > (
        select dateadd(day, -3, max(transaction_date))
        from {{ this }}
    )
{% endif %}
```

### Key Decisions

**1. Incremental Strategy: `merge` vs `append`**
- **merge**: Handles late-arriving facts and dimension updates (RECOMMENDED for facts)
- **append**: Faster but no updates (use for immutable event logs)

**2. Lookback Window: 2-7 days**
- Balance data completeness vs performance
- 3 days typical for transactional systems
- Tune based on late-arrival patterns from source systems

**3. on_schema_change: `fail`**
- Forces deliberate schema management
- Prevents accidental column additions breaking downstream dashboards
- Alternative: `append_new_columns` for additive-only changes

---

## Performance Expectations

**Typical Improvements**:
- **Runtime**: 70-90% reduction for daily incremental runs
- **Compute**: 75-85% reduction in Snowflake credits (daily)
- **Example**: 45 min full refresh → 6-7 min incremental

**Assumptions**:
- Daily new/updated data is < 10% of total table
- Appropriate Snowflake warehouse sizing
- Table clustered on filter column (transaction_date)

---

## Critical Pre-Implementation Validation

### 1. Unique Key Integrity (MANDATORY)

```bash
dbt test --select model_name --data unique
```

**Must pass 100%** - if fails:
- Investigate root cause (source data issue, transform logic)
- Consider composite key: `unique_key=['col1', 'col2']`
- Fix upstream before implementing incremental

### 2. Snowflake Warehouse Analysis (REQUIRED)

**Delegate to snowflake-expert**:
- Current warehouse size and cost per model run
- Query execution plan analysis (join strategies, partition pruning)
- Clustering recommendation for incremental filter column
- Dual-warehouse strategy: MEDIUM for incremental, LARGE for full-refresh

**Context to Provide**:
```
Model: <model_name>
Current Runtime: <X> minutes
Data Volume: <Y> rows historical, <Z> new daily
Transformations: <N> dimension joins, <M> calculated metrics
Proposed Change: table → incremental materialization
Questions: Warehouse sizing, clustering strategy, join optimization
```

### 3. Test Optimization Strategy

**Update test configurations** for incremental execution:

```yaml
models:
  - name: fct_sales_daily
    data_tests:
      - unique:
          column_name: transaction_id
          config:
            where: "transaction_date >= dateadd(day, -7, current_date)"
      - not_null:
          column_name: transaction_id
          config:
            where: "transaction_date >= dateadd(day, -7, current_date)"
```

**Benefit**: 80% reduction in test execution time for daily runs

---

## Data Drift Prevention (CRITICAL)

**Problem**: Incremental models inevitably drift from source data over time
- Late arrivals beyond lookback window
- Source data corrections to old records
- Dimension updates requiring fact reprocessing

**Solution**: Scheduled Full Refreshes

```yaml
# In dbt Cloud or orchestration tool
schedule:
  daily_incremental:
    cron: "0 5 * * *"  # 5 AM daily
    command: "dbt run --select model_name"
  
  weekly_full_refresh:
    cron: "0 2 * * 0"  # 2 AM Sunday
    command: "dbt run --select model_name --full-refresh"
```

**Frequency Recommendations**:
- **Weekly**: Standard for most fact tables
- **Monthly**: Low-volatility tables with long lookback windows
- **Daily**: High-volatility tables or strict accuracy requirements

---

## Implementation Phases

### Phase 1: Pre-Implementation Validation (1-2 days)

1. Verify unique key integrity: `dbt test --select model --data unique`
2. Request snowflake-expert warehouse analysis
3. Create feature branch: `feature/model-name-incremental-optimization`
4. Backup current configuration and document current runtime

### Phase 2: Code Implementation (1-2 days)

1. Add incremental configuration to model
2. Add `dbt_updated_at` timestamp column
3. Implement `is_incremental()` filter logic
4. Update test configurations with `where` clauses
5. Initial full-refresh: `dbt run --select model --full-refresh`

### Phase 3: Performance Validation (2-3 days)

1. Measure incremental runtime: `time dbt run --select model`
2. Compare row counts with source (reconciliation test)
3. Validate downstream dashboard accuracy
4. Document actual performance improvement vs projections

### Phase 4: Operationalization (1 week)

1. Configure weekly full-refresh in orchestration tool
2. Set up data drift monitoring (reconciliation alerts)
3. Document troubleshooting procedures
4. Train team on incremental model maintenance

**Total Timeline**: 2-3 weeks for single model optimization

---

## Risk Mitigation

### Risk 1: Data Drift
- **Mitigation**: Weekly full-refresh schedule
- **Detection**: Daily reconciliation test comparing fact vs source counts
- **Impact**: Medium (data accuracy for dashboards)

### Risk 2: Late-Arriving Transactions Not Captured
- **Mitigation**: Tunable lookback window (start with 3 days)
- **Detection**: Monitor late-arrival patterns in source systems
- **Impact**: Low-Medium (missing recent data)

### Risk 3: Unique Key Constraint Violations
- **Mitigation**: Pre-implementation validation, ongoing unique tests
- **Detection**: dbt test failures, Snowflake merge errors
- **Impact**: High (incremental run failures)

### Risk 4: Schema Changes Breaking Incremental Logic
- **Mitigation**: `on_schema_change='fail'` forces explicit handling
- **Detection**: dbt compilation error on schema mismatch
- **Impact**: High (requires full-refresh to resolve)

---

## Rollback Plan

**If optimization causes data quality issues**:

```bash
# Step 1: Revert model configuration
git checkout models/path/to/model.sql
git checkout models/path/to/_models.yml

# Step 2: Full refresh with original table materialization  
dbt run --select model_name --full-refresh

# Step 3: Validate data integrity
dbt test --select model_name

# Step 4: Refresh downstream Tableau dashboards
# [Manual validation by BI team]
```

**Rollback Time**: 60-90 minutes (includes rebuild + validation)

---

## Cost Analysis Framework

**IMPORTANT**: Runtime improvements ≠ Direct cost savings until validated

### Measuring Actual Snowflake Costs

**Before Implementation**:
1. Query Snowflake `QUERY_HISTORY` for last 30 days
2. Sum credits consumed by model across all runs
3. Calculate average credits per run and monthly total

**SQL for Cost Baseline**:
```sql
SELECT
    query_text,
    warehouse_name,
    warehouse_size,
    execution_time / 1000 as seconds,
    credits_used_cloud_services,
    COUNT(*) as run_count,
    SUM(credits_used_cloud_services) as total_credits,
    AVG(credits_used_cloud_services) as avg_credits_per_run
FROM snowflake.account_usage.query_history
WHERE query_text ILIKE '%dbt_model_name%'
  AND start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY 1, 2, 3, 4, 5
ORDER BY total_credits DESC;
```

**After 30 Days Post-Implementation**:
1. Run same query for incremental period
2. Calculate delta: (old_avg_credits - new_avg_credits) × runs_per_month
3. Convert to dollars: credits_saved × $3 (adjust for actual Snowflake pricing)

**Extrapolation to Similar Models**:
1. Identify candidate models with similar characteristics
2. Measure EACH model's baseline (don't assume uniformity)
3. Calculate realistic ROI: total_credits_saved × pricing

**DO NOT**:
- ❌ Assume cost savings without measuring baseline
- ❌ Extrapolate from unmeasured estimates ("probably 90 credits/month")
- ❌ Apply blanket percentage reduction across all models

---

## When to Use Snowflake-Expert Delegation

**ALWAYS delegate for**:
- Warehouse sizing recommendations (incremental vs full-refresh)
- Clustering strategy validation
- Query execution plan analysis
- Cost baseline measurement from QUERY_HISTORY
- Join optimization for large dimension tables

**Delegation Pattern**:
```
DELEGATE TO: snowflake-expert
CONFIDENCE: <0.60
REASON: Warehouse cost analysis and performance tuning requires Snowflake-specific expertise
CONTEXT: [Model details, current runtime, data volume, transformation complexity]
```

---

## Production-Validated Use Cases

### fct_sales_daily (Analysis Complete, Not Deployed)
- **Model**: Sales transaction fact table
- **Data Volume**: 50M+ rows historical, 500K-1M daily
- **Current**: 45 min full table refresh
- **Expected**: 6-7 min incremental (85% improvement)
- **Status**: Implementation plan complete, awaiting snowflake-expert analysis
- **Cost Savings**: TBD (requires warehouse cost baseline)
- **Reference**: `.claude/tasks/dbt-expert/fct-sales-daily-optimization-analysis.md`

---

## References

- **dbt Documentation**: https://docs.getdbt.com/docs/build/incremental-models
- **Best Practices**: https://docs.getdbt.com/best-practices/materializations/4-incremental-models
- **Specialist Analysis**: `.claude/tasks/dbt-expert/fct-sales-daily-optimization-analysis.md`

---

## Pattern Maintenance

**Update this pattern when**:
- Production deployment validates (or invalidates) performance projections
- Cost savings measured and documented
- Additional models optimized with lessons learned
- Snowflake best practices evolve (new incremental strategies)

**Next Review**: After fct_sales_daily production deployment and 30-day measurement
