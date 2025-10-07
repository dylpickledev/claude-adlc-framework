# Streamlit Sales Journal Reference - Complete Analysis

**Source File**: `/Users/TehFiestyGoat/da-agent-hub/da-agent-hub/projects/active/feature-salesjournaltoreact/working/working_mostly_9_25.py`
**Lines**: 4775
**Purpose**: Authoritative reference for React migration

---

## 🎯 CRITICAL CONSTANTS

### Orchestra Pipeline IDs (lines 990-991)
```python
REFRESH_PIPELINE_ID = "c468dd21-7af0-4892-9f48-d8cdf24d9b7d"  # Original pipeline for refresh
FINAL_PIPELINE_ID = "daa39221-b30f-4b27-a8ee-a1b98ca28d0f"   # New pipeline for finalize
```

### Configuration Constants (lines 992-994)
```python
DB_TIMEOUT = 30
CACHE_TTL = 300  # 5 minutes
MAX_RETRIES = 3
```

### Orchestra API Base URL
```python
"https://app.getorchestra.io"
```

---

## 🗄️ DATABASE TABLES

### Primary Tables Used:
1. **dash_r245a_apex_sales_journal_review_summary** - Main journal data
   - Columns: `accountcode_adjusted`, `batch_type`, `error`, `account_entry_qty`, `amount`, `batch_id`, `is_proof`, `branch_id`
   - Used in: Sales Journal tab, Balance queries

2. **dash_r245a_apex_sales_journal_review_detail** - Detailed journal entries
   - Columns: `branch_id`, `item_id`, `ticket_number`, `bol_other_ticket_number`
   - Used in: Detail by Ticket tab, Branch ID dropdown

3. **dash_r245a_apex_sales_journal_review_out_of_balance** - Out of balance data
   - Columns: `batch_type`, `batch_id`, `amount`
   - Used in: Out of Balance total calculations

4. **rpt_r245t_apex_sales_journal_tieout_app_only** - Tieout status
   - Columns: `batch_type`, `batch_id`, `is_proof`, `test`
   - Used in: Tieout Management tab, Batch ID dropdown

5. **fact_aws_dms__status** - DMS replication status
   - Columns: `replication_task`, `task_status`, `task_status_last_updated`, `pending_changes`, `replication_last_updated`
   - Used in: Tieout Records status card

### Database Connection (lines 1011-1045)
- Host: `postgres.grc-ops.com`
- Port: `5432`
- Database: `fellowship_of_data`
- Credentials: Retrieved from Snowflake secrets manager
- Timeout: 30 seconds
- SSL Mode: `require`

---

## 🔐 AUTHENTICATION & SECRETS

### Orchestra Token (lines 997-1008)
```python
def get_orchestra_token() -> Optional[str]:
    """Get Orchestra token from Snowflake secrets with error handling"""
    token = _snowflake.get_generic_secret_string('orchestra_token')
```

### PostgreSQL Credentials (lines 1023-1024)
```python
username = _snowflake.get_generic_secret_string('postgres_username')
password = _snowflake.get_generic_secret_string('postgres_password')
```

---

## 📊 SESSION STATE VARIABLES (lines 1330-1354)

### Pipeline State
- `pipeline_run_id`: Current pipeline run ID
- `pipeline_type`: 'refresh' or 'final'
- `pipeline_status`: Current pipeline status object
- `run_details`: Detailed run information
- `pending_refresh`: Flag for expected refresh
- `last_run_time`: Last pipeline execution time

### Navigation State
- `active_tab_index`: Current tab (0-9)
  - 0 = Dashboard
  - 1 = Sales Journal
  - 2 = Detail by Ticket
  - 3 = Out of Balance
  - 4 = 1140 Research
  - 5 = Pipeline Control
  - 6 = Tieout Management
  - 7 = Pipeline History
  - 8 = Documentation
  - 9 = Debug

### Filter State (Shared across tabs)
- `shared_batch_type`: 'CASH' | 'CREDIT' | 'INTRA' (default: 'CASH')
- `shared_is_proof`: 'Y' | 'N' (default: 'Y')
- `shared_batch_id`: Batch ID or 'All' (default: max_batch_id)
- `shared_invalid_account`: Invalid account filter or 'All'
- `shared_accountcode`: Account code search filter
- `previous_batch_type`: Track batch type changes
- `previous_is_proof`: Track proof changes

