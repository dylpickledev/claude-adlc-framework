- hey. dont read my .env in full. only env var names

## dbt Issue Analysis Patterns

### Common dbt Issue Categories
1. **Schema/Column Reference Errors**: Tests referencing incorrect column names vs actual model schemas
2. **Data Quality Issues**: Uniqueness constraint violations, null constraint failures, massive duplications
3. **Cross-System Validation Failures**: Mismatches between source systems and dbt model expectations
4. **Business Logic Validation**: Failed reconciliation tests, metric validation errors

### Architecture-Aware Analysis Approach
- **Data Flow Context**: Issues often span multiple layers (Orchestra → dbt → Snowflake → Semantic Layer)
- **Model Layer Impact**: Problems cascade from staging (stg_) through marts (dm_) to reports (rpt_)
- **Source System Dependencies**: ERP, Customer, Operations, Safety systems create different data patterns

### Effective Prioritization Framework
1. **CRITICAL**: Schema compilation errors that block other work
2. **HIGH**: Large-scale data quality issues indicating upstream pipeline problems
3. **MEDIUM**: Business logic and validation failures
4. **LOW**: Warning-level issues that don't break functionality

### Investigation Strategy
- Use dbt-mcp to examine actual model schemas vs test expectations
- Check upstream Orchestra pipeline health for massive duplication issues
- Validate source system data quality for cross-system reconciliation failures
- Focus on fixing blocking issues before addressing data quality problems

## Git Workflow for dbt_cloud Repository

### Branch Structure
- **master**: Production branch
- **dbt_dw**: Staging branch

### Branching Workflow
1. Always sync local dbt_dw with remote: `git checkout dbt_dw && git pull origin dbt_dw`
2. Create new feature branches from dbt_dw: `git checkout -b feature-branch-name`
3. Never branch directly from master
4. Ensure dbt_dw is up-to-date before creating any new branches
- git branches should be prefixed by feature/ or fix/