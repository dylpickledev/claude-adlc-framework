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
# models/staging/stg_customers.yml
models:
  - name: stg_customers
    tests:
      - unique:
          column_name: customer_id
      - not_null:
          column_name: customer_id
    columns:
      - name: customer_id
        tests:
          - relationships:
              to: ref('stg_orders')
              field: customer_id
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

### Test-First Development Cycle
```bash
# 1. Write test first (RED phase)
echo "select count(*) from {{ ref('new_model') }} having count(*) = 0" > tests/assert_new_model_has_data.sql

# 2. Run test to confirm failure
dbt test --select test_name:assert_new_model_has_data

# 3. Implement model (GREEN phase)  
dbt run --select new_model

# 4. Verify test passes
dbt test --select test_name:assert_new_model_has_data

# 5. Refactor if needed (REFACTOR phase)
dbt run --select new_model --full-refresh
```

### Continuous Testing
```bash
# Run all tests with failure storage
dbt test --store-failures

# Test specific model and its dependencies
dbt test --select +my_model+

# Performance testing with profiling
dbt run --select my_model --profiles-dir ./profiles --profile performance_test
```

## 📊 **Testing Strategy by Component**

### dbt Models
- **Schema tests**: Data type validation, uniqueness, nulls
- **Custom tests**: Business rule validation
- **Freshness tests**: Data recency checks

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

### Custom Test Macros
```sql
-- macros/test_row_count_between.sql
{% test row_count_between(model, min_count, max_count) %}
  select count(*)
  from {{ model }}
  having count(*) not between {{ min_count }} and {{ max_count }}
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

### Before Implementation
- [ ] Write failing tests first
- [ ] Define success criteria
- [ ] Set performance expectations
- [ ] Plan test data requirements

### During Development
- [ ] Run tests frequently
- [ ] Keep tests simple and focused
- [ ] Test edge cases and error conditions
- [ ] Document test purpose and expectations

### After Implementation
- [ ] All tests pass consistently
- [ ] Performance meets requirements
- [ ] No false positives/negatives
- [ ] Tests are maintainable

This comprehensive testing framework implements Claude Code's **test-driven development** best practice specifically for data analytics workflows.