### Detail Tab Filters
- `detail_item_id`: Item ID filter
- `detail_ticket_number`: Ticket number filter
- `detail_bol_other_ticket`: BOL/Other ticket filter
- `detail_branch_id`: Branch ID filter

### Research Tab Filters
- `ticket_number_1140`: 1140 research ticket number

### Out of Balance Cache
- `out_of_balance_total`: Cached total (default: 0.0)
- `out_of_balance_color`: Cached color (default: "gray")
- `out_of_balance_filters`: Filter state tracker

### UI State
- `show_finalize_confirmation`: Finalize confirmation dialog flag

---

## 🔄 ORCHESTRA API FUNCTIONS

### 1. Trigger Pipeline (lines 1411-1449)
```python
def trigger_pipeline(pipeline_id: str, pipeline_type: str) -> Optional[Dict]:
    """Trigger an Orchestra pipeline with comprehensive error handling"""
    url = f"https://app.getorchestra.io/engine/public/pipelines/{pipeline_id}/start"
    # POST request with bearer token
    # Returns: {"pipelineRunId": "...", ...}
```

### 2. Get Pipeline Status (lines 1452-1483)
```python
def get_pipeline_status(pipeline_run_id: str) -> Optional[Dict]:
    """Get the status of a pipeline run with error handling"""
    url = "https://app.getorchestra.io/api/engine/public/pipeline_runs"
    params = {"pipeline_run_ids": pipeline_run_id}
    # Returns: First result from results array
```

### 3. Get Pipeline History (lines 1486-1536)
```python
def get_pipeline_history(pipeline_ids: List[str], limit: int = 10) -> Optional[List[Dict]]:
    """Get the last few runs of specific pipelines with error handling"""
    # Paginates through up to 10 pages
    # Filters for specific pipeline IDs: [REFRESH_PIPELINE_ID, FINAL_PIPELINE_ID]
    # Sorts by createdAt descending
    # Returns: List of pipeline runs limited to specified count
```

**IMPORTANT**: Pipeline history DOES filter by specific pipeline IDs when provided. Dashboard calls it with:
```python
history_data = get_pipeline_history([REFRESH_PIPELINE_ID, FINAL_PIPELINE_ID], limit=5)
```

---

## 🎨 DASHBOARD TAB (lines 3421-3794)

### Pipeline Status Card Logic (lines 3463-3517)
```python
current_status = ""
if st.session_state.pipeline_status:
    current_status = st.session_state.pipeline_status.get("runStatus", "").upper()

if current_status in ["RUNNING", "CREATED", "QUEUED"]:
    status_color = "#E67E22"
    status_text = "RUNNING"
    status_icon = "🔄"
    description = "Pipeline is currently processing"
elif current_status == "SUCCEEDED":
    status_color = "#27AE60"
    status_text = "READY"
    status_icon = "✅"
    description = "System is ready for operations"
elif current_status == "FAILED":
    status_color = "#C0392B"
    status_text = "FAILED"
    status_icon = "❌"
    description = "Pipeline requires attention"
else:
    status_color = "#7F8C8D"
    status_text = "IDLE"
    status_icon = "⏸️"
    description = "No active pipeline operations"
```

### DMS Status Card Logic (lines 3519-3570)
```python
# Query DMS status
query = "SELECT task_status FROM dbt_dev_utils.fact_aws_dms__status"
data = query_postgres(query)

if data is not None and not data.empty:
    all_change_processing = (data['task_status'] == 'CHANGE PROCESSING').all()

    if all_change_processing:
        status_color = "#27AE60"  # Green
        status_text = "CHANGE PROCESSING"
        status_icon = "✅"
        description = f"{len(data)} replication tasks running"
    else:
        status_color = "#C0392B"  # Red
        status_text = "ERROR"
        status_icon = "❌"
        description = "Some tasks not processing"
else:
    status_color = "#7F8C8D"  # Gray
    status_text = "UNKNOWN"
    status_icon = "❓"
```

**CRITICAL**: DMS status must check ALL rows. Only return 'CHANGE PROCESSING' if ALL tasks have that status, otherwise 'ERROR'.

