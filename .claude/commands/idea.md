# /idea Command Protocol

## Purpose
Quick idea capture using GitHub Issues for ADLC Plan phase. The primary command for capturing ideas - replaces `/capture` with clearer, more intuitive naming.

## Usage
```bash
claude /idea "idea description"
```

## Protocol

### 1. Execute idea.sh Script
```bash
./scripts/idea.sh "[idea]"
```

### 2. Automatic GitHub Issue Creation
- **Creates GitHub issue**: Idea stored as issue with appropriate labels
- **Auto-labeling**: Intelligently categorizes ideas (bi-analytics, data-engineering, analytics-engineering, architecture, ui-development)
- **ADLC tracking**: Issues tagged with 'idea' label for roadmap planning
- **Next step guidance**: Clear path to research, roadmap, and start commands

## Claude Instructions

When user runs `/idea [idea]`:

1. **Execute the script**: Run `./scripts/idea.sh "[idea]"`
2. **Monitor output**: Display script progress and GitHub issue creation
3. **Provide guidance**: Show next steps from script output

### Response Format
```
💡 Capturing idea: [idea description]
📋 Detected type: [BI/Analytics|Data Engineering|Analytics Engineering|Architecture|UI Development]

✅ Idea captured as GitHub issue!
🔗 Issue: https://github.com/[org]/[repo]/issues/[number]

💡 Next steps:
   - Deep analysis: /research [number]
   - Add more ideas: /idea "[another idea]"
   - View all ideas: gh issue list --label idea
   - Plan roadmap: /roadmap [quarterly|sprint|annual]
   - Start building: /start [number]
```

## Integration with ADLC
- **ADLC Plan Phase**: Business case validation and implementation planning
- **GitHub Issues integration**: Ideas become trackable, commentable, and linkable
- **Seamless workflow**: Direct path from issue to project via `/start <issue-number>`
- **Team visibility**: All team members can see and prioritize ideas

## GitHub Issue Labels

### Automatic Labeling
- **idea**: All captured ideas (enables filtering)
- **bi-analytics**: Dashboard, visualization, Tableau, Power BI projects
- **data-engineering**: Pipeline, ETL, ingestion, orchestration work
- **analytics-engineering**: dbt models, transformations, SQL work
- **architecture**: Platform, infrastructure, AWS, Snowflake architecture
- **ui-development**: Streamlit, React, frontend applications

## Examples

### Example 1: BI Dashboard Idea
```bash
/idea "Create executive KPI dashboard with real-time metrics"
# → Creates issue with labels: idea, bi-analytics
```

### Example 2: Data Engineering Idea
```bash
/idea "Implement real-time customer data pipeline from Salesforce"
# → Creates issue with labels: idea, data-engineering
```

### Example 3: Architecture Idea
```bash
/idea "Evaluate Snowflake cost optimization strategies"
# → Creates issue with labels: idea, architecture
```

## Workflow Integration

### From Idea to Production
```
/idea → GitHub Issue Created
    ↓
/research [#] → Deep analysis (optional but recommended)
    ↓
/roadmap → Prioritize issues in roadmap planning
    ↓
/start [#] → Create project from prioritized issue
    ↓
Development → Project work with agent coordination
    ↓
/complete → Finish project, close linked issue
```

## When to Use /idea vs /research

| Scenario | Command | Reason |
|----------|---------|--------|
| Quick thought, clear value | `/idea` | Fast capture, obvious benefit |
| Complex idea, needs analysis | `/research` first | Validate before committing |
| Brainstorming session | `/idea` multiple times | Rapid collection |
| Strategic planning | `/idea` then `/roadmap` | Capture then prioritize |

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

*Primary ADLC idea capture command - from thought to trackable GitHub issue in seconds.*
