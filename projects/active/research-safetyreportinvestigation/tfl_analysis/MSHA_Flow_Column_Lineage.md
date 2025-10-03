# MSHA Flow Column Lineage Analysis

## Summary
**Yes, I can extract column lineage from Tableau Prep flow files!** Here's what I found in the MSHA Flow:

## Source Tables Identified
1. **[bisf].[Skill_SK_EmployeeSkill]** - Main employee skills/certifications
2. **[bisf].[Skill_SK_Skill]** - Skills/certification definitions
3. **[dbo].[ActiveEmployees_Branch]** - Active employee data with branch info
4. **[dbo].[ActiveEmployees]** - Basic active employee data
5. **[dbo].[vwEmployeeTitle]** - Employee title information
6. **[bisf].[Safety_Meeting_Topics_Subtopics]** - Meeting topics and subtopics
7. **[bisf].[Safety_SF_Meeting]** - Safety meeting records
8. **[bisf].[Safety_SF_RecordedMeetingEmployee]** - Employee meeting attendance

## Data Flow Structure
The flow performs extensive joins and transformations across these tables to create different certification "containers":

### Key Containers (Output Sets)
- **MSHA** - MSHA-specific certifications
- **Skills** - General skills tracking
- **Calendar** - Calendar-based training
- **Fall** - Fall protection certifications
- **Job Specific** - Job-specific training
- **New hire** - New hire requirements
- **CPR** - CPR certifications
- **And many others...**

## Critical Finding for Investigation
The flow has **NO DATE FILTERS** applied at the flow level:
```json
"filterSettings": {
  "filters": []  // EMPTY - No flow-level date restrictions!
}
```

This means **all date filtering happens in the workbook calculations**, not in the Prep flow.

## Column Lineage Tracing Methodology
The TFL file contains:
1. **Source table mappings** - Which tables feed into the flow
2. **Join relationships** - How tables connect (via SuperJoin nodes)
3. **Transformation logic** - Field mappings and calculations
4. **Output containers** - Final grouped datasets
5. **Published extract name** - "MSHA Datasource"

## Key Insight for Debugging
Since the MSHA flow processes ALL historical data and publishes it to the "MSHA Datasource", the issue with missing October 2025 certifications for EmployeeCode 24184 is likely either:

1. **Source data missing** - The certifications don't exist in [bisf].[Skill_SK_EmployeeSkill]
2. **Workbook filtering issue** - The TWB file's `YEAR([CertificationDate])=YEAR(TODAY())` calculation is filtering them out incorrectly

The flow itself is not applying date filters, so it should pass through all certification records.