### Tieout Status Card (lines 3572-3627)
```python
query = "SELECT test FROM dbt_dev_accounting.rpt_r245t_apex_sales_journal_tieout_app_only LIMIT 100"
data = query_postgres(query)

if data is not None and not data.empty:
    all_ties = (data['test'] == 'TIES').all()

    if all_ties:
        status_color = "#27AE60"
        status_text = "ALL TIED OUT"
        status_icon = "✅"
    else:
        failing_count = (data['test'] != 'TIES').sum()
        status_color = "#C0392B"
        status_text = f"{failing_count} FAILING"
        status_icon = "❌"
```

### Out of Balance Card (lines 3629-3685)
```python
# Get out of balance total from dedicated function
total, color = get_out_of_balance_total(
    st.session_state.shared_batch_type,
    st.session_state.shared_batch_id,
    st.session_state.shared_is_proof
)

# Color logic:
# - red if abs(total) > 0.02
# - green if abs(total) <= 0.02
# - gray if is_proof == 'N' or no data
```

### Recent Pipeline Activity (lines 3687-3761)
```python
with st.spinner("Loading recent activity..."):
    history_data = get_pipeline_history([REFRESH_PIPELINE_ID, FINAL_PIPELINE_ID], limit=5)

if history_data and len(history_data) > 0:
    for i, run in enumerate(history_data[:3]):  # Show only last 3 runs
        pipeline_name = run.get("pipelineName", "Unknown Pipeline")
        started_at = format_timestamp(run.get("startedAt", ""))
        run_status = run.get("runStatus", "UNKNOWN").upper()

        # Status icon mapping:
        status_icons = {
            "SUCCEEDED": "✅",
            "FAILED": "❌",
            "RUNNING": "🔄",
            "QUEUED": "⏳",
            "CREATED": "🆕"
        }
```

---

## 📈 SALES JOURNAL TAB (lines 1953-2185)

### Main Query (lines 1987-2002)
```python
base_query = """
    SELECT accountcode_adjusted,
           batch_type,
           error as invalid_acount,
           SUM(account_entry_qty) AS account_entry_qty,
           SUM(amount) AS amount
    FROM dbt_dev_accounting.dash_r245a_apex_sales_journal_review_summary
"""

# Add WHERE conditions from filters
# GROUP BY 1,2,3 ORDER BY error, accountcode_adjusted
```

### Filter UI Components:
1. **Batch Type Radio** (lines 2066-2074)
   - Options: "CASH", "CREDIT", "INTRA"
   - Key: `shared_batch_type_journal`
   - Triggers: Update session state + invalidate out of balance cache

2. **Proof Radio** (lines 2077-2085)
   - Options: "Y", "N"
   - Key: `shared_is_proof_journal`
   - Triggers: Update session state + invalidate out of balance cache

3. **Batch ID Dropdown** (lines 2089-2098)
   - Options: Dynamic from `get_batch_id_options()`
   - Key: `shared_batch_id_journal`
   - Default: Max batch ID for current filters
   - Triggers: Update session state + invalidate out of balance cache

4. **Invalid Account Dropdown** (lines 2101-2111)
   - Options: Dynamic from `get_invalid_account_options()`
   - Key: `shared_invalid_account_journal`
   - Default: "All"

5. **Account Code Text Input** (lines 2123-2130)
   - Key: `shared_accountcode_journal`
   - Max chars: 50
   - Placeholder: "Enter account code.."

### Display Columns:
- Accountcode Adjusted
- Batch Type
- Invalid Account
- Account Entry Qty (formatted number)
- Amount (formatted currency)

### Metrics Display:
- Total Entry Qty (sum of account_entry_qty)
- Total Amount (sum of amount)

### Export Options:
1. **CSV** - Always available
2. **Excel** - Requires xlsxwriter library
3. **PDF** - Requires matplotlib library (custom multi-page report)

---

## 🔍 HELPER FUNCTIONS

### Query Building (lines 1634-1721)
```python
def build_where_conditions_and_params(
    filters: Dict[str, Any],
    include_detail_filters: bool = False,
    table_name: str = None
) -> Tuple[List[str], Dict[str, Any]]:
    """Build SQL WHERE conditions and parameters based on filters with validation"""

    # Core filters (always applied):
    # - batch_type (required)
    # - is_proof (not for out_of_balance table)
    # - batch_id (if not 'All')
    # - accountcode_adjusted (ILIKE with wildcards)
    # - invalid_account (error column, if not 'All')

    # Detail filters (only if include_detail_filters=True):
    # - item_id (ILIKE with wildcards)
    # - ticket_number (ILIKE with wildcards)
    # - bol_other_ticket_number (ILIKE with wildcards)
    # - branch_id (exact match if not 'All')
```

