# dbt_cloud Repository: Issues Without Linked PRs

**Analysis Date**: 2025-08-28  
**Total Open Issues**: 25+  
**Issues Without PRs**: 18  
**Issues With PRs**: 7  

## Issues WITHOUT Linked PRs (Priority for Swarm)

### 🔴 CRITICAL - Data Integrity Issues

#### #1822 - unique_stg_quarrycamera__camera_stg_quarrycamera_camera_primary_key
- **Impact**: MASSIVE - 5,388,082 duplicate records  
- **System**: Quarry Camera staging data
- **Status**: No PR found  
- **Risk**: Data corruption, storage costs, downstream cascade failures
- **Swarm Agents**: dbt-expert, snowflake-expert, dlthub-expert

#### #1806 - unique_stg_fuelcloud__concrete_fuel_usage_stg_fuelcloud_concrete_primary_key  
- **Impact**: HIGH - 1,820 duplicate records (warning level)
- **System**: Fuel/Concrete usage data
- **Status**: No PR, marked "ignore" but actively failing
- **Risk**: Fuel usage reporting inaccuracies  
- **Swarm Agents**: dbt-expert, snowflake-expert

### 🟡 HIGH - Schema & Compilation Errors

#### #1805 & #1802 - rpt_r468_reseller_and_non_taxable_customers (Schema Errors)
- **Impact**: HIGH - Compilation failures blocking report
- **Error**: `invalid identifier 'PRIMARY_KEY'`
- **System**: Sales reporting  
- **Status**: No PR found
- **Risk**: Sales reports completely broken
- **Swarm Agents**: dbt-expert, business-context

#### #1801 - not_null_fact_safety_incident_responses_smartsheet_join_case_no
- **Impact**: HIGH - 2 null records in safety data
- **System**: Safety incident reporting
- **Status**: No PR found  
- **Risk**: Safety compliance reporting gaps
- **Swarm Agents**: dbt-expert, business-context

### 🟠 MEDIUM - Data Quality & Validation Issues

#### #1800 - Inventory Ledger Cross-System Validation Failures  
- **Impact**: MEDIUM - 25 discrepancies (escalated from 1-2)
- **System**: JDE F4111 vs Data Mart reconciliation
- **Status**: No PR found (comprehensive analysis available)
- **Risk**: Inventory accuracy issues, trend escalating  
- **Swarm Agents**: dbt-expert, snowflake-expert, business-context

#### #1804 - unique_fact_fuel_truck_summary_fact_fuel_truck_summary_unique_key
- **Impact**: MEDIUM - 4 duplicate records
- **System**: Fuel truck summary facts
- **Status**: No PR found (marked "ignore" but still failing)
- **Risk**: Fuel usage analytics inaccuracies
- **Swarm Agents**: dbt-expert, snowflake-expert

#### #1799 & #1778 - stg_accounting_master_units (Duplicates)
- **Impact**: MEDIUM - 1,284 duplicate records  
- **System**: Accounting master data
- **Status**: Model skipped, no PR found
- **Risk**: Accounting data integrity issues
- **Swarm Agents**: dbt-expert, dlthub-expert

#### #1798 & #1777 - src_accounting__master_units (Source Duplicates)
- **Impact**: MEDIUM - 107 duplicate records at source
- **System**: Accounting source data
- **Status**: No PR found  
- **Risk**: Root cause of downstream accounting issues
- **Swarm Agents**: dlthub-expert, dbt-expert

#### #1791 - dm_master__tickets_view (Validation Failures)
- **Impact**: MEDIUM - Multiple metric validation failures (13, 1, 2 records)
- **System**: Master tickets reporting
- **Status**: No PR found
- **Risk**: Dashboard metric accuracy issues
- **Swarm Agents**: dbt-expert, tableau-expert, business-context

#### #1788 - bt4_rpt_stock_receipt_reconciliation (Warning Level)
- **Impact**: LOW-MEDIUM - 2 duplicate records (warning only)  
- **System**: Stock receipt reconciliation
- **Status**: No PR found
- **Risk**: Inventory reconciliation accuracy
- **Swarm Agents**: dbt-expert, business-context

### 🟢 LOW - Minor Issues

#### #1759 & #1758 - rpt_r468_reseller_and_non_taxable_customers (Legacy)
- **Impact**: LOW - Same as #1805/#1802 but older
- **Status**: No PR, likely superseded by newer issues
- **Action**: Should be consolidated or closed

#### #1752 - unique_stg_fuelcloud__concrete_fuel_usage (Legacy)  
- **Impact**: LOW - Same as #1806 but older
- **Status**: No PR, marked "ignore"
- **Action**: Should be consolidated with #1806

#### #1750, #1749, #1751 - Various Legacy Test Failures
- **Impact**: LOW - Historical failures, marked "ignore"  
- **Status**: No PRs, marked for ignoring
- **Action**: Clean up or consolidate

## Issues WITH Linked PRs (In Progress)

1. **#1822** → PR #1823, #1824 (quarrycamera fixes)
2. **#1797** → PR #1819 (value-added freight duplicates)  
3. **#1796** → PR #1818 (safety inspections null tests)
4. **#1795, #1792, #1789** → PR #1816 (fuel truck duplicates)
5. **#1793** → PR #1820 (construction cost reporting)
6. **#1804, #1751** → PR #1816 (fuel truck summary)
7. **Schema errors** → PR #1814 (column reference errors)

## Prioritized Swarm Targets

### Swarm Test #1: Quarry Camera Crisis (Issue #1822)
**Agents**: dbt-expert, snowflake-expert, dlthub-expert
**Focus**: 5.3M duplicate records - immediate data integrity threat

### Swarm Test #2: Schema Compilation Failures (Issues #1805, #1802, #1759, #1758)  
**Agents**: dbt-expert, business-context
**Focus**: Sales reports completely broken due to schema errors

### Swarm Test #3: Cross-System Validation Escalation (Issue #1800)
**Agents**: dbt-expert, snowflake-expert, business-context  
**Focus**: Inventory discrepancies trending upward (1-2 → 25 failures)

### Swarm Test #4: Accounting Data Integrity (Issues #1799, #1778, #1798, #1777)
**Agents**: dbt-expert, dlthub-expert, snowflake-expert
**Focus**: Root cause analysis of accounting master data duplicates

## D&A Impact Framework

### CRITICAL (Immediate Action Required)
- Massive data corruption (>1M records)
- Complete system/report failures
- Compilation errors blocking development

### HIGH (This Week)  
- Schema errors preventing report generation
- Safety/compliance data quality issues
- Escalating trend failures

### MEDIUM (Next 2 Weeks)
- Cross-system validation failures  
- Data quality issues affecting accuracy
- Performance impacts from duplicates

### LOW (Next Month)
- Warning-level issues
- Legacy/duplicate issue cleanup
- Process improvements

---

**Recommended First Swarm Test**: Issue #1822 (Quarry Camera) - Massive scale, clear impact, multiple system coordination needed.