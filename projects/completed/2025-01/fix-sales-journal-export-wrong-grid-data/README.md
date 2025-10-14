# Fix: Sales Journal Export Buttons Export Wrong Grid Data

**Created**: 2025-10-13/14
**Status**: 🔍 Investigation
**Repository**: graniterock/react-sales-journal
**Issue**: [#36](https://github.com/graniterock/react-sales-journal/issues/36)

## Quick Links
- [Specification](./spec.md) - Problem statement and requirements
- [Context](./context.md) - Current investigation state
- [Tasks](./tasks/) - Investigation findings

## Problem Summary
The export buttons (CSV/Excel/PDF) in the "Detail by Ticket Date" tab are exporting data from the Sales Journal grid instead of the Detail by Ticket grid.

## Current Status
- ✅ Issue created (#36)
- ✅ Root cause identified (hardcoded column extraction)
- ✅ Fix implemented (generic export functions)
- ✅ Build successful
- ✅ PR created (#37)
- 🧪 Awaiting: Manual testing and merge