### Dropdown Options Functions

#### Batch ID Options (lines 1092-1121)
```python
@st.cache_data(ttl=600, show_spinner=False)
def get_batch_id_options(batch_type: str, is_proof: str) -> Tuple[List[str], Optional[str]]:
    """Get distinct batch_id values based on batch_type and is_proof filters
    Returns tuple of (options_list, max_batch_id)"""

    # Query: SELECT DISTINCT batch_id FROM rpt_r245t_apex_sales_journal_tieout_app_only
    # WHERE batch_type = ? AND is_proof = ?
    # ORDER BY batch_id DESC LIMIT 100

    # Returns: (["All", "batch1", "batch2", ...], "batch1")
```

#### Invalid Account Options (lines 1124-1164)
```python
@st.cache_data(ttl=600, show_spinner=False)
def get_invalid_account_options(batch_type: str, is_proof: str, batch_id: str) -> List[str]:
    """Get distinct invalid account (error) values for dropdown based on current filters"""

    # Query: SELECT DISTINCT error FROM dash_r245a_apex_sales_journal_review_summary
    # WHERE batch_type = ? AND is_proof = ? AND batch_id = ? AND error IS NOT NULL
    # ORDER BY error LIMIT 50

    # Returns: ["All", "error1", "error2", ...]
```

#### Branch ID Options (lines 1167-1198)
```python
@st.cache_data(ttl=600, show_spinner=False)
def get_branch_id_options(batch_type: str) -> List[str]:
    """Get distinct branch_id values for dropdown with caching"""

    # Query: SELECT DISTINCT branch_id FROM dash_r245a_apex_sales_journal_review_detail
    # WHERE batch_type = ? AND branch_id IS NOT NULL AND branch_id != '' AND branch_id != 'null'
    # ORDER BY branch_id LIMIT 50

    # Returns: ["All", "branch1", "branch2", ...]
```

### Out of Balance Total (lines 1201-1273)
```python
@st.cache_data(ttl=300, show_spinner=False)
def get_out_of_balance_total(batch_type: str, batch_id: str, is_proof: str) -> Tuple[float, str]:
    """Get the total amount from out of balance table and return (total, color)"""

    # Returns (0.0, "gray") if is_proof == 'N'

    # First checks if journal data exists for filters
    # Then queries: SELECT COALESCE(SUM(amount), 0) as total_amount
    # FROM dash_r245a_apex_sales_journal_review_out_of_balance
    # WHERE batch_type = ? AND batch_id = ?

    # Color logic:
    # - "red" if abs(total) > 0.02
    # - "green" if abs(total) <= 0.02
    # - "gray" if no data or proof disabled
```

### Timestamp Formatting (lines 1539-1585)
```python
def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp for display in Pacific Time with proper DST handling"""

    # Parses ISO format UTC timestamps
    # Determines PST vs PDT based on date
    # Returns: "2025-09-30 08:15:10 PDT"
```

### Currency & Number Formatting (lines 1724-1751)
```python
def safe_format_currency(value: Any) -> str:
    """Safely format currency values"""
    # Returns: "$1,234.56" or "$0.00" if invalid

def safe_format_number(value: Any) -> str:
    """Safely format numeric values"""
    # Returns: "1,234.56" or "0" if invalid

def safe_format_date(date_value: Any) -> str:
    """Safely format date values"""
    # Returns: "09/30/2025" or "" if invalid
```

---

## 🎯 KEY REACT MIGRATION INSIGHTS

### 1. **NO MOCK DATA FALLBACKS**
The React app must show error states when APIs fail, NOT fallback to mock data. User explicitly stated:
> "if the API's fail, dont fall back to mock data generators instead have them say invalid or error or something to let us know the data isn't current"

### 2. **Pipeline Status Logic**
The Dashboard has TWO separate concepts:
- **Pipeline Status Card**: Shows current status of ANY running pipeline (RUNNING/READY/FAILED/IDLE)
- **Recent Pipeline Activity**: Shows last 5 runs from REFRESH and FINAL pipelines specifically

### 3. **DMS Status ALL Rows Check**
Must check ALL rows from `fact_aws_dms__status` table:
- Return 'CHANGE PROCESSING' ONLY if every single row has task_status = 'CHANGE PROCESSING'
- Otherwise return 'ERROR'

