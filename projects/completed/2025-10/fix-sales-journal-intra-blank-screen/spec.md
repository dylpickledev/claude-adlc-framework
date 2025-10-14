# Bug Specification: Sales Journal Intra Filter Blank Screen

**Repository**: `graniterock/react-sales-journal`
**Issue**: [#31](https://github.com/graniterock/react-sales-journal/issues/31)
**Environment**: Production - https://apps.grc-ops.com/sales-journal/

## Bug Description
The Sales Journal application displays a blank screen on the "Ticket by Detail" tab when selecting "Intra" from the batch type filter.

## Reproduction Steps
1. Navigate to https://apps.grc-ops.com/sales-journal/
2. Go to "Ticket by Detail" tab
3. Select "Intra" from the batch type filter
4. Observe blank screen (no data, no error message)

## Expected Behavior
Should display ticket detail data filtered by Intra batch type, OR display a user-friendly message if no data exists for this filter

## Actual Behavior
- Completely blank screen
- No data displayed
- No loading indicator
- No error message
- No user feedback

## Investigation Plan

### Phase 1: Reproduce & Diagnose (Browser)
- [ ] Open browser developer console
- [ ] Navigate to Ticket by Detail tab
- [ ] Apply Intra filter
- [ ] Check for JavaScript errors in console
- [ ] Check Network tab for API calls
- [ ] Verify API response (success/failure, data structure)
- [ ] Check React component state in React DevTools

### Phase 2: Code Review (Frontend)
- [ ] Locate "Ticket by Detail" component
- [ ] Review filter logic for batch type
- [ ] Check data fetching logic
- [ ] Review error handling
- [ ] Check empty state handling
- [ ] Verify conditional rendering logic

### Phase 3: Backend Investigation
- [ ] Check FastAPI endpoint for ticket details
- [ ] Verify SQL query for Intra batch type
- [ ] Test query directly in database
- [ ] Check for data existence
- [ ] Review API error handling

### Phase 4: Root Cause Analysis
Determine which scenario:
- **Scenario A**: No data exists for Intra batch type (expected, needs empty state UI)
- **Scenario B**: Data exists but API query fails (bug in backend)
- **Scenario C**: API returns data but React component fails to render (bug in frontend)
- **Scenario D**: JavaScript error crashes component (error handling bug)

## Possible Root Causes
1. **Empty data + missing empty state**: Query returns empty array, component doesn't handle gracefully
2. **API error + missing error UI**: Backend throws error, frontend doesn't catch/display
3. **React render error**: Component crashes on specific data shape from Intra filter
4. **Filter logic bug**: Filter value not properly passed to API
5. **Data type mismatch**: Intra batch type value doesn't match database values

## Success Criteria
- [ ] Root cause identified and documented
- [ ] Fix implemented (either proper error handling OR empty state UI OR data fix)
- [ ] Intra filter either displays data OR shows user-friendly "no data" message
- [ ] No blank screens under any filter condition
- [ ] User receives clear feedback about data availability
- [ ] Fix tested in production environment
- [ ] Issue #31 closed with solution documented

## Related Files (To Investigate)
- Frontend: `/src/components/TicketByDetail.tsx` (or similar)
- Frontend: API client / data fetching logic
- Backend: FastAPI route for ticket details
- Backend: SQL query building for filters
