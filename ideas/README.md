# Ideas Management - Migrated to GitHub Issues

## Migration Notice

**As of October 2025**, the DA Agent Hub idea management system has migrated from file-based storage to **GitHub Issues** for improved team collaboration and tracking.

## New Workflow

### Capture Ideas
```bash
./scripts/capture.sh "Your idea description"
```
Creates a GitHub issue with appropriate labels automatically.

### View All Ideas
```bash
gh issue list --label idea --state open
```

### Filter by Category
```bash
gh issue list --label idea --label bi-analytics
gh issue list --label idea --label data-engineering
gh issue list --label idea --label architecture
```

### Plan Roadmap
```bash
./scripts/roadmap.sh quarterly
```
Analyzes all GitHub issues with 'idea' label and creates prioritization framework.

### Build Project from Idea
```bash
./scripts/build.sh <issue-number>
```
Creates full project structure from GitHub issue, links issue to project, and adds 'in-progress' label.

### Complete Project
```bash
./scripts/finish.sh <project-name>
```
Archives project and automatically closes linked GitHub issue.

## Benefits of GitHub Issues

- **Team Visibility**: All team members can see and comment on ideas
- **Better Tracking**: Labels, milestones, and assignees for organization
- **Integration**: Links directly between issues and projects
- **Search**: Full-text search across all ideas
- **History**: Complete audit trail of idea evolution
- **Notifications**: Team members get notified of updates

## Labels

### Core Label
- **idea**: All captured ideas (required for ADLC workflow)

### Category Labels
- **bi-analytics**: Dashboard, visualization, Tableau, Power BI projects
- **data-engineering**: Pipeline, ETL, ingestion, orchestration work
- **analytics-engineering**: dbt models, transformations, SQL work
- **architecture**: Platform, infrastructure, AWS, Snowflake architecture
- **ui-development**: Streamlit, React, frontend applications
- **general**: Ideas not matching specific categories

### Status Label
- **in-progress**: Ideas currently being built as projects

## Legacy File Structure

This directory structure is maintained for reference only:

- **inbox/**: Historical ideas (migrated to issues)
- **organized/**: Historical categorized ideas (migrated to issues)
- **pipeline/**: Historical ready-to-build ideas (migrated to issues)
- **archive/**: Completed projects (will remain for historical reference)
- **templates/**: Documentation templates (still in use)

## Migration Strategy

Existing file-based ideas have been converted to GitHub issues with appropriate labels. The file-based system is deprecated and no new ideas should be added to the file structure.

## Questions?

See the complete ADLC workflow documentation in `CLAUDE.md` or run:
```bash
claude /help
```

---

*Part of the Analytics Development Lifecycle (ADLC) - Plan Phase Enhancement*
