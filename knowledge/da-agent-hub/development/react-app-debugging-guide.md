# React Application Debugging Guide

## Overview
This guide documents the systematic approach to debugging React applications showing blank screens, based on real-world troubleshooting of the GraniteRock Sales Journal application.

## Common React Blank Screen Issues

### Issue 1: Module-Level Side Effects
**Symptom**: Blank white screen, no error in console initially
**Root Cause**: Synchronous code execution during module import that blocks rendering

**Example Problem**:
```typescript
// ❌ BAD: Module-level initialization in store file
// src/store/financialStore.ts (bottom of file)
useFinancialStore.getState().loadFilterOptions();
useFinancialStore.getState().loadJournalData();
useFinancialStore.getState().loadOutOfBalanceData();
```

**Why It Fails**:
- Code executes **synchronously** when module is imported
- If async functions fail (network errors, missing backend), they can block React mounting
- Module load happens **before** React even starts rendering
- Error handling in async functions may not catch module-level execution issues

**Solution**:
```typescript
// ✅ GOOD: Let React components handle initialization
// Remove module-level calls, use useEffect in components
// App.tsx already has proper initialization:
useEffect(() => {
  const initializeApp = async () => {
    try {
      await refreshAllData();
      setIsInitializing(false);
    } catch (error) {
      console.error('Failed to initialize:', error);
      setHasError(true);
    }
  };
  initializeApp();
}, [refreshAllData]);
```

**Diagnostic Steps**:
1. Check bottom of store files for immediate function calls
2. Look for module-level code that runs on import
3. Verify initialization happens in React component lifecycle

---

### Issue 2: Vite Environment Variables
**Symptom**: `Uncaught ReferenceError: process is not defined`
**Root Cause**: Using Node.js `process.env` in browser context

**Example Problem**:
```typescript
// ❌ BAD: Node.js environment variable access
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';
if (process.env.NODE_ENV === 'development') {
  // mock setup
}
```

**Why It Fails**:
- `process` is a Node.js global variable
- Browser doesn't have `process` object
- Vite uses different environment variable system

**Solution**:
```typescript
// ✅ GOOD: Vite environment variable access
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
if (import.meta.env.DEV) {
  // mock setup
}
```

**Vite Environment Variable Mapping**:
| Create React App | Vite |
|-----------------|------|
| `process.env.NODE_ENV` | `import.meta.env.MODE` |
| `process.env.NODE_ENV === 'development'` | `import.meta.env.DEV` |
| `process.env.NODE_ENV === 'production'` | `import.meta.env.PROD` |
| `process.env.REACT_APP_*` | `import.meta.env.VITE_*` |

**TypeScript Support**:
Create `src/vite-env.d.ts`:
```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string
  readonly DEV: boolean
  readonly PROD: boolean
  readonly MODE: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

**Diagnostic Steps**:
1. Search codebase: `grep -r "process\.env" src/`
2. Check browser console for "process is not defined"
3. Replace all `process.env` with `import.meta.env`

---

### Issue 3: Python vs JavaScript Method Names
**Symptom**: `TypeError: ... .upper is not a function`
**Root Cause**: Using Python method names in JavaScript

**Example Problem**:
```typescript
// ❌ BAD: Python method syntax
const status = pipelineStatus?.runStatus?.upper() || '';
```

**Why It Fails**:
- Python uses `str.upper()`, JavaScript uses `String.toUpperCase()`
- Common when porting code from Python (Flask, Django) to JavaScript/React
- Easy to miss during initial development

**Solution**:
```typescript
// ✅ GOOD: JavaScript method syntax
const status = pipelineStatus?.runStatus?.toUpperCase() || '';
```

**Common Python → JavaScript Method Mappings**:
| Python | JavaScript |
|--------|-----------|
| `.upper()` | `.toUpperCase()` |
| `.lower()` | `.toLowerCase()` |
| `.strip()` | `.trim()` |
| `.split()` | `.split()` ✅ (same) |
| `.join()` | `.join()` ✅ (same) |
| `.append()` | `.push()` |
| `.extend()` | `.concat()` or `[...arr1, ...arr2]` |

**Diagnostic Steps**:
1. Look for `.upper()` or `.lower()` in TypeScript/JavaScript files
2. Check for other Python-style method calls
3. Search: `grep -r "\.upper()" src/` and `grep -r "\.lower()" src/`

---

## Systematic Debugging Process

### Phase 1: Verify Development Server
```bash
# Check if Vite is running
lsof -ti:5173  # or whatever port

# Check server logs
tail -f /tmp/vite-server.log

