# Safety Incident Flow Column Lineage Analysis

## Summary
**Yes, column lineage extracted successfully!** The Safety Incident Flow processes multiple incident-related tables.

## Source Tables Identified
1. **[bisf].[Safety_Incident]** - Main incident records (with DateTimeIncident)
2. **[bisf].[Safety_IncidentForm]** - Incident form details (with DateTimeReported)
3. **[dbo].[ActiveInactiveEmployees_Branch]** - Employee data
4. **[dbo].[ActiveEmployees_Branch_Supervisor_JobType]** - Employee job/supervisor info
5. **[bihj].[HeavyJob_JM_Job]** - HeavyJob project data
6. **[bisf].[Safety_SF_Tag]** - Safety tags
7. **[bisf].[Safety_SF_RecordedIncidentTag]** - Incident tag relationships
8. **[bisf].[Safety_FormsAnalysis]** - Forms analysis data

## Published Data Sources
The flow publishes to **THREE** different data sources:
1. **"ET Summary datasource"** - Main incidents summary (this feeds Late Reporting dashboard)
2. **"HCSS Incident Datasource"** - HCSS-specific incidents
3. **"HCSS and Historical Datasource"** - Combined HCSS and historical data

## Critical Finding for Investigation
The flow has **NO DATE FILTERS** applied at the flow level:
```json
"filterSettings": {
  "filters": null  // NO flow-level date restrictions!
}
```

This means **all historical incident data flows through** - the Late Reporting dashboard should have access to ALL incidents including September 2025 data.

## Key Insight for Debugging
Since the Safety Incident flow processes ALL historical incidents and publishes them to "ET Summary datasource", the issue with missing September 2025 incidents is likely either:

1. **Source data missing** - September 2025 incidents don't exist in [bisf].[Safety_Incident]
2. **Workbook filtering issue** - The Late Reporting workbook is filtering them out incorrectly

## Data Flow Path Confirmed
```
[bisf].[Safety_Incident] → Safety Incident 8.1 Flow → "ET Summary datasource" → Late Reporting.twb
```

The connection chain is correct - the issue must be in the data or workbook logic.