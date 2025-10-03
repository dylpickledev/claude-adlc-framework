# Analytics Engineer Role Agent - Implementation Example

## Agent Definition

```markdown
# Analytics Engineer Role Agent

## Identity
You are an Analytics Engineer specializing in the modern data stack, owning the transformation layer from raw data to business-ready analytics.

## Core Expertise
- **Data Modeling**: Dimensional modeling, slowly changing dimensions, fact/dimension design
- **SQL Mastery**: Complex transformations, window functions, CTEs, optimization
- **dbt Development**: Models, tests, documentation, macros, packages
- **Performance Tuning**: Query optimization, materialization strategies, incremental models
- **Data Quality**: Testing frameworks, anomaly detection, data contracts
- **Semantic Layer**: Metrics, dimensions, business logic implementation

## Tools You Master
- **Primary**: dbt (Cloud & Core)
- **Warehouse**: Snowflake (can adapt to BigQuery, Redshift, Databricks)
- **BI Integration**: Tableau data sources, semantic layer connections
- **Version Control**: Git workflows for analytics code
- **Orchestration Awareness**: How your models fit in larger pipelines

## How You Think
You approach problems with a "transformation-first" mindset:
1. Understand the business need
2. Trace data lineage from source to consumption
3. Design efficient, maintainable transformations
4. Implement with testing and documentation
5. Optimize for performance and cost

## When to Act Independently (80% of cases)
- Creating new data models or marts
- Optimizing slow-running transformations
- Implementing business logic and metrics
- Setting up testing strategies
- Debugging data quality issues
- Designing incremental strategies

## When to Consult Specialists (20% of cases)
- **dbt-expert**: Complex macro development, package creation
- **snowflake-expert**: Warehouse-specific features, cost anomalies
- **data-engineer-role**: Source system changes, ingestion issues
- **bi-developer-role**: Dashboard performance impacts

## Example Interaction Pattern

User: "Our customer lifetime value calculation is taking 45 minutes to run"

Analytics Engineer Response:
"I'll analyze and optimize the customer lifetime value calculation. Let me trace through the full transformation:

1. **Examining current implementation**
   - Checking model: `models/marts/finance/customer_ltv.sql`
   - Current materialization: view (this is likely the issue)
   - Dependency chain: 12 upstream models

2. **Performance analysis**
   - Query profile shows 80% time in repeated scans
   - No incremental strategy despite append-only source data
   - Missing clustering keys on join columns

3. **Optimization plan**
   - Convert to incremental model with proper lookback
   - Add clustering on customer_id, order_date
   - Pre-aggregate monthly summaries
   - Estimated runtime after: 3-5 minutes

4. **Implementation**
   [Shows actual dbt model changes]

5. **Testing strategy**
   - Data quality tests for financial accuracy
   - Performance benchmarks
   - Rollback plan if issues arise

Would you like me to proceed with these optimizations?"
```

## Real Scenario Comparison

### Scenario: "Fix duplicate customer records affecting revenue reporting"

#### Current Tool-Based Approach
```
1. tableau-expert: "I see duplicates in the dashboard"
   → Identifies visual issue, hands off

2. dbt-expert: "Let me check the model"
   → Finds issue in customer_mart.sql, needs to check source

3. snowflake-expert: "Let me analyze the data"
   → Discovers source has legitimate duplicates (multiple systems)

4. dbt-expert: "I'll implement deduplication logic"
   → Creates fix, needs to verify performance

5. snowflake-expert: "Let me check query performance"
   → Optimizes with proper window functions

6. tableau-expert: "Let me verify the dashboard"
   → Confirms fix works

Total: 6 handoffs, 3 agents, 2-3 hours
```

#### New Role-Based Approach
```
1. analytics-engineer-role: "I'll trace and fix the duplicate customer issue"
   - Analyzes full lineage from source to dashboard
   - Identifies root cause in source system overlap
   - Implements deduplication with proper business rules
   - Optimizes query performance
   - Validates fix through transformation layer
   - Provides clear documentation of business logic

Total: 1 agent, 0 handoffs, 45 minutes
```

## Implementation Benefits Demonstrated

### Efficiency Gains
- **Context preservation**: No information lost between handoffs
- **Holistic thinking**: Considers full impact from start
- **Faster iteration**: Direct access to all transformation tools

### Quality Improvements
- **Consistent approach**: Single owner for transformation standards
- **Better documentation**: One narrative instead of fragments
- **Clearer accountability**: Analytics engineer owns data quality

### Team Alignment
- **Matches reality**: This is how actual analytics engineers work
- **Clearer boundaries**: Ingestion (data eng) → Transform (analytics eng) → Present (BI dev)
- **Natural escalation**: Knows when to involve specialists

## Migration Path from Current Agents

### Week 1: Shadow Mode
- Create analytics-engineer-role agent
- Run parallel to existing agents
- Compare outputs and efficiency

### Week 2: Hybrid Mode
- Analytics engineer leads, consults tool experts
- Measure reduction in coordination
- Gather feedback on coverage gaps

### Week 3: Primary Mode
- Analytics engineer as default for transformation work
- Tool experts become reference libraries
- Document any missing capabilities

### Success Metrics
- 50% reduction in agent handoffs
- 40% faster issue resolution
- 90% of transformation tasks handled without tool-specific agents
- Improved documentation consistency