### 4. **Filter Auto-Reset**
When `shared_batch_type` or `shared_is_proof` changes:
- Auto-reset `shared_batch_id` to the maximum batch ID for new filters
- Clear out of balance cache
- Tracked via `previous_batch_type` and `previous_is_proof` session state

### 5. **Shared Filter State**
Filters are shared across multiple tabs via session state:
- Sales Journal tab
- Detail by Ticket tab
- Out of Balance tab
- 1140 Research tab

When user changes filters in one tab, they should persist to other tabs.

### 6. **Caching Strategy**
Streamlit uses `@st.cache_data` decorators with TTL:
- 600 seconds (10 minutes): Dropdown options
- 300 seconds (5 minutes): Out of balance data, tieout status

React should implement similar caching to avoid excessive API calls.

### 7. **Query Retries**
PostgreSQL queries retry up to 3 times with exponential backoff on OperationalError.

### 8. **Orchestra API Pagination**
`get_pipeline_history()` paginates through up to 10 pages (100 per page) to find enough matching pipeline runs when filtering by specific pipeline IDs.

---

## 📝 TODOS FOR REACT MIGRATION

1. ✅ Fix mock data fallbacks - COMPLETED
2. ✅ Update DMS status logic to check all rows - COMPLETED
3. ✅ Fix Pipeline Status card - COMPLETED
4. ✅ Update Quick Actions buttons - COMPLETED
5. ⚠️ Verify Recent Pipeline Activity uses correct filtering
6. ⚠️ Implement filter auto-reset on batch_type/is_proof change
7. ⚠️ Add shared filter state management across tabs
8. ⚠️ Implement query caching with TTL
9. ⚠️ Add retry logic for database queries
10. ⚠️ Implement pagination for Orchestra API history

---

## 🔗 KEY STREAMLIT PATTERNS TO REPLICATE

### Session State Management
Streamlit uses `st.session_state` dictionary for global state. React equivalent: Zustand store already in place.

### Filter Change Callbacks
Streamlit uses `on_change` callbacks on inputs. React equivalent: Update Zustand store on change events.

### Data Caching
Streamlit uses `@st.cache_data(ttl=X)` decorator. React equivalent: React Query with `staleTime` or custom cache implementation.

### Error Boundaries
Streamlit has `render_error_boundary()` wrapper function. React equivalent: React Error Boundary component.

### Loading States
Streamlit uses `with st.spinner("Loading...")`. React equivalent: Loading states in Zustand + Skeleton components.

---

## 📊 COMPLETE TAB BREAKDOWN

### Tab 0: Dashboard (DEFAULT)
- 4 Status Cards: Pipeline Status, DMS Status, Tieout Status, Out of Balance
- Recent Pipeline Activity (last 3 of 5 most recent runs)
- No filters on this tab

### Tab 1: Sales Journal
- Main journal data table with aggregated amounts
- Filters: Batch Type, Proof, Batch ID, Invalid Account, Account Code
- Export: CSV, Excel, PDF
- Metrics: Total Entry Qty, Total Amount

### Tab 2: Detail by Ticket
- Detailed line-item data
- Filters: Batch Type, Proof, Batch ID + Detail filters (Item ID, Ticket Number, BOL, Branch ID)
- Export: CSV, Excel

### Tab 3: Out of Balance
- Out of balance records
- Shows records where is_proof='Y' and amount != 0
- Filters: Batch Type, Batch ID (Proof always 'Y')
- Export: CSV

### Tab 4: 1140 Research
- Research specific ticket numbers with 1140 account code
- Filter: Ticket Number input
- Shows related transactions

### Tab 5: Pipeline Control
- Trigger Refresh Pipeline button
- Trigger Finalize Pipeline button (with confirmation)
- Shows current pipeline status with real-time updates

### Tab 6: Tieout Management
- Shows tieout test results
- Filters: Batch Type, Proof, Batch ID
- Status indicators for each test (TIES/DOES NOT TIE)

### Tab 7: Pipeline History
- Full pipeline run history table
- Filters by REFRESH and FINAL pipeline IDs
- Shows all runs with status, timestamps, duration

### Tab 8: Documentation
- Static documentation page
- Usage instructions
- Filter explanations
- System architecture

### Tab 9: Debug
- Technical information
- Session state viewer
- Cache status
- Connection testing

---

**END OF REFERENCE DOCUMENT**
