# Claude Memory System

## Overview
Persistent knowledge storage for Claude Code sessions. Since each Claude session is independent, this file-based memory system preserves learnings across sessions.

## Directory Structure

### `/patterns/`
Reusable solutions and proven patterns discovered during development:
- **dbt-patterns.md** - SQL transformations, model architectures
- **react-patterns.md** - Component structures, state management
- **error-fixes.md** - Common errors and their solutions
- **integration-patterns.md** - Cross-system coordination strategies

### `/recent/`
Rolling 30-day knowledge extraction from completed projects:
- Monthly files (e.g., `2025-09.md`) containing patterns, solutions, and fixes
- Auto-populated by `/complete` command
- Reviewed at session start for recent context

### `/templates/`
Branch-type specific starting templates:
- **investigate-template.md** - Investigation branch starter
- **build-template.md** - Building project starter
- **fix-template.md** - Bug fix branch starter

## Pattern Markers

When documenting findings in `.claude/tasks/*/findings.md`, use these markers for automatic extraction:

```markdown
PATTERN: [Description of reusable pattern]
SOLUTION: [Specific solution that worked]
ERROR-FIX: [Error message] -> [Fix that resolved it]
ARCHITECTURE: [System design pattern]
INTEGRATION: [Cross-system coordination approach]
```

## Usage

### At Session Start
Claude should check:
1. `/recent/` for patterns from last 30 days
2. `/patterns/` for relevant domain patterns
3. `/templates/` for branch-type templates

### During Work
- Document findings with pattern markers
- Reference existing patterns before investigation
- Note novel solutions for extraction

### At Project Completion
The `/complete` command automatically:
1. Extracts marked patterns from task findings
2. Updates recent/ with new discoveries
3. Promotes high-value patterns to patterns/
4. Cleans up task findings after extraction

## Maintenance

- **Monthly**: Review recent/ files and promote valuable patterns
- **Quarterly**: Consolidate and organize patterns/ directory
- **Annually**: Archive old patterns that are no longer relevant