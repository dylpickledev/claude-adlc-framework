# /idea Command Protocol

## Purpose
Quick idea capture using GitHub Issues for ADLC Plan phase. Creates trackable GitHub issues that connect ideation directly to project execution.

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
- **Creates GitHub issue**: Idea stored as issue with 'idea' label
- **ADLC tracking**: Tagged for roadmap planning
- **Next step guidance**: Clear path to research, roadmap, and start commands

## Claude Instructions

When user runs `/idea [idea]`:

1. **Execute the script**: Run `./scripts/idea.sh "[idea]"`
2. **Monitor output**: Display script progress and GitHub issue creation
3. **Provide guidance**: Show next steps from script output

### Response Format
```
💡 Creating GitHub issue for idea...
📝 Idea: [idea description]

✅ GitHub issue created successfully!
🔗 Issue #[number]: [URL]

🎯 Next steps:
   1. View issue: gh issue view [number]
   2. Deep analysis: /research [number]
   3. Start development: /start [number]

💡 Or use /roadmap to see all ideas and prioritize
```

## Integration with ADLC
- **ADLC Plan Phase**: Business case validation and implementation planning
- **GitHub Issues integration**: Ideas become trackable, commentable, and linkable
- **Seamless workflow**: Direct path from issue to project via `/start <issue-number>`
- **Team visibility**: All team members can see and prioritize ideas

## Examples

### Example 1: BI Dashboard Idea
```bash
claude /idea "Create executive KPI dashboard with real-time metrics"
# → Creates issue #123
```

### Example 2: Data Engineering Idea
```bash
claude /idea "Implement real-time customer data pipeline from Salesforce"
# → Creates issue #124
```

### Example 3: Architecture Idea
```bash
claude /idea "Evaluate Snowflake cost optimization strategies"
# → Creates issue #125
```

## Workflow Integration

### From Idea Capture to Project
```
/idea → GitHub Issue Created (#123)
    ↓
/research 123 → Deep analysis (optional)
    ↓
/roadmap → Prioritize in strategic planning (optional)
    ↓
/start 123 → Create project from issue
    ↓
Development → Project work with agent coordination
    ↓
/complete → Complete project, close linked issue
```

## Success Criteria
- [ ] GitHub issue created successfully
- [ ] 'idea' label applied
- [ ] Issue description includes context
- [ ] Clear next step guidance provided
- [ ] Issue URL returned for reference

## Viewing and Managing Ideas

### List All Ideas
```bash
gh issue list --label idea --state open
```

### Sort by Date
```bash
gh issue list --label idea --sort created --order desc
gh issue list --label idea --sort updated --order desc
```

### Search Ideas
```bash
gh issue list --label idea --search "dashboard"
```

---

*Streamlined ADLC Plan phase implementation - from brainstorm to GitHub-tracked execution plan.*
