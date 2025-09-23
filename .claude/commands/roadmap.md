# /roadmap Command Protocol

## Purpose
Strategic planning and prioritization for ADLC Plan phase completion. Creates impact vs effort analysis with execution-ready roadmaps.

## Usage
```bash
claude /roadmap [timeframe]
# timeframe: quarterly (default), sprint, annual
```

## Protocol

### 1. Execute roadmap.sh Script
```bash
./scripts/roadmap.sh [timeframe]
```

### 2. Strategic Planning Workflow
- **Analyzes organized ideas**: Reviews `ideas/organized/` directory
- **Creates prioritization matrix**: Impact vs effort analysis framework
- **Generates execution plan**: Ready-to-build priorities with sequencing
- **Stakeholder alignment**: Templates for cross-departmental coordination

## Claude Instructions

When user runs `/roadmap [timeframe]`:

1. **Execute the script**: Run `./scripts/roadmap.sh [timeframe]`
2. **Monitor progress**: Display analysis and roadmap creation
3. **Guide completion**: Help user fill prioritization matrix if requested
4. **Suggest next steps**: Identify top priorities for `/build` command

### Response Format
```
🗺️ Creating [timeframe] roadmap...
📊 Analyzing organized ideas...
✅ Roadmap created: ideas/roadmaps/[timeframe]-[date].md

📋 Next steps:
   1. Review and fill in the prioritization matrix
   2. Identify top 2-3 ideas for execution
   3. Build highest priority: ./scripts/build.sh [idea-name]

💡 Tip: Open the roadmap file to complete the prioritization analysis
```

## Integration with ADLC
- **ADLC Plan Phase**: Strategic planning and stakeholder feedback
- **Impact analysis**: Business value vs implementation effort
- **Implementation planning**: Dependencies, sequencing, and resource allocation
- **Cross-layer context**: Links planning directly to development execution

## Prioritization Framework
### Impact vs Effort Matrix
- **High Priority**: High impact, low-medium effort (quick wins + strategic)
- **Medium Priority**: Medium impact, any effort OR high impact, high effort
- **Low Priority**: Low impact, any effort OR parking lot items

### Dependencies & Sequencing
- Technical prerequisites identification
- Cross-system coordination requirements
- Resource availability and timeline constraints

## Examples

### Example 1: Quarterly Planning
```bash
claude /roadmap quarterly
# → Creates comprehensive quarterly execution plan
```

### Example 2: Sprint Planning
```bash
claude /roadmap sprint
# → Creates 2-week focused execution plan
```

### Example 3: Annual Strategic Planning
```bash
claude /roadmap annual
# → Creates long-term strategic roadmap
```

## Success Criteria
- [ ] Roadmap file created with all organized ideas analyzed
- [ ] Prioritization matrix template provided
- [ ] Clear execution plan with sequencing
- [ ] Dependencies and blockers identified
- [ ] Ready for immediate `/build` execution

## Follow-up Actions
After roadmap creation, typically:
1. **Review and prioritize**: Complete the impact vs effort analysis
2. **Select top priorities**: Choose 1-3 ideas for immediate execution
3. **Execute**: Use `/build [idea-name]` for highest priority items

---

*Strategic ADLC Plan phase completion - from organized ideas to execution-ready roadmap.*