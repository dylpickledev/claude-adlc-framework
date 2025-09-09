# Sub-Agent Project Handoff Template

This template guides how parent agents should communicate project requirements to sub-agents within the spec-driven development framework.

## Handoff Process

### 1. Create Project Task Assignment
When assigning a sub-agent to work on a spec-driven project, create a task file in the project directory:

**File**: `projects/[project-num]-[name]/tasks/current-task.md`

```markdown
# Task Assignment: [SUB-AGENT-NAME]

**Project**: [Project Name]  
**Branch**: [branch-name]  
**Assigned Agent**: [sub-agent-name]  
**Task Phase**: [Specification/Planning/Implementation/Testing]  
**Priority**: [High/Medium/Low]  
**Due Date**: [if applicable]  

## Context Documents
- **Specification**: `projects/[project-num]-[name]/spec.md`
- **Implementation Plan**: `projects/[project-num]-[name]/plan.md` (if available)
- **Task List**: `projects/[project-num]-[name]/tasks.md` (if available)

## Your Specific Assignment
[Detailed description of what the sub-agent should do]

### Success Criteria
- [Specific deliverable 1]
- [Specific deliverable 2]
- [Integration requirement with other tools]

### Expected Output
Create your findings in: `projects/[project-num]-[name]/findings/[tool]-findings.md`

Include:
1. **Analysis Summary**: Key findings and recommendations
2. **Implementation Details**: Specific configurations, code, scripts
3. **Integration Points**: How your work connects to other tools
4. **Testing Strategy**: How to validate your recommendations
5. **Risks and Dependencies**: Issues that need attention
6. **Next Steps**: What the parent agent should do next

## Cross-Tool Integration Points
[Map out how this work relates to other sub-agents and tools]

### Dependencies
- **Depends on**: [What needs to be completed first]
- **Enables**: [What other work can start after this]

### Communication Requirements
- **Coordinate with**: [Other sub-agents working on this project]
- **Handoff to**: [Next agent in the workflow]

---
*Created*: [timestamp]  
*Parent Agent*: [parent agent identifier]
```

### 2. Sub-Agent Task Execution

Sub-agents should follow this pattern:

1. **Read Project Context**:
   - Load and analyze project specification
   - Review implementation plan (if available)
   - Understand business requirements and technical constraints

2. **Execute Research and Analysis**:
   - Apply tool-specific expertise to the requirements
   - Research current state and technical feasibility
   - Design implementation approach

3. **Document Findings**:
   - Create comprehensive findings document
   - Include specific implementation details
   - Flag integration requirements and dependencies

4. **Update Task Status**:
   - Mark task as completed in current-task.md
   - Include summary of deliverables
   - Flag any blockers or issues for parent agent

### 3. Parent Agent Integration

After sub-agent completes work:

1. **Review Findings**: Read and analyze sub-agent recommendations
2. **Cross-Validate**: Check integration points with other sub-agent findings  
3. **Execute Implementation**: Use sub-agent specifications to implement solution
4. **Validate Results**: Test implementation against business requirements

## Communication Templates

### Task Assignment Template
Use this when assigning work to a sub-agent via the Task tool:

```
Please work on [project-name]. Your specific assignment is to [detailed task description].

Context:
- Project specification: projects/[num]-[name]/spec.md
- Current phase: [Specification/Planning/Implementation]
- Integration requirements: [list other tools involved]

Expected deliverables:
1. [specific output 1]
2. [specific output 2]

Create your detailed findings in: projects/[num]-[name]/findings/[tool]-findings.md

Focus on [tool-specific requirements] and ensure your recommendations integrate properly with [other tools in stack].
```

### Findings Template for Sub-Agents
```markdown
# [TOOL] Analysis: [Project Name]

**Analyst**: [Tool Expert Name]  
**Date**: [Date]  
**Project**: [Project Specification Location]  

## Executive Summary
[2-3 sentences summarizing key findings and approach]

## Business Requirements Analysis
[How you interpreted the business requirements for your tool]

## Technical Analysis
### Current State Assessment
[What you discovered about existing systems/data]

### Recommended Implementation  
[Specific tool implementation strategy with details]

### Configuration Details
[Exact configs, code snippets, settings needed]

## Integration Specifications
### Input Requirements
[What you need from other tools/systems]

### Output Specifications  
[What you'll provide to downstream tools]

### Handoff Points
[Specific coordination needed with other sub-agents]

## Implementation Tasks
### Phase 1: Setup and Foundation
- [Specific task 1]
- [Specific task 2]

### Phase 2: Core Development
- [Specific task 3]
- [Specific task 4]

### Phase 3: Testing and Integration
- [Specific task 5]
- [Specific task 6]

## Quality Assurance
### Testing Strategy
[How to validate this implementation]

### Success Metrics
[How to measure if this is working correctly]

## Risks and Dependencies
### Blockers
[Anything preventing implementation]

### Dependencies
[What needs to happen before/after this work]

### Assumptions
[Key assumptions made in this analysis]

## Next Steps for Parent Agent
1. [Specific action 1]
2. [Specific action 2]
3. [When to involve other sub-agents]

---
**Status**: [Complete/Pending/Blocked]  
**Ready for Implementation**: [Yes/No]  
**Follow-up Required**: [Yes/No - with details]
```

## Quality Gates

### Before Sub-Agent Assignment
- [ ] Project specification is complete and clear
- [ ] Business requirements are well-defined
- [ ] Technical constraints are documented
- [ ] Success criteria are measurable

### Sub-Agent Deliverable Review
- [ ] Findings document is complete and detailed
- [ ] Implementation approach is technically sound  
- [ ] Integration points are clearly specified
- [ ] Testing strategy is comprehensive
- [ ] Dependencies and risks are identified

### Integration Validation
- [ ] Sub-agent recommendations are consistent across tools
- [ ] Integration points are technically feasible
- [ ] Business requirements are fully addressed
- [ ] Implementation plan is executable

This handoff template ensures clear communication and successful coordination between parent agents and sub-agents in the spec-driven development framework.