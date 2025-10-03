# Manual Testing Script: Sales Journal Critical Features

## Pre-Testing Setup

### 1. Environment Check
```bash
# Verify servers are running
lsof -i :5176  # Frontend (React)
lsof -i :8000  # Backend (FastAPI)

# Open application
open http://localhost:5176
```

### 2. Browser Setup
- Open Chrome or Safari
- Open Developer Tools (⌘ + Option + I)
- Select Console tab
- Enable "Preserve log" checkbox
- Clear console (⌘ + K)

### 3. Screenshot Directory
```bash
# Create screenshots directory
mkdir -p ~/Desktop/qa-screenshots-$(date +%Y%m%d)
cd ~/Desktop/qa-screenshots-$(date +%Y%m%d)
```

---

## FEATURE 1: Query Retry Logic

### Test 1.1: Normal Operation

**Steps**:
1. Ensure DevTools Console is open and visible
2. Clear console (⌘ + K)
3. Refresh page (⌘ + R)
4. Wait for Dashboard to load
5. **Screenshot 1**: Capture full browser window (Dashboard loaded, console visible)
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/01-normal-operation.png
   ```
6. Note in findings:
   - ✅ Dashboard loads successfully
   - ✅ No retry messages in console
   - ✅ No toast notifications
   - ✅ Data displays correctly

### Test 1.2: Simulated Network Failure

**Steps**:
1. Open Network tab in DevTools
2. Find throttling dropdown (usually says "No throttling")
3. Select "Offline" mode
4. **Screenshot 2**: Capture Network tab showing "Offline"
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/02-offline-mode.png
   ```
5. Try to navigate to Sales Journal tab
6. Watch for:
   - Toast notification appearing (top-right corner)
   - Console messages about retries
7. **Screenshot 3**: Capture retry toast notification
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/03-retry-toast.png
   ```
8. Wait for all 3 retry attempts to complete
9. **Screenshot 4**: Capture final error state
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/04-retry-exhausted.png
   ```
10. Note console output (copy exact text)

### Test 1.3: Retry Recovery

**Steps**:
1. Keep DevTools open with Console visible
2. Set Network to "Slow 3G"
3. Click Dashboard tab to trigger data load
4. Watch for first retry message in console
5. **Immediately** change Network back to "No throttling"
6. Observe:
   - Does data load successfully?
   - Does error state clear?
7. **Screenshot 5**: Capture successful recovery
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/05-retry-recovery.png
   ```

---

## FEATURE 2: Shared Filter State Persistence

### Test 2.1: Cross-Tab Filter Persistence

**Steps**:
1. Navigate to Sales Journal tab
2. Note current filters in sidebar:
   - Batch Type: [Write down value]
   - Proof Mode: [Write down value]
   - Batch ID: [Write down value]
3. **Screenshot 6**: Capture Sales Journal initial state
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/06-sales-journal-initial.png
   ```
4. Change Batch Type from CASH to CREDIT (use dropdown in sidebar)
5. Wait for data to load
6. Switch to Dashboard tab
7. **Screenshot 7**: Capture Dashboard with CREDIT filter
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/07-dashboard-credit-filter.png
   ```
8. Check sidebar - verify Batch Type shows CREDIT
9. Switch to Out of Balance tab
10. **Screenshot 8**: Capture Out of Balance tab
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/08-out-of-balance-filters.png
   ```
11. Switch back to Sales Journal tab
12. **Screenshot 9**: Verify CREDIT still selected
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/09-sales-journal-persist.png
   ```

### Test 2.2: Filter Change Propagation

**Steps**:
1. Navigate to Dashboard tab
2. Current Proof Mode: [Note value]
3. Change Proof Mode from Y to N (use dropdown)
4. **Screenshot 10**: Dashboard after proof mode change
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/10-dashboard-proof-n.png
   ```
5. Observe: Out of Balance card should disappear
6. Switch to Sales Journal tab
7. Check sidebar: Proof Mode should show N
8. **Screenshot 11**: Sales Journal with Proof Mode N
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/11-sales-journal-proof-n.png
   ```

---

## FEATURE 3: Filter Auto-Reset Logic

### Test 3.1: Batch Type Change Auto-Reset

**Steps**:
1. Navigate to Sales Journal tab
2. Ensure Console is visible
3. Set filters:
   - Batch Type: CASH
   - Proof Mode: Y
   - **Write down exact Batch ID value**: ___________
4. **Screenshot 12**: Initial state (CASH/Y/specific batch_id)
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/12-before-batch-type-change.png
   ```
