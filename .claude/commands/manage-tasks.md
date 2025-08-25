---
description: Manage agent task files - archive, purge, or show status
argument-hint: [status|archive|purge|compact] [--dry-run]
---

You are managing the D&A Agent Hub task file system. The agents use isolated directories to prevent conflicts:

**Current Structure:**
```
.claude/tasks/
├── current-task.md              # Shared task description (read-only for agents)
├── business-context/           # Business agent workspace
├── dbt-expert/                # dbt agent workspace  
├── tableau-expert/            # Tableau agent workspace
├── snowflake-expert/          # Snowflake agent workspace
├── orchestra-expert/          # Orchestra agent workspace
├── dlthub-expert/             # dlthub agent workspace
└── archive/                   # Archived task sets
```

**Commands to execute based on arguments:**

**`/manage-tasks status`** - Show current task file status:
- Count files in each agent directory
- Show current-task.md status
- Display archive count

**`/manage-tasks archive`** - Archive all current agent task files:
- Create timestamped tar.gz archive in `archive/` directory
- Remove original files after successful archive
- Preserve current-task.md

**`/manage-tasks purge [--dry-run]`** - Delete all agent task files:
- Remove all .md files from agent directories
- Preserve current-task.md
- Use --dry-run to preview what would be deleted
- Confirm before permanent deletion

**`/manage-tasks compact`** - Archive current tasks and clean old archives:
- Archive current agent task files
- Remove archived files older than 30 days
- Full cleanup operation

**If no arguments provided, default to showing status.**

Execute the requested task management operation. Use the Bash tool to perform file operations. Always preserve `current-task.md` as it contains the shared task context.