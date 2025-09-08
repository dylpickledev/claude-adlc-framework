---
name: test-framework
description: Comprehensive testing framework for data analytics projects using TDD principles
---

I'll guide you through implementing a comprehensive testing framework that follows Claude Code TDD best practices for data analytics.

## 🧪 **Test-Driven Data Analytics Framework**

### Testing Pyramid for Data Projects
```
    ┌─────────────────┐
    │   End-to-End    │  ← Dashboard/Report Tests
    │     Tests       │
    ├─────────────────┤
    │  Integration    │  ← Cross-System Tests
    │     Tests       │
    ├─────────────────┤
    │   Unit Tests    │  ← Model/Function Tests
    │                 │
    └─────────────────┘
```

## 🎯 **Testing Categories**

### 1. dbt Model Tests (Unit Level)
```yaml
# models/staging/_models.yml - Modern dbt testing syntax
models:
  - name: stg_customers
    description: "Cleaned customer data from ERP system"
    data_tests:
      - unique:
          column_name: customer_id
      - not_null:
          column_name: customer_id
    columns:
      - name: customer_id
        description: "Primary key for customers"
        data_tests:
          - unique
          - not_null
      - name: email
        description: "Customer email address"  
        data_tests:
          - unique
          - not_null
      - name: status
        description: "Customer status"
        data_tests:
          - accepted_values:
              values: ['active', 'inactive', 'prospect']
          - relationships:
              to: ref('dim_customer_status')
              field: status_code
```

### 2. Data Quality Tests (Integration Level)
```sql
-- tests/data_quality/assert_revenue_reconciliation.sql
{{ config(severity='error') }}

with source_total as (
  select sum(amount) as source_revenue
  from {{ source('erp', 'transactions') }}
  where date >= current_date - 30
),
warehouse_total as (
  select sum(revenue) as warehouse_revenue  
  from {{ ref('fct_sales') }}
  where date >= current_date - 30
)
select *
from source_total
cross join warehouse_total
where abs(source_revenue - warehouse_revenue) > 100
```

### 3. Business Logic Tests (Integration Level)
```sql
-- tests/business_logic/assert_customer_lifetime_value.sql
with customer_clv as (
  select 
    customer_id,
    sum(order_value) as total_spent,
    count(distinct order_id) as order_count
  from {{ ref('fct_orders') }}
  group by customer_id
)
select customer_id
from customer_clv
where total_spent < 0  -- Should never happen
   or order_count = 0  -- Customers must have orders
```

### 4. Performance Tests (System Level)
```sql
-- tests/performance/assert_query_performance.sql
{{ config(
    severity='warn',
    meta={'performance_threshold_seconds': 30}
) }}

-- This test ensures key queries complete within thresholds
select 1 as test_result
where (
  select count(*)
  from {{ ref('dm_customer_analytics') }}
  where updated_at >= current_date
) > 0
```

## 🔄 **TDD Workflow Commands**

### Test-First Development Cycle (Following dbt Best Practices)
```bash
# 1. Write schema with tests first (RED phase)
# Create models/staging/_models.yml with data_tests defined
dbt parse  # Validate YAML syntax

# 2. Run tests to confirm failure
dbt test --select stg_new_model --store-failures

# 3. Implement model (GREEN phase)  
dbt run --select stg_new_model

# 4. Verify tests pass
dbt test --select stg_new_model

# 5. Build with dependencies (includes run + test)
dbt build --select +stg_new_model+

# 6. Refactor if needed (REFACTOR phase)
dbt run --select stg_new_model --full-refresh
dbt test --select stg_new_model  # Verify after refactor
```

### Continuous Testing (Best Practice Commands)
```bash
# Run all tests with failure storage for debugging
dbt test --store-failures

# Test specific model and its dependencies (upstream + downstream)
dbt test --select +my_model+

# Build command (recommended) - runs models and tests in dependency order
dbt build --select my_model

# Test primary keys on all models (critical first step)
dbt test --select config.tags:primary_key

# Test by layer using selectors
dbt test --select fqn:*staging*     # Test all staging models
dbt test --select fqn:*marts*      # Test all mart models

# Performance-aware testing with limited scope
dbt build --select my_model --full-refresh
```

## 📊 **Testing Strategy by Component**

