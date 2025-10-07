# Filter Auto-Reset Logic Test Plan

**Date**: 2025-09-30
**Status**: ✅ IMPLEMENTATION VERIFIED

## Implementation Review

### 🔍 Auto-Reset Logic Flow

**Trigger Points**:
1. `setFilter()` when key is `shared_batch_type` or `shared_is_proof`
2. `setFilters()` when `shared_batch_type` or `shared_is_proof` included in update

**Implementation**: `src/store/financialStore.ts:454-509`

```typescript
checkAndResetBatchId: async () => {
  // 1. Check if batch_type or is_proof changed
  if (batch_type changed OR is_proof changed) {
    // 2. Fetch new batch options for updated filter combination
    const batchOptions = await queryBatchOptions(batch_type, is_proof);

    // 3. Get max batch_id (first item after 'All')
    const maxBatchId = batchOptions[1] || 'All';

    // 4. Update filters with new batch_id
    set({ filters: { ...filters, shared_batch_id: maxBatchId } });

    // 5. Update previousFilters to track change
    set({ previousFilters: { batch_type, is_proof } });

    // 6. Invalidate relevant caches
    invalidateCache('out_of_balance');
    invalidateCache('journal_data');
  }
}
```

### ✅ Implementation Strengths

1. **Atomic Operations**: Filter update → auto-reset → cache invalidation → data refresh
2. **Error Handling**: Gracefully handles API failures, still updates previousFilters
3. **Console Logging**: Detailed logging for debugging filter changes
4. **Cache Invalidation**: Properly clears stale data after filter changes
5. **Cross-Tab Persistence**: Works across tab switches via shared store state

### 🧪 Manual Test Plan

#### Test Scenario 1: Batch Type Change (Single Tab)
**Steps**:
1. Navigate to Sales Journal tab
2. Set filters: batch_type='CASH', is_proof='Y'
3. Note current batch_id value
4. Change batch_type to 'CREDIT'
5. Observe console logs for "Filter change detected"

**Expected Results**:
- ✅ batch_id automatically resets to max for CREDIT/Y combination
- ✅ Console shows: "Filter change detected, resetting batch_id..."
- ✅ Console shows: "Auto-reset batch_id to: [new_value]"
- ✅ Journal data refreshes with new filters
- ✅ Out of Balance card updates (if proof='Y')

#### Test Scenario 2: Proof Mode Change (Single Tab)
**Steps**:
1. Navigate to Sales Journal tab
2. Set filters: batch_type='CASH', is_proof='Y'
3. Note current batch_id value
4. Change is_proof to 'N'
5. Observe console logs

**Expected Results**:
- ✅ batch_id automatically resets to max for CASH/N combination
- ✅ Console shows filter change detected
- ✅ Out of Balance card disappears (proof mode disabled)
- ✅ Journal data refreshes

#### Test Scenario 3: Cross-Tab Filter Persistence
**Steps**:
1. Navigate to Sales Journal tab
2. Set filters: batch_type='CASH', is_proof='Y', batch_id='12345'
3. Switch to Dashboard tab
4. Verify filter state in Dashboard components
5. Switch to Out of Balance tab
6. Verify same filters applied

**Expected Results**:
- ✅ All tabs show same batch_type='CASH'
- ✅ All tabs show same is_proof='Y'
- ✅ All tabs show same batch_id='12345'
- ✅ Filter changes on one tab reflect on all tabs

#### Test Scenario 4: Auto-Reset Across Tab Switches
**Steps**:
1. Navigate to Sales Journal tab
2. Set filters: batch_type='CASH', is_proof='Y'
3. Note batch_id value (e.g., '12345')
4. Switch to Dashboard tab
5. Change batch_type to 'CREDIT' (via any filter UI on Dashboard)
6. Switch back to Sales Journal tab
7. Observe batch_id value

**Expected Results**:
- ✅ batch_id on Sales Journal tab shows new max for CREDIT/Y
- ✅ NOT '12345' (previous CASH batch_id)
- ✅ Data on Sales Journal reflects new CREDIT batch