# Verify HTML is served
curl -s http://localhost:5173/ | grep "root"
```

**Expected**: HTML loads with `<div id="root"></div>` and script tags

---

### Phase 2: Browser Console Investigation
**Critical**: You MUST check the browser console - it contains the actual error!

**How to Access Console**:
```bash
# Open Chrome with developer tools
osascript << 'EOF'
tell application "Google Chrome"
    activate
    open location "http://localhost:5173/"
    delay 2
end tell

tell application "System Events"
    tell process "Google Chrome"
        keystroke "j" using {command down, option down}
        delay 1
    end tell
end tell
EOF
```

**Common Console Errors**:
1. **`process is not defined`** → Environment variable issue
2. **`... is not a function`** → Method name error (Python vs JS)
3. **`Cannot read property of undefined`** → Missing data/initialization
4. **Network errors** → API calls failing
5. **Module not found** → Import path issues

---

### Phase 3: Check Module Loading
```bash
# Test if main entry point compiles
curl -s http://localhost:5173/src/main.tsx | head -20

# Test if App component compiles
curl -s http://localhost:5173/src/App.tsx | head -30

# Check for import errors in console
# Look for 404s in Network tab
```

---

### Phase 4: Identify Root Cause Category

**Blank Screen Categories**:

1. **Compilation/Build Errors**
   - Check Vite terminal output
   - Run `npm run build` to see all errors
   - TypeScript errors usually show in IDE

2. **Runtime Errors**
   - **Always in browser console**
   - Check console immediately - don't assume
   - Errors might be in specific component files

3. **Module Loading Issues**
   - Check Network tab in DevTools
   - Look for 404s or failed module loads
   - Verify import paths are correct

4. **State/Data Issues**
   - App loads but shows blank content
   - Check if data fetch errors are suppressed
   - Verify error boundaries are working

---

## Testing React Apps: Roy Kent Standards

### "It Loads" Is NOT Testing
When testing React applications, follow these comprehensive steps:

#### 1. Visual Verification
- [ ] App renders visible content (not blank screen)
- [ ] Navigation elements appear
- [ ] Loading states show appropriately
- [ ] Error states display when needed

#### 2. Console Verification
- [ ] **ALWAYS CHECK CONSOLE FIRST**
- [ ] No red errors in console
- [ ] Warnings are acceptable (document them)
- [ ] Network tab shows successful module loads

#### 3. Interaction Testing
- [ ] Click navigation items
- [ ] Test form inputs if present
- [ ] Verify data loads (even if mock data)
- [ ] Check responsive behavior

#### 4. Screenshot Documentation
Capture evidence of testing:
```bash
# Capture browser window
screencapture -x -o /tmp/app-working.png

# Capture specific window
screencapture -l$(osascript -e 'tell app "Google Chrome" to id of window 1') /tmp/chrome.png
```

---

## Quick Reference: React Blank Screen Checklist

When encountering a blank screen in a React app:

```bash
# 1. Check if dev server is running
lsof -ti:5173  # or current port

# 2. Check HTML loads
curl -s http://localhost:5173/ | grep root

# 3. Open browser console (MOST IMPORTANT)
open -a "Google Chrome" "http://localhost:5173/"
# Cmd+Option+J to open console

# 4. Check for common issues
cd /path/to/react-app
grep -r "process\.env" src/                    # Environment variables
grep -r "\.upper()\|\.lower()" src/            # Python method names
grep -r "useStore.getState()" src/**/*.ts      # Module-level store calls
```

**Priority Order**:
1. ✅ **Browser console errors** (always check first)
2. ✅ Vite server logs
3. ✅ Network tab (module loading)
4. ✅ React DevTools (component tree)

---

## Common Pitfalls to Avoid

### ❌ Don't Assume - Verify
- Don't assume "no console errors" - **check the console**
- Don't assume HTML loads - verify with curl
- Don't assume modules load - check Network tab

### ❌ Don't Skip Error Messages
- Read the full error message and stack trace
- Error messages usually tell you the exact file and line
- Stack traces show the execution path

### ❌ Don't Ignore Warnings
- Warnings can indicate future errors
- Document warnings in testing notes
- Vite warnings about duplicate attributes are usually non-blocking

### ❌ Don't Test in Isolation
- Check both dev and production builds
- Test in multiple browsers if possible
- Verify on different screen sizes

---

## Tools and Commands Reference

### Browser Automation (macOS)
```bash
# Open Chrome with URL
open -a "Google Chrome" "http://localhost:5173/"

# Activate Chrome and open console
osascript -e 'tell application "Google Chrome" to activate'
osascript -e 'tell application "System Events" to keystroke "j" using {command down, option down}'

