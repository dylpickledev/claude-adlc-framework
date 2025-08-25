# Critical Schema/Column Reference Errors Analysis

## Task Overview
Analyze and create fix plan for critical schema compilation errors in graniterock/dbt_cloud repository.

## Specific Issues to Investigate
- **Issues**: #1805, #1802, #1759, #1758
- **Model**: `rpt_r468_reseller_and_non_taxable_customers`  
- **Problem**: Tests reference `PRIMARY_KEY` but actual column is `APEX_CUSTOMERS_PRIMARY_KEY`
- **Error**: `000904 (42000): SQL compilation error: invalid identifier 'PRIMARY_KEY'`
- **Location**: `models/marts/sales/dashboards_reports/sales_dash_reports.yml`

## Research Requirements
1. Examine actual model schema using dbt-mcp tools
2. Identify exact column names vs test expectations
3. Locate test configuration files causing errors
4. Create detailed fix plan with before/after changes
5. Provide implementation steps for immediate execution

## Expected Deliverables
1. Current model schema analysis
2. Test configuration causing errors
3. Exact changes needed (before/after)
4. Step-by-step implementation plan

## Context
- Database compilation errors are blocking other dbt work
- Issue affects sales reporting model in production environment
- Fix is straightforward column name reference update
- High priority for immediate resolution