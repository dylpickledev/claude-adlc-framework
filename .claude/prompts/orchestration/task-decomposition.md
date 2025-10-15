# Task Decomposition Template

## Purpose
Systematically break down complex tasks into executable subtasks for multi-specialist coordination.

## When to Use
- Complex problems spanning multiple domains
- Tasks where subtasks can't be predicted upfront
- Novel situations without established patterns
- Multi-system investigations or implementations

## Template

```markdown
## TASK DECOMPOSITION

### Original Task
{{TASK_DESCRIPTION}}

### Complexity Assessment

**Why This Requires Decomposition**:
- [ ] Spans multiple domains ({{DOMAIN_LIST}})
- [ ] Subtasks unpredictable without investigation
- [ ] No single specialist owns entire problem
- [ ] Novel situation without established pattern
- [ ] High complexity requiring coordination

**Decomposition Approach**: {{APPROACH}} (e.g., by domain, by phase, by system)

### Subtask Breakdown

**Subtask 1: {{SUBTASK_NAME}}**
- **Description**: {{WHAT_NEEDS_DOING}}
- **Required Expertise**: {{DOMAIN/SPECIALIST}}
- **Expected Output**: {{DELIVERABLE}}
- **Success Criteria**: {{HOW_TO_VALIDATE}}
- **Dependencies**: {{NONE_OR_DEPENDS_ON}}
- **Estimated Effort**: {{TIME_ESTIMATE}}
- **Priority**: {{HIGH/MEDIUM/LOW}}

**Subtask 2: {{SUBTASK_NAME}}**
- **Description**: {{WHAT_NEEDS_DOING}}
- **Required Expertise**: {{DOMAIN/SPECIALIST}}
- **Expected Output**: {{DELIVERABLE}}
- **Success Criteria**: {{HOW_TO_VALIDATE}}
- **Dependencies**: {{NONE_OR_DEPENDS_ON}}
- **Estimated Effort**: {{TIME_ESTIMATE}}
- **Priority**: {{HIGH/MEDIUM/LOW}}

[... continue for all subtasks ...]

### Execution Phases

**Phase 1 - {{PHASE_NAME}}** (Parallel/Sequential):
- Subtask X
- Subtask Y
- Subtask Z
- **Completion Criteria**: {{WHAT_MARKS_PHASE_COMPLETE}}

**Phase 2 - {{PHASE_NAME}}** (Parallel/Sequential):
- Subtask A (requires Phase 1 completion)
- Subtask B (requires Phase 1 completion)
- **Completion Criteria**: {{WHAT_MARKS_PHASE_COMPLETE}}

### Integration Strategy

**How Subtask Outputs Combine**:
{{DESCRIBE_SYNTHESIS_APPROACH}}

**Quality Gates**:
- [ ] {{VALIDATION_CHECKPOINT_1}}
- [ ] {{VALIDATION_CHECKPOINT_2}}
- [ ] {{VALIDATION_CHECKPOINT_3}}

### Overall Success Criteria

**Task Complete When**:
- [ ] All subtasks completed successfully
- [ ] Outputs integrated and validated
- [ ] Original task fully addressed
- [ ] Quality threshold met (8.5/10)
```

## Example Usage

### Original Task
"Production dashboard performance degraded significantly, users reporting 30+ second load times, unclear cause"

### Complexity Assessment

**Why This Requires Decomposition**:
- [x] Spans multiple domains (BI, data warehouse, transformations, infrastructure)
- [x] Subtasks unpredictable without investigation (unknown root cause)
- [x] No single specialist owns entire problem
- [ ] Novel situation without established pattern
- [x] High complexity requiring coordination

**Decomposition Approach**: By system layer (presentation → query → data → infrastructure)

### Subtask Breakdown

**Subtask 1: Tableau Dashboard Analysis**
- **Description**: Analyze dashboard configuration, filters, calculated fields for performance issues
- **Required Expertise**: tableau-expert
- **Expected Output**: List of dashboard-level performance issues with severity ratings
- **Success Criteria**: Identified all Tableau-specific bottlenecks
- **Dependencies**: None (can run immediately)
- **Estimated Effort**: 15 minutes
- **Priority**: HIGH

**Subtask 2: Snowflake Query Performance**
- **Description**: Examine query execution plans, warehouse sizing, query patterns
- **Required Expertise**: snowflake-expert
- **Expected Output**: Query performance analysis with optimization recommendations
- **Success Criteria**: Identified warehouse/query issues with evidence
- **Dependencies**: None (can run immediately)
- **Estimated Effort**: 20 minutes
- **Priority**: HIGH

**Subtask 3: dbt Model Efficiency**
- **Description**: Review dbt model logic, materialization strategy, incremental patterns
- **Required Expertise**: dbt-expert
- **Expected Output**: dbt transformation efficiency analysis
- **Success Criteria**: Identified transformation bottlenecks
- **Dependencies**: None (can run immediately)
- **Estimated Effort**: 15 minutes
- **Priority**: HIGH

**Subtask 4: AWS Infrastructure Health**
- **Description**: Check ECS task health, ALB performance, network latency
- **Required Expertise**: aws-expert
- **Expected Output**: Infrastructure health report
- **Success Criteria**: Confirmed infrastructure is/isn't contributing factor
- **Dependencies**: None (can run immediately)
- **Estimated Effort**: 10 minutes
- **Priority**: MEDIUM

**Subtask 5: Recent Changes Analysis**
- **Description**: Identify recent deployments, config changes, data volume changes
- **Required Expertise**: github-sleuth-expert
- **Expected Output**: Timeline of recent changes correlated with performance degradation
- **Success Criteria**: Identified what changed and when
- **Dependencies**: None (can run immediately)
- **Estimated Effort**: 10 minutes
- **Priority**: MEDIUM

### Execution Phases

**Phase 1 - Parallel Investigation** (Parallel):
- Subtask 1 (tableau-expert)
- Subtask 2 (snowflake-expert)
- Subtask 3 (dbt-expert)
- Subtask 4 (aws-expert)
- Subtask 5 (github-sleuth-expert)
- **Completion Criteria**: All 5 specialists have submitted findings

**Phase 2 - Root Cause Synthesis** (Sequential):
- Orchestrator combines all findings
- Cross-references timing, severity, evidence
- Identifies definitive root cause
- **Completion Criteria**: Root cause identified with high confidence

**Phase 3 - Fix Implementation** (Sequential):
- Appropriate specialist implements fix based on root cause
- Validate fix resolves issue
- **Completion Criteria**: Dashboard performance restored to acceptable levels (<5s load time)

### Integration Strategy

**How Subtask Outputs Combine**:
Each specialist provides independent analysis of their layer. Orchestrator synthesizes by:
1. Timing correlation - when did performance degrade vs when changes occurred
2. Evidence strength - which findings have strongest supporting data
3. Impact severity - which issues have biggest performance impact
4. Cross-layer dependencies - how issues in one layer affect others

Root cause will be issue with:
- Strongest correlation to performance degradation timeline
- Clear evidence from specialist investigation
- Logical explanation for observed symptoms

**Quality Gates**:
- [ ] All specialists completed investigation (no gaps in analysis)
- [ ] Root cause has supporting evidence from multiple specialists
- [ ] Fix addresses root cause (not just symptoms)
- [ ] Performance restored to acceptable levels after fix

### Overall Success Criteria

**Task Complete When**:
- [x] All subtasks completed successfully (5 specialist reports received)
- [x] Outputs integrated and validated (root cause identified)
- [x] Original task fully addressed (dashboard performance restored)
- [x] Quality threshold met (8.5/10 - validated fix, no recurrence)

**Outcome**: Root cause identified in 20 minutes (parallel investigation) vs 60+ minutes sequential. Fix implemented and validated within 1 hour total.

---

## Variables Reference

| Variable | Description | Example |
|:---------|:------------|:--------|
| `{{TASK_DESCRIPTION}}` | Original complex task | "Production incident investigation" |
| `{{DOMAIN_LIST}}` | Domains involved | "BI, warehouse, transformation, infrastructure" |
| `{{APPROACH}}` | Decomposition strategy | "By system layer" or "By phase" |
| `{{SUBTASK_NAME}}` | Descriptive subtask name | "Snowflake Query Performance Analysis" |
| `{{WHAT_NEEDS_DOING}}` | Specific work for subtask | "Examine query execution plans" |
| `{{DOMAIN/SPECIALIST}}` | Required expertise | "snowflake-expert" |
| `{{DELIVERABLE}}` | Expected output | "Performance analysis report" |
| `{{HOW_TO_VALIDATE}}` | Success criteria | "Identified bottlenecks with evidence" |
| `{{NONE_OR_DEPENDS_ON}}` | Dependencies | "None" or "Requires Subtask 1" |
| `{{TIME_ESTIMATE}}` | Effort estimate | "15 minutes" |
| `{{HIGH/MEDIUM/LOW}}` | Priority level | "HIGH" |
| `{{PHASE_NAME}}` | Phase description | "Parallel Investigation" |
| `{{WHAT_MARKS_PHASE_COMPLETE}}` | Phase completion | "All specialists submitted findings" |
| `{{DESCRIBE_SYNTHESIS_APPROACH}}` | How to combine outputs | "Cross-reference timing and evidence" |
| `{{VALIDATION_CHECKPOINT_N}}` | Quality gate | "Root cause has supporting evidence" |

---

## Best Practices

### DO
- ✅ Create atomic subtasks (single responsibility)
- ✅ Assign appropriate specialists to each subtask
- ✅ Identify true dependencies (don't create artificial sequencing)
- ✅ Plan synthesis strategy upfront
- ✅ Define clear success criteria for each subtask

### DON'T
- ❌ Create subtasks that are too broad ("investigate everything")
- ❌ Assign wrong specialist to subtask
- ❌ Force sequential when parallel is possible
- ❌ Skip integration planning
- ❌ Leave success criteria vague

---

*Use this template for complex tasks requiring coordinated multi-specialist effort. Adapt variables to specific context.*