5. Clear console (⌘ + K)
6. Change Batch Type from CASH to CREDIT
7. **IMMEDIATELY** look at console for these messages:
   - "Filter change detected, resetting batch_id..."
   - "Auto-reset batch_id to: [value]"
8. **Screenshot 13**: Console showing auto-reset logs
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/13-console-auto-reset.png
   ```
9. Check Batch ID dropdown - should show NEW value (not old one)
10. **Screenshot 14**: After batch type change (new batch_id)
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/14-after-batch-type-change.png
   ```
11. Copy exact console output to findings document

### Test 3.2: Proof Mode Change Auto-Reset

**Steps**:
1. Set filters:
   - Batch Type: CASH
   - Proof Mode: Y
   - **Write down Batch ID**: ___________
2. Clear console
3. Change Proof Mode from Y to N
4. Watch console for auto-reset logs
5. **Screenshot 15**: Console output
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/15-proof-mode-auto-reset.png
   ```
6. Verify Batch ID changed

### Test 3.3: Cross-Tab Auto-Reset

**Steps**:
1. On Sales Journal tab:
   - Set Batch Type: CASH
   - Set Proof Mode: Y
   - **Write down Batch ID**: ___________ (e.g., 12345)
2. **Screenshot 16**: Sales Journal initial state
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/16-sales-journal-before-cross-tab.png
   ```
3. Switch to Dashboard tab
4. On Dashboard, change Batch Type to CREDIT (use sidebar)
5. Watch console for auto-reset messages
6. **Screenshot 17**: Dashboard after change
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/17-dashboard-cross-tab-change.png
   ```
7. Switch back to Sales Journal tab
8. **VERIFY**:
   - Batch Type shows CREDIT (not CASH)
   - Batch ID is NEW value (NOT 12345)
9. **Screenshot 18**: Sales Journal after cross-tab auto-reset
   ```bash
   screencapture -w ~/Desktop/qa-screenshots-$(date +%Y%m%d)/18-sales-journal-cross-tab-reset.png
   ```

---

## Post-Testing Tasks

### 1. Review All Screenshots
```bash
open ~/Desktop/qa-screenshots-$(date +%Y%m%d)
```
- Verify all 18 screenshots captured
- Ensure screenshots are clear and readable
- Check that relevant UI elements are visible

### 2. Console Output Documentation
- Copy all console messages from testing
- Paste into findings document under "Browser Console Verification"
- Highlight any unexpected errors or warnings

### 3. Update Findings Document
For each test scenario:
- Change Status from [PENDING] to [PASS/FAIL]
- Fill in "Actual Results" section
- Add screenshot references
- Document any deviations from expected behavior

### 4. Issues Identification
If any tests fail:
- Document exact steps to reproduce
- Capture additional screenshots if needed
- Note severity: Critical/High/Medium/Low
- Describe impact on user experience

### 5. Summary Completion
Update Test Summary section:
- Total scenarios: 8
- Passed: [count]
- Failed: [count]
- Calculate pass rate

---

## Quick Reference: Key Things to Watch

### ✅ Success Indicators
- Data loads without errors
- Filters persist across tabs
- Auto-reset triggers on filter changes
- Console logs show expected messages
- No unexpected errors

### ❌ Failure Indicators
- Data doesn't load
- Filters reset unexpectedly
- Auto-reset doesn't trigger
- Console shows errors
- Toast notifications don't appear
- Old batch_id retained after auto-reset

### 📸 Screenshot Checklist
1. Normal operation (no retries)
2. Offline mode enabled
3. Retry toast notification
4. Retry exhausted error
5. Successful retry recovery
6. Sales Journal initial state
7. Dashboard with filter change
8. Out of Balance filters
9. Sales Journal filter persistence
10. Dashboard proof mode change
11. Sales Journal proof mode propagation
12. Before batch type auto-reset
13. Console auto-reset logs
14. After batch type auto-reset
15. Proof mode auto-reset console
16. Sales Journal before cross-tab test
17. Dashboard cross-tab change
18. Sales Journal cross-tab auto-reset

---

## Testing Tips

1. **Always clear console** before starting each test
2. **Take screenshots immediately** when events occur (retries, auto-resets)
3. **Copy console output** while it's fresh
4. **Note exact values** (batch IDs, filter states)
5. **Test slowly** - allow data to load between actions
6. **Watch the UI** - look for visual feedback (loading spinners, toasts)
7. **Be thorough** - every interactive element should be tested

---

**Ready to begin testing? Start with Feature 1, Test 1.1!**