### dbt Models (Following Official Best Practices)
- **Primary Key Tests**: Always test uniqueness and not_null on primary keys
- **Generic Tests**: Use built-in tests (unique, not_null, accepted_values, relationships)
- **Custom Generic Tests**: Create reusable, parameterized tests for business rules
- **Singular Tests**: Use .sql files in tests/ for one-off, specific assertions
- **Documentation**: Include descriptions with all tests for clarity
- **Test Organization**: Use _models.yml files in each layer directory
- **Freshness Tests**: Test source data recency and availability

### Snowflake Queries  
- **Performance tests**: Query execution time validation
- **Resource tests**: Warehouse usage monitoring
- **Cost tests**: Query cost thresholds

### Tableau Dashboards
- **Load tests**: Dashboard rendering time
- **Data tests**: Correct data display validation
- **User tests**: Navigation and interaction flows

### Orchestra Pipelines
- **Schedule tests**: Pipeline timing validation
- **Dependency tests**: Proper task sequencing
- **Error handling tests**: Failure recovery validation

## 🛠️ **Testing Utilities**

### Custom Generic Test Macros (Following dbt Best Practices)
```sql
-- macros/test_row_count_between.sql
{% test row_count_between(model, min_count, max_count) %}
  select count(*) as row_count
  from {{ model }}
  having count(*) not between {{ min_count }} and {{ max_count }}
{% endtest %}

-- Usage in _models.yml:
-- data_tests:
--   - row_count_between:
--       min_count: 1000
--       max_count: 50000
```

### Advanced Testing Patterns
```sql
-- macros/test_unique_combination_of_columns.sql  
{% test unique_combination_of_columns(model, combination_of_columns) %}
  select 
    {{ combination_of_columns | join(', ') }},
    count(*) as occurrences
  from {{ model }}
  group by {{ combination_of_columns | join(', ') }}
  having count(*) > 1
{% endtest %}
```

### Test Data Generation
```sql
-- macros/generate_test_data.sql
{% macro generate_test_customers(count=100) %}
  select 
    'CUST_' || seq as customer_id,
    'Test Customer ' || seq as customer_name,
    current_date - (seq % 365) as created_date
  from table(generator(rowcount => {{ count }}))
{% endmacro %}
```

## 📋 **Testing Checklist**

### Before Implementation (Following dbt Best Practices)
- [ ] Write failing tests first (TDD approach)
- [ ] Define success criteria and business logic requirements
- [ ] Set performance expectations and thresholds
- [ ] Plan test data requirements and create seed files if needed
- [ ] Document test purpose in schema YAML files
- [ ] Plan incremental model testing strategy (if applicable)
- [ ] Consider cross-project dependencies for large projects

### During Development (Best Practice Workflow)
- [ ] Run tests frequently using `dbt build` for efficiency
- [ ] Keep tests simple and focused on single assertion
- [ ] Test edge cases and error conditions
- [ ] Document test purpose and expectations in YAML descriptions
- [ ] Use version control branches for feature development
- [ ] Implement code reviews via Pull Requests
- [ ] Use model selection syntax to limit data processing during development
- [ ] Test incremental models with `--full-refresh` when logic changes

### After Implementation (Production Readiness)
- [ ] All tests pass consistently across environments
- [ ] Performance meets requirements (use incremental models for >1M rows)
- [ ] No false positives/negatives in test results
- [ ] Tests are maintainable and documented
- [ ] Unique keys defined for incremental models (no nulls)
- [ ] Schema change handling configured (`on_schema_change`)
- [ ] CI/CD pipeline includes slim CI for modified models only
- [ ] Tests cover primary keys with uniqueness and not_null assertions

## 🚀 **Advanced Testing Strategies**

### Incremental Model Testing
```bash
# Test incremental models with schema changes
dbt run --select incremental_model --full-refresh
dbt test --select incremental_model

# Test with incremental predicates for performance
dbt run --select incremental_model --vars '{"start_date": "2024-01-01"}'
```

### CI/CD Integration Testing
```bash
# Slim CI - only test changed models (recommended for large projects)
dbt build --select state:modified+ --defer --state ./previous-state

# Test downstream impact
dbt test --select +changed_model+ --exclude changed_model
```

This comprehensive testing framework implements Claude Code's **test-driven development** best practice specifically for data analytics workflows, enhanced with official dbt best practices for large-scale projects.