#### Test Scenario 5: Multiple Filter Changes
**Steps**:
1. Navigate to Sales Journal tab
2. Change batch_type: CASH → CREDIT
3. Observe batch_id auto-reset
4. Immediately change is_proof: Y → N
5. Observe second batch_id auto-reset
6. Change batch_type: CREDIT → INTRA
7. Observe third batch_id auto-reset

**Expected Results**:
- ✅ Each batch_type or is_proof change triggers auto-reset
- ✅ batch_id updates three times total
- ✅ Final batch_id = max for INTRA/N combination
- ✅ Data refreshes after each change
- ✅ No race conditions or stale data

#### Test Scenario 6: API Failure Handling
**Steps**:
1. Simulate API failure (disconnect backend or mock error)
2. Change batch_type: CASH → CREDIT
3. Observe console errors
4. Verify previousFilters still updated
5. Reconnect backend
6. Change is_proof: Y → N
7. Verify auto-reset resumes

**Expected Results**:
- ✅ Console shows error: "Error auto-resetting batch_id:"
- ✅ previousFilters still updated (prevents infinite retry)
- ✅ Filter state remains consistent
- ✅ Auto-reset works again after reconnection

#### Test Scenario 7: Cache Invalidation
**Steps**:
1. Navigate to Sales Journal tab
2. Load data with batch_type='CASH', is_proof='Y'
3. Wait for cache to populate (check cacheTimestamps)
4. Change batch_type to 'CREDIT'
5. Verify caches invalidated
6. Observe data refetch from API (not cache)

**Expected Results**:
- ✅ `out_of_balance` cache cleared
- ✅ `journal_data` cache cleared
- ✅ Fresh data fetched from API
- ✅ No stale cached data shown

### 🎯 Acceptance Criteria

**All tests must pass**:
- [ ] Single-tab batch_type change triggers auto-reset
- [ ] Single-tab is_proof change triggers auto-reset
- [ ] Filters persist across tab switches
- [ ] Auto-reset works across tab switches
- [ ] Multiple consecutive changes handled correctly
- [ ] API failures handled gracefully
- [ ] Cache invalidation works properly

### 🐛 Known Edge Cases

**Edge Case 1**: Rapid filter changes
- **Scenario**: User changes batch_type and is_proof within 100ms
- **Expected**: Both changes queued, auto-reset called twice
- **Risk**: Potential race condition if API responses out of order
- **Mitigation**: Sequential `await` in setFilter ensures proper order

**Edge Case 2**: No batch options available
- **Scenario**: API returns empty batch options array
- **Expected**: batch_id resets to 'All'
- **Implementation**: `const maxBatchId = batchOptions[1] || 'All';`

**Edge Case 3**: Tab switch during auto-reset
- **Scenario**: User switches tabs while batch options API is pending
- **Expected**: Auto-reset completes, filters persist on original tab
- **Implementation**: Store-based, not component-based, so works correctly

### 📊 Test Execution Checklist

#### Pre-Test Setup
- [ ] Backend API running at http://localhost:8000
- [ ] Frontend running at http://localhost:5175
- [ ] PostgreSQL database accessible
- [ ] Console DevTools open (for log verification)
- [ ] Network tab open (for API call monitoring)

#### During Testing
- [ ] Monitor console logs for filter change messages
- [ ] Verify network requests for `/api/journal/batch-options`
- [ ] Check Zustand DevTools for state updates
- [ ] Observe UI updates in real-time
- [ ] Test on multiple browsers (Chrome, Firefox, Safari)

#### Post-Test Validation
- [ ] All acceptance criteria met
- [ ] No console errors during test execution
- [ ] Data integrity maintained across all scenarios
- [ ] Performance acceptable (auto-reset < 1 second)
- [ ] User experience smooth (no flickering or race conditions)

### ✅ Conclusion

**Implementation Status**: ✅ COMPLETE

The filter auto-reset logic is correctly implemented with:
1. Proper trigger points (`setFilter` and `setFilters`)
2. Robust error handling
3. Cache invalidation
4. Cross-tab persistence via shared store
5. Console logging for debugging

**Next Step**: Execute manual test plan with qa-coordinator before marking feature as production-ready.