# Hard refresh (clear cache)
osascript -e 'tell application "System Events" to keystroke "r" using {command down, shift down}'

# Capture Chrome window
screencapture -x -o /tmp/screenshot.png
```

### Vite Development Server
```bash
# Start dev server
npm run dev

# Start with specific port
npm run dev -- --port 5173

# Check which port is in use
lsof -ti:5173

# Kill process on port
pkill -f "vite.*5173"

# View server logs
tail -f /tmp/vite-server.log
```

### Debugging Commands
```bash
# Find all process.env usage
grep -rn "process\.env" src/

# Find Python method names
grep -rn "\.upper()\|\.lower()" src/

# Check for module-level side effects in stores
grep -rn "getState()" src/store/

# List all TypeScript errors
npx tsc --noEmit

# Build production to see all errors
npm run build
```

---

## React + Vite Best Practices

### 1. Environment Variables
- Always use `import.meta.env` in Vite projects
- Prefix custom variables with `VITE_`
- Create `vite-env.d.ts` for TypeScript support

### 2. Store Initialization
- Never call async functions at module level
- Use React component lifecycle (useEffect) for initialization
- Handle errors gracefully in initialization code

### 3. Error Boundaries
- Implement error boundaries for production
- Show user-friendly error messages
- Log errors for debugging

### 4. Development vs Production
- Test in both development and production builds
- Mock API responses for development
- Handle missing backend gracefully

---

## Testing Workflow for Future React Apps

### Initial Setup Testing
1. Clone repository
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`
4. **OPEN BROWSER CONSOLE IMMEDIATELY**
5. Navigate to localhost URL
6. Check console for errors
7. Document any warnings
8. Take screenshots of working app

### Issue Troubleshooting Workflow
1. **Check browser console first** (always!)
2. Check Vite server logs
3. Check Network tab for failed loads
4. Search codebase for common issues:
   - `process.env` usage
   - Python method names
   - Module-level side effects
5. Fix issues one at a time
6. Verify each fix in browser
7. Document the fix

### Completion Criteria
- [ ] App renders content (not blank)
- [ ] No errors in browser console
- [ ] All navigation works
- [ ] Mock data loads if backend unavailable
- [ ] Screenshots captured showing working app
- [ ] All fixes documented

---

## Lessons Learned

### Key Takeaways from GraniteRock Sales Journal Debugging

1. **Browser console is the source of truth**
   - The actual error was hidden until console was checked
   - Console showed exact file and line number
   - Stack trace revealed the execution path

2. **Multiple issues can stack**
   - Module-level initialization (Issue #1)
   - Environment variables (Issue #2)
   - Method name error (Issue #3)
   - All needed fixing before app would render

3. **HMR doesn't always catch everything**
   - Some issues require full server restart
   - Clear browser cache for environment changes
   - Hard refresh (Cmd+Shift+R) when in doubt

4. **Vite != Create React App**
   - Different environment variable system
   - Different build configuration
   - Migration requires careful conversion

5. **Test incrementally**
   - Fix one issue at a time
   - Verify in browser after each fix
   - Don't assume HMR reloaded properly

---

## Quick Command Reference Sheet

```bash
# START TESTING A REACT APP

# 1. Setup
cd /path/to/react-app
npm install
npm run dev

# 2. Open browser with console
open -a "Google Chrome" "http://localhost:[PORT]/"
# Then: Cmd+Option+J

# 3. Check for common issues
grep -r "process\.env" src/
grep -r "\.upper()\|\.lower()" src/
grep -r "getState()" src/store/

# 4. Fix environment variables
# Replace: process.env.REACT_APP_* with import.meta.env.VITE_*
# Replace: process.env.NODE_ENV with import.meta.env.MODE or import.meta.env.DEV

# 5. Create TypeScript types
cat > src/vite-env.d.ts << 'EOF'
/// <reference types="vite/client" />
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string
  readonly DEV: boolean
  readonly PROD: boolean
  readonly MODE: string
}
interface ImportMeta {
  readonly env: ImportMetaEnv
}
EOF

# 6. Verify fixes
# Check console - no errors
# Take screenshot
# Document findings
```

---

## Related Documentation

- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [React Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
- [Chrome DevTools Console](https://developer.chrome.com/docs/devtools/console/)
- [Zustand State Management](https://docs.pmnd.rs/zustand/getting-started/introduction)

---

## Continuous Improvement

This guide should be updated when:
- New React blank screen issues are discovered
- New diagnostic techniques are developed
- New tools become available
- Better testing approaches are found

**Last Updated**: 2025-09-29 (GraniteRock Sales Journal debugging session)