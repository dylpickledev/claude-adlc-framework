# Project Work Tracking System

This directory contains the work tracking system for the D&A Agent Hub, designed to manage cross-repository projects and preserve knowledge systematically.

## Directory Structure

```
projects/
├── active/          # Current work projects
│   ├── feature-snowflake-optimization/
│   ├── fix-dbt-test-failures/
│   └── research-tableau-performance/
├── completed/       # Archived completed projects
│   ├── 2025-01/
│   ├── 2025-02/
│   └── ...
└── README.md        # This documentation
```

## Workflow Overview

### 1. Initialize New Work

```bash
./scripts/work-init.sh <type> "<description>"
```

**Types:** `feature`, `fix`, `research`, `refactor`, `docs`

**Example:**
```bash
./scripts/work-init.sh feature "snowflake cost optimization"
```

**This creates:**
- `projects/active/feature-snowflake-cost-optimization/` directory
- **README.md** - Navigation hub with quick links and progress tracking
- **spec.md** - Project specification with requirements and implementation plan  
- **context.md** - Dynamic working context with branches, PRs, and current state
- **tasks/** - Agent coordination directory
- New git branch with matching name
- All files staged and ready for first commit

### 2. Work on Project

- **Commit early and often** - All project work is tracked in git
- **Use the project folder** for all related files, notes, scripts
- **Update README.md** with progress, links, and findings
- **Cross-reference related PRs** in other repositories

### 3. Complete Project

```bash
./scripts/work-complete.sh feature-snowflake-cost-optimization
```

**This process:**
- Reviews project for knowledge dissemination opportunities
- Moves project to `projects/completed/YYYY-MM/`
- Switches back to main branch
- Optionally deletes the work branch

## Project Types

### feature
New functionality, enhancements, or capabilities
- Example: `feature-semantic-layer-integration`

### fix
Bug fixes, error resolution, or corrective measures
- Example: `fix-dbt-compilation-errors`

### research
Investigation, analysis, or exploratory work
- Example: `research-pipeline-performance`

### refactor
Code improvements, reorganization, or technical debt
- Example: `refactor-agent-communication`

### docs
Documentation creation, updates, or improvements
- Example: `docs-onboarding-process`

## Project Folder Contents

**IMPORTANT:** Projects folders are for coordination, NOT code changes. All actual code goes in `repos/`.

### What Goes in `projects/`
- **README.md** - Navigation hub and progress summary
- **spec.md** - Stable project specification and requirements
- **context.md** - Dynamic working context (branches, PRs, blockers)
- **tasks/** - Agent coordination and findings
- **notes/** - Research findings and meeting notes  
- **docs/** - Documentation drafts and requirements
- **config/** - Configuration templates or examples
- **analysis/** - Data analysis, screenshots, test results

### What Goes in `repos/`
- **All actual code changes** - Python, SQL, JavaScript, etc.
- **Repository-specific files** - dbt models, scripts, configs
- **Tests and CI/CD** - Unit tests, integration tests
- **Production deployments** - Anything that ships to users

### Typical Project Flow
```
projects/feature-snowflake-optimization/
├── README.md                      # Navigation hub, progress, decisions
├── spec.md                        # Requirements, success criteria, timeline
├── context.md                     # Current branches, PRs, blockers
├── tasks/
│   ├── current-task.md           # Agent assignments
│   ├── snowflake-findings.md     # Cost analysis research
│   └── dbt-findings.md           # Performance optimization findings
├── notes/performance-analysis.md  # Research findings
└── analysis/query-benchmarks.csv  # Test results

repos/dbt_cloud/
├── models/marts/optimized_sales.sql    # Actual model changes
└── tests/test_performance.py           # Performance tests

repos/snowflake_utils/
└── scripts/cost_monitoring.py          # New monitoring script
```

The `projects/` folder **coordinates** the work across multiple repos and preserves the context.

### Enhanced File Structure Benefits

- **spec.md**: Provides Claude with stable project requirements and clear end goals
- **context.md**: Tracks dynamic state so Claude always knows current project status  
- **README.md**: Serves as navigation hub for quick project overview
- **tasks/**: Enables structured agent coordination and findings preservation

## Knowledge Dissemination

When completing projects, consider extracting learnings to:

### knowledge/
- **business/** - Business context, requirements, stakeholder info
- **technical/** - Technical documentation, how-tos, troubleshooting
- **projects/** - Cross-cutting project learnings

### agents/
- **dbt-expert/knowledge/** - dbt-specific learnings
- **snowflake-expert/knowledge/** - Snowflake optimization insights  
- **tableau-expert/knowledge/** - Dashboard best practices
- **orchestra-expert/knowledge/** - Workflow orchestration patterns
- **dlthub-expert/knowledge/** - Data loading techniques

## Benefits

### Collaboration
- **Full git history** of all work
- **Easy sharing** across team members
- **Branch-based development** for each project

### Knowledge Building
- **Systematic preservation** of learnings
- **Cross-project insights** readily available
- **Agent expertise** grows over time

### Project Management
- **Clear status tracking** (active vs completed)
- **Cross-repository coordination** in one place
- **Full audit trail** of all decisions and changes

## Best Practices

### Getting Started
1. **Always start with work-init.sh** - Creates proper structure
2. **Commit README immediately** - Establishes the project in git
3. **Update objectives early** - Refine the project scope

### During Work
1. **Commit frequently** - Don't lose work or context
2. **Link related PRs** - Track cross-repository dependencies  
3. **Document decisions** - Capture the "why" behind changes
4. **Update progress** - Keep README current

### Completing Work
1. **Review for knowledge extraction** - What should be preserved?
2. **Update permanent documentation** - Extract to knowledge/ or agents/
3. **Link final PRs** - Complete the paper trail
4. **Use work-complete.sh** - Proper archival process

## Commands Quick Reference

```bash
# Start new work
./scripts/work-init.sh feature "description"

# Complete work  
./scripts/work-complete.sh project-name

# List active projects
ls projects/active/

# Review completed projects
ls projects/completed/
```

---

*This system grows with your team - start simple with just README.md files, then add structure as your projects become more complex.*