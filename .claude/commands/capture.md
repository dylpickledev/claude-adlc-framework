# /capture Command Protocol

⚠️ **DEPRECATED**: This command has been renamed to `/idea` for better semantics. Please use `/idea` instead.

This command still works but will redirect to `/idea`.

---

## Purpose
**Use `/idea` instead - clearer, more intuitive naming.**

Simplified idea capture using GitHub Issues for ADLC Plan phase. Replaces file-based idea management with integrated issue tracking that connects ideation directly to project execution.

## Usage
```bash
claude /capture "idea description"
```

## Protocol

### 1. Execute capture.sh Script
```bash
./scripts/capture.sh "[idea]"
```

### 2. Automatic GitHub Issue Creation
- **Creates GitHub issue**: Idea stored as issue with appropriate labels
- **Auto-labeling**: Intelligently categorizes ideas (bi-analytics, data-engineering, analytics-engineering, architecture, ui-development, general)
- **ADLC tracking**: Issues tagged with 'idea' label for roadmap planning
- **Next step guidance**: Clear path to roadmap and build commands

## Claude Instructions

When user runs `/capture [idea]`:

1. **Execute the script**: Run `./scripts/capture.sh "[idea]"`
2. **Monitor output**: Display script progress and GitHub issue creation
3. **Provide guidance**: Show next steps from script output

### Response Format
```
🧠 Capturing idea: [idea description]
📋 Detected type: [BI/Analytics|Data Engineering|Analytics Engineering|Architecture|UI Development|General]

✅ Idea captured as GitHub issue!
🔗 Issue: https://github.com/[org]/[repo]/issues/[number]

💡 Next steps:
   - Add more ideas: ./scripts/capture.sh "[another idea]"
   - View all ideas: gh issue list --label idea
   - Plan roadmap: ./scripts/roadmap.sh [quarterly|sprint|annual]
   - Build top priority: ./scripts/build.sh <issue-number>
```

## Integration with ADLC
- **ADLC Plan Phase**: Business case validation and implementation planning
- **GitHub Issues integration**: Ideas become trackable, commentable, and linkable
- **Seamless workflow**: Direct path from issue to project via `/build <issue-number>`
- **Team visibility**: All team members can see and prioritize ideas

## GitHub Issue Labels

### Automatic Labeling
- **idea**: All captured ideas (enables filtering)
- **bi-analytics**: Dashboard, visualization, Tableau, Power BI projects
- **data-engineering**: Pipeline, ETL, ingestion, orchestration work
- **analytics-engineering**: dbt models, transformations, SQL work
- **architecture**: Platform, infrastructure, AWS, Snowflake architecture
- **ui-development**: Streamlit, React, frontend applications
- **general**: Ideas not matching specific categories

## Examples

### Example 1: BI Dashboard Idea
```bash
claude /capture "Create executive KPI dashboard with real-time metrics"
# → Creates issue with labels: idea, bi-analytics
```

### Example 2: Data Engineering Idea
```bash
claude /capture "Implement real-time customer data pipeline from Salesforce"
# → Creates issue with labels: idea, data-engineering
```

### Example 3: Architecture Idea
```bash
claude /capture "Evaluate Snowflake cost optimization strategies"
# → Creates issue with labels: idea, architecture
```

## Workflow Integration

### From Idea Capture to Project
```
/capture → GitHub Issue Created
    ↓
/roadmap → Prioritize issues in roadmap planning
    ↓
/build <issue-number> → Create project from prioritized issue
    ↓
Development → Project work with agent coordination
    ↓
/finish → Complete project, close linked issue
```

## Success Criteria
- [ ] GitHub issue created successfully
- [ ] Appropriate labels automatically applied
- [ ] Issue description includes ADLC context
- [ ] Clear next step guidance provided
- [ ] Issue URL returned for reference

## Viewing and Managing Ideas

### List All Ideas
```bash
gh issue list --label idea
```

### Filter by Category
```bash
gh issue list --label idea --label bi-analytics
gh issue list --label idea --label data-engineering
gh issue list --label idea --label architecture
```

### Search Ideas
```bash
gh issue list --label idea --search "dashboard"
gh issue list --label idea --state open
```

---

*Streamlined ADLC Plan phase implementation - from brainstorm to GitHub-tracked execution plan.*
