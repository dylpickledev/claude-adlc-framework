# Project Specification: Fix Sales Journal Export Wrong Grid Data

## Problem Statement
The export buttons (CSV/Excel/PDF) in the "Detail by Ticket Date" tab are exporting data from the Sales Journal summary grid instead of the Detail by Ticket detail grid.

## Expected Behavior
When clicking export buttons in the Detail by Ticket Date tab:
- Should export detail-level data (ticket-level rows)
- Should include columns like: ticket_number, item_id, customer, sale_date, amount, etc.
- Should match what's visible in the Detail by Ticket grid

## Current Behavior
Export buttons appear to be exporting:
- Sales Journal summary data (aggregated by account code)
- Wrong columns (accountcode_adjusted, batch_type, invalid_acount, account_entry_qty, amount)
- Data from a different data source/store

## Investigation Areas

1. **Export Button Component**
   - Find where export buttons are defined in DetailByTicket.tsx
   - Check which data they're passing to export functions
   - Verify they're using `detailData` not `journalData`

2. **Export Functions**
   - Located in: `src/utils/formatters.ts`
   - Functions: `downloadCSV`, `downloadExcel`, `downloadPDF`
   - Check which data parameter they receive

3. **Data Source**
   - Correct source: `detailData` from `useFinancialStore()`
   - Wrong source: `journalData` from `useFinancialStore()`
   - Need to ensure export buttons use correct state

4. **Possible Root Causes**
   - Export buttons hardcoded to use journalData
   - Export buttons copying from SalesJournal component
   - Missing prop to specify which data to export
   - Shared export component using wrong default

## Success Criteria
- [ ] Export buttons in Detail by Ticket tab export detail data
- [ ] CSV export contains ticket-level columns
- [ ] Excel export contains ticket-level columns
- [ ] PDF export contains ticket-level columns
- [ ] Exported data matches what's visible in the grid
- [ ] Sales Journal export still works correctly

## Implementation Plan
1. Locate export button implementation in DetailByTicket.tsx
2. Identify which data source export buttons are using
3. Update export buttons to use `detailData` instead of `journalData`
4. Test all export formats (CSV, Excel, PDF)
5. Verify Sales Journal exports still work
6. Create PR and deploy
7. Test in production
