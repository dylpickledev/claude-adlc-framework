don't look at the full .env file. Only search for the var names up to the equals sign.

## Repository Branch Structures

### dbt_cloud
- **master**: Production branch
- **dbt_dw**: Staging branch
- **Workflow**: Branch from dbt_dw, sync before creating features

### dbt_errors_to_issues
- **main**: Production branch (no staging branch)
- **Workflow**: Branch directly from main

### roy_kent
- **master**: Production branch (no staging branch)  
- **Workflow**: Branch directly from master

### sherlock
- **main**: Production branch (no staging branch)
- **Workflow**: Branch directly from main

## General Git Workflow

### Branch Naming Convention
- Feature branches: `feature/description`
- Fix branches: `fix/description`

### Standard Workflow Steps
1. Sync with production/staging branch before creating features
2. Create descriptive branch names
3. Keep branches focused and atomic
4. Test locally before pushing

## Cross-System Issue Analysis & Coordination

### Common Issue Categories (Multi-Tool)
1. **Schema/Column Reference Errors**: Tests referencing incorrect column names vs actual model schemas
2. **Data Quality Issues**: Uniqueness constraint violations, null constraint failures, massive duplications
3. **Cross-System Validation Failures**: Mismatches between source systems and dbt model expectations
4. **Business Logic Validation**: Failed reconciliation tests, metric validation errors

### Architecture-Aware Analysis Approach
- **Data Flow Context**: Issues often span multiple layers (Orchestra → dbt → Snowflake → Semantic Layer)
- **Model Layer Impact**: Problems cascade from staging (stg_) through marts (dm_) to reports (rpt_)
- **Source System Dependencies**: ERP, Customer, Operations, Safety systems create different data patterns

### Cross-Tool Prioritization Framework
1. **CRITICAL**: Schema compilation errors that block other work (dbt-expert)
2. **HIGH**: Large-scale data quality issues indicating upstream pipeline problems (orchestra-expert + dlthub-expert)
3. **MEDIUM**: Business logic and validation failures (dbt-expert + business-context)
4. **LOW**: Warning-level issues that don't break functionality

### Agent Coordination Strategy
- **dbt-expert**: Examine model schemas vs test expectations, focus on blocking compilation issues first
- **orchestra-expert**: Check pipeline health for massive duplication issues, upstream data quality
- **snowflake-expert**: Validate warehouse-level performance and data quality issues  
- **dlthub-expert**: Source system data quality for cross-system reconciliation failures
- **tableau-expert**: Dashboard performance issues stemming from data problems
- **business-context**: Business logic validation and stakeholder requirement clarification
- **da-architect**: System design, data flow analysis, and strategic platform decisions across the entire data stack

- git branches should be prefixed by feature/ or fix/
- use subagents for tasks to help optimize your context window. Determine if it'd be best to use defined agent, or if its general then give to a general subagent

## Test-Driven Data Development (TDD)

### Data Testing Workflow
Follow Claude Code's TDD best practice adapted for data work:

1. **Write Tests First**: Create dbt tests before implementing models
   ```sql
   -- tests/assert_customer_ids_unique.sql
   select customer_id, count(*)
   from {{ ref('stg_customers') }}
   group by customer_id
   having count(*) > 1
   ```

2. **Confirm Test Failures**: Run tests to verify they initially fail
   ```bash
   dbt test --select stg_customers --store-failures
   ```

3. **Implement Model Logic**: Write SQL to pass tests
   ```sql
   -- models/staging/stg_customers.sql
   select distinct customer_id, customer_name
   from {{ source('erp', 'customers') }}
   ```

4. **Verify No Overfitting**: Test against production data samples
   ```bash
   dbt test --select stg_customers --vars '{"test_data_sample": 1000}'
   ```

### Data Quality Testing Strategy
- **Schema Tests**: Column existence, data types, constraints
- **Business Logic Tests**: Reconciliation, metric validation, referential integrity
- **Performance Tests**: Query execution time, result set sizes
- **Cross-System Tests**: Source system vs. warehouse validation

### TDD Commands for Data Work
```bash
# Test-first development cycle
dbt test --select <model_name> --store-failures  # Confirm failures
dbt run --select <model_name>                    # Implement solution
dbt test --select <model_name>                   # Verify success
```