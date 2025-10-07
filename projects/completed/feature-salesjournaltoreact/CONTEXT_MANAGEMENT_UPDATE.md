# Context Management System Update

**Date:** 2025-09-30
**Purpose:** Clarify file source tracking and sandbox principles for all Claude sessions

## What Changed

The project context management system has been updated to prevent confusion about which files to analyze and where to write changes.

## Key Principle: Sandbox Isolation 🏖️

**All work stays in `projects/active/feature-salesjournaltoreact/` until explicit deployment request.**

This project folder is an **isolated sandbox** for development.

## File Source Indicators

Claude will now use visual indicators to clarify which files are being referenced:

- **📁 PROJECT SANDBOX**: Working files in project folder (modify freely)
- **📦 REPO**: Source repository files (read-only reference)
- **🎯 DEPLOY**: Deployment target locations (only on explicit request)

## Updated context.md Structure

The `context.md` file now has a clear "File Sources & Working Versions" section that explicitly declares:

### Primary Working Files 📁 (Project Sandbox)
- `📁 working/working_mostly_9_25.py` - Authoritative Streamlit source (4775 lines)
- `📁 STREAMLIT_REFERENCE.md` - Complete analysis documentation
- React code in `/Users/TehFiestyGoat/da-agent-hub/react-sales-journal/` (separate sandbox)

### Reference Files 📦 (Read-Only)
- `📦 repos/front_end/streamlit_apps_snowflake/Apex Sales Journal/streamlit_app.py` - Outdated version (DO NOT USE)

### Deployment Targets 🎯
- Production repos (ONLY on explicit "deploy to production" command)

## Workflow Signals

You can direct Claude's context using these commands:

| Your Command | Claude Action |
|--------------|---------------|
| "Use the project version" | Work with sandbox files only |
| "Check the repo" | Read production (read-only) |
| "Deploy to [repo]" | Move from sandbox → production |
| "Compare project vs repo" | Side-by-side analysis |

## Context Declaration Protocol

Claude will proactively declare context at key decision points:

```
📍 Context Check:
- Working File: 📁 PROJECT working/working_mostly_9_25.py
- Reference: 📦 REPO streamlit_apps_snowflake/streamlit_app.py
- Deploy Target: 🎯 DEPLOY production-repo/

If you want different sources, please redirect me.
```

## What This Prevents

1. **Analyzing wrong file versions** - Clear indicators show which file is being used
2. **Accidental production writes** - Sandbox principle keeps changes isolated
3. **Context confusion** - Explicit declarations ensure shared understanding
4. **Lost work** - All development stays in project folder until ready

## For Your Current Session

If you're mid-work and not experiencing context confusion, you can continue as-is. The updated rules will help if you encounter any file source ambiguity.

**Key reminder**: All changes should go to project sandbox files unless explicitly asked to deploy to production.

## React Development Coordination

The React app at `/Users/TehFiestyGoat/da-agent-hub/react-sales-journal/` is also a sandbox:
- All React code changes stay in that development repo
- Never push to production without explicit request
- Use `📁 working/working_mostly_9_25.py` as source of truth for features

---

**Bottom Line**: If you're making code changes, they go in the project sandbox. If you're deploying to production, user will explicitly ask for it.
