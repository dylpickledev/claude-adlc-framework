# /capture Command Protocol

## Purpose
Simplified idea capture with intelligent auto-organization. Replaces `/ideate` and manual `/organize` with a single streamlined command that handles the complete ADLC Plan phase.

## Usage
```bash
claude /capture "idea description"
```

## Protocol

### 1. Execute capture.sh Script
```bash
./scripts/capture.sh "[idea]"
```

### 2. Automatic Workflow
- **Rapid capture**: Idea stored in `ideas/inbox/` with timestamp
- **Auto-organization**: When 3+ ideas exist, automatically clusters into themes
- **Next step guidance**: Provides clear roadmap and build options

## Claude Instructions

When user runs `/capture [idea]`:

1. **Execute the script**: Run `./scripts/capture.sh "[idea]"`
2. **Monitor output**: Display script progress and results
3. **Provide guidance**: Show next steps from script output

### Response Format
```
🧠 Capturing idea: [idea description]
📁 Idea saved to: ideas/inbox/[filename]
📊 Auto-organizing ideas (found X ideas in inbox)...
✅ Ideas organized into themes

💡 Next steps:
   - Add more ideas: ./scripts/capture.sh "[another idea]"
   - Plan roadmap: ./scripts/roadmap.sh [quarterly|sprint|annual]
   - Build top priority: ./scripts/build.sh [idea-name]
```

## Integration with ADLC
- **ADLC Plan Phase**: Business case validation and implementation planning
- **Intelligent clustering**: AI-powered organization into strategic themes
- **Seamless workflow**: Direct path to roadmap planning and project execution

## Examples

### Example 1: First Idea
```bash
claude /capture "Implement real-time customer churn prediction model"
```

### Example 2: Auto-Organization Trigger
```bash
claude /capture "Create executive KPI dashboard"
# → Triggers auto-organization when 3+ ideas exist
```

### Example 3: Strategic Planning
```bash
claude /capture "Evaluate Snowflake cost optimization strategies"
```

## Success Criteria
- [ ] Script executes successfully
- [ ] Idea captured with proper timestamp
- [ ] Auto-organization triggers when appropriate
- [ ] Clear next step guidance provided
- [ ] User understands complete workflow

---

*Streamlined ADLC Plan phase implementation - from brainstorm to organized execution plan.*