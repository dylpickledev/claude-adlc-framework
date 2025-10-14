# Project Completion: Sales Journal Intra Filter Blank Screen

**Created**: 2025-10-13
**Completed**: 2025-10-13
**Status**: ✅ RESOLVED
**Repository**: graniterock/react-sales-journal
**Issue**: [#31](https://github.com/graniterock/react-sales-journal/issues/31)
**PR**: [#34](https://github.com/graniterock/react-sales-journal/pull/34)

## Root Cause

**ACTUAL Issue (Different from Initial Investigation)**:
- TypeError: `Cannot read properties of null (reading 'getTime')`
- Located in: `src/utils/formatters.ts` line 59
- Cause: `formatDate()` function didn't handle null date values
- When INTRA data contained null `sale_date` fields, the component crashed

## Solution Implemented

**File**: `src/utils/formatters.ts`
**Changes**:
1. Updated type signature: `(date: Date | string | null | undefined)`
2. Added null check before any date processing: `if (!date) return 'N/A';`
3. Returns user-friendly 'N/A' instead of crashing

**Code Change**:
```typescript
export const formatDate = (date: Date | string | null | undefined): string => {
  // Handle null/undefined dates before any processing
  if (!date) return 'N/A';

  const dateObj = typeof date === 'string' ? new Date(date) : date;
  if (isNaN(dateObj.getTime())) return 'Invalid Date';

  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(dateObj);
};
```

## Deployment

**Branch**: `fix/null-date-handling-detail-ticket`
**Deployment Method**: GitHub Actions → AWS ECS Fargate
**Status**: ✅ Deployed and verified by user

**Timeline**:
1. PR #34 created
2. PR #34 merged to master
3. GitHub Actions workflow triggered
4. Docker image built and pushed to ECR
5. ECS service updated with new image
6. Deployment completed successfully
7. User confirmed fix is working

## Additional Work: DMS TCP Timeout Fixes

While investigating, also resolved DMS replication issues:

**Problem**: TCP timeout errors when fetching BLOB columns
**Tables Affected**:
- `Tkbatch.CertHash`
- `Tkhist1.CertHash`

**Solution**: DMS transformation rules to exclude BLOB columns

**Table Mappings Updated** (`/tmp/table-mappings-modified.json`):
- Rule #13: Remove `Tkbatch.CertHash` column
- Rule #14: Remove `Tkhist1.CertHash` column

**Result**:
- DMS task resumed from CDC checkpoint (no full reload)
- Zero replication errors
- All tables replicating successfully

## Lessons Learned

### Initial Investigation vs Actual Root Cause
- **Initial hypothesis**: Missing error state handling in component
- **Actual issue**: Null pointer exception in date formatter
- **Key insight**: Browser console errors are critical for React debugging

### TypeScript Null Safety
- Always include `null | undefined` in type signatures when data source quality is uncertain
- Add null checks before any property access (`.getTime()`, `.toString()`, etc.)
- Return user-friendly fallbacks ('N/A', '—') instead of throwing errors

### Financial Data Considerations
- 'N/A' is better than arbitrary default dates (1899, etc.) for missing data
- Clear indication of missing data prevents data quality confusion
- Aligns with accounting standards for missing/incomplete data

### DMS BLOB Column Handling
- Large BLOB columns can cause TCP timeouts in replication
- Transformation rules with `remove-column` action are effective
- Resume processing preserves CDC checkpoint (no full reload)
- Acceptable tradeoff: BLOB data loss vs stable replication

## Patterns Extracted

**PATTERN**: Null-safe utility functions for TypeScript/React
**SOLUTION**: Add null checks before any property access in formatters
**ERROR-FIX**: `TypeError: Cannot read properties of null (reading 'getTime')` → Add `if (!date) return 'N/A';` before accessing date properties

**PATTERN**: DMS BLOB column exclusion for TCP timeout resolution
**SOLUTION**: Use transformation rules with `remove-column` action for large BLOB fields causing replication failures

## References

- Issue: https://github.com/graniterock/react-sales-journal/issues/31
- PR: https://github.com/graniterock/react-sales-journal/pull/34
- AWS DMS Documentation: Table Mapping Rules
- React AG Grid: Date formatter patterns
