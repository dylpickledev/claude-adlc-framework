# Paused Contexts Index

This directory contains saved conversation contexts from `/pause` commands, enabling seamless resumption of work across sessions.

## Active Paused Contexts

*None yet - contexts will appear here when you use `/pause`*

## How to Use

### Pause a Conversation
```bash
/pause
# or
/pause "custom description of what you're working on"
```

### Resume a Conversation
```bash
"Continue from [filename]"
# or
"Resume from where we left off on [topic]"
```

## Context File Format

Each paused context includes:
- **Current task/goal**: What you were working on
- **Progress made**: Accomplishments from the session
- **Decisions made**: Key choices with rationale
- **Next steps**: Where to pick up
- **Blockers/questions**: Issues needing resolution
- **Relevant files**: Paths to discussed/modified files
- **Agent context**: Specialist agents involved
- **Conversation summary**: Key topics and exchanges

## Benefits

✅ **Seamless resumption**: Pick up exactly where you left off
✅ **Context preservation**: All decisions and rationale captured
✅ **Cross-session work**: Support for multi-day projects
✅ **Team handoff**: Share context with collaborators
✅ **Blocker management**: Document what's blocking progress

---

*Paused contexts auto-indexed and sorted by date*
