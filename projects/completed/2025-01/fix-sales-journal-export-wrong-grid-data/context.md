# Context: Fix Sales Journal Export Wrong Grid Data

## Problem Confirmed ✅

**Root Cause**: `downloadCSV()` and `downloadPDF()` functions in `src/utils/formatters.ts` are hardcoded to export only Sales Journal columns, not Detail by Ticket columns.

### Evidence

**File**: `src/utils/formatters.ts:121-159`

```typescript
export const downloadCSV = (data: JournalEntry[], filename: string = 'sales-journal'): void => {
  // Hardcoded to Sales Journal columns
  const headers = [
    'Account Code Adjusted',
    'Batch Type',
    'Invalid Account',
    'Account Entry Qty',
    'Amount'
  ];

  // Only accessing Sales Journal fields
  ...data.map(row => [
    `"${row.accountcode_adjusted}"`,
    `"${row.batch_type}"`,
    `"${row.invalid_acount}"`,
    row.account_entry_qty,
    row.amount
  ].join(','))
```

**Type Safety Issue**: Function expects `JournalEntry[]` but `DetailByTicket.tsx` passes `DetailEntry[]`. TypeScript allows this because both types share some common fields.

### What's Happening

1. DetailByTicket component calls: `downloadCSV(detailData || [], 'detail-by-ticket')`
2. `detailData` is type `DetailEntry[]` with fields like: `ticket_number`, `item_id`, `customer`, `sale_date`, etc.
3. `downloadCSV()` receives the data but only extracts Sales Journal fields
4. Result: CSV contains wrong columns with undefined/missing data

## Solution Approach

**Option 1: Generic Export Function** (RECOMMENDED)
- Make `downloadCSV()` and `downloadPDF()` accept any data type
- Automatically detect columns from data keys
- Pass custom headers if needed

**Option 2: Separate Export Functions**
- Create `downloadDetailCSV()` and `downloadDetailPDF()`
- Keep original functions for Sales Journal
- More explicit but more duplication

**Recommendation**: Option 1 - Single generic export function with column detection

## Implementation Plan

1. Update `downloadCSV()` to accept generic data type and auto-detect columns
2. Update `downloadPDF()` to accept generic data type and auto-detect columns
3. Update `downloadExcel()` (currently placeholder) for future use
4. Test both Sales Journal and Detail by Ticket exports
5. Verify CSV/PDF contain correct columns

## Files to Modify

- ✅ Read: `src/components/pages/DetailByTicket.tsx:318-329` (export handlers)
- ✅ Read: `src/utils/formatters.ts:121-303` (export functions)
- 🔧 Modify: `src/utils/formatters.ts` (make exports generic)
- 🧪 Test: Sales Journal exports still work
- 🧪 Test: Detail by Ticket exports now work

## Branch & PR

- **Branch**: `fix/export-wrong-grid-data`
- **Issue**: #36
- **PR**: #37
- **Status**: ✅ Implemented and ready for review

## Implementation Summary

### Changes Made

1. **`downloadCSV()` - Now Generic**
   - Auto-detects columns from first data row keys
   - Converts snake_case to Title Case headers
   - Proper CSV escaping for commas and quotes
   - Handles null/undefined values

2. **`downloadPDF()` - Now Generic**
   - Auto-detects columns dynamically
   - Smart formatting based on column names:
     - Columns with "amount" or "price" → formatCurrency()
     - Columns with "qty" or "quantity" → formatNumber(2 decimals)
     - Columns with "date" → formatDate()
   - Reduced font size for more columns (11px)

3. **`downloadExcel()` - Updated for Consistency**
   - Changed function signature to accept `any[]`
   - Updated comments to reflect generic nature

### Test Results

- ✅ TypeScript compilation successful
- ✅ Vite build successful (9.73s)
- ✅ No type errors
- 🧪 Awaiting manual testing in browser

### Deployment Notes

- Changes only affect export functions, no API changes
- Backward compatible with Sales Journal exports
- Should work for any future data grids added
