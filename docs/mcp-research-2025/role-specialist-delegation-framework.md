# Role-Specialist Delegation Framework
**Research Date**: 2025-10-05
**Foundation**: Anthropic's Role → Specialist (with MCP) pattern
**Purpose**: Define when roles delegate to specialists, which specialist to use, and how specialists use MCP tools

---

## Executive Summary

This framework provides clear decision trees for each role agent to determine:
1. **When to delegate** (vs. handling directly)
2. **Which specialist to delegate to**
3. **What context to provide**
4. **How to validate specialist output**

### Core Principle (from Anthropic Research):
**"Delegating to specialist IS NOT added complexity - it's proper separation of concerns"**

Specialists with MCP tools = Informed decisions
Roles with MCP tools directly = Guessing with domain-specific data

---

## 1. Analytics Engineer Role → Specialist Delegation

### 1.1 Delegation Decision Tree

```
Task: Data transformation/modeling work

├─ Is this a straightforward SQL transformation?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it involve complex dbt patterns (macros, packages, advanced incremental)?
│  ├─ YES → DELEGATE to dbt-expert
│  └─ NO → Continue to next question
│
├─ Does it involve Snowflake-specific optimization?
│  ├─ YES → DELEGATE to snowflake-expert
│  └─ NO → Continue to next question
│
├─ Does it require business logic validation?
│  ├─ YES → DELEGATE to business-context
│  └─ NO → Continue to next question
│
├─ Does it involve data quality testing framework setup?
│  ├─ YES → DELEGATE to data-quality-specialist (or qa-coordinator)
│  └─ NO → Continue to next question
│
├─ Does it require documentation standards?
│  ├─ YES → DELEGATE to documentation-expert
│  └─ NO → Handle directly
│
└─ Is there architectural uncertainty?
   ├─ YES → DELEGATE to da-architect
   └─ NO → Handle directly
```

### 1.2 Specialist Assignment Matrix

| Task Type | Confidence | Specialist | MCP Tools Used | Expected Output |
|-----------|-----------|------------|----------------|-----------------|
| Complex dbt macros | <0.60 | dbt-expert | dbt-mcp, git-mcp | Validated macro implementation |
| Warehouse cost issues | <0.60 | snowflake-expert | snowflake-mcp, sequential-thinking-mcp | Cost optimization plan |
| Business metric validation | <0.60 | business-context | atlassian-mcp, dbt-mcp | Validated business requirements |
| Data quality framework | <0.60 | data-quality-specialist | dbt-mcp, great-expectations-mcp | Comprehensive test suite |
| Technical documentation | <0.60 | documentation-expert | confluence-mcp, dbt-mcp | GraniteRock-standard docs |
| System design decisions | <0.60 | da-architect | aws-mcp, snowflake-mcp, dbt-mcp | Architecture design doc |

### 1.3 Delegation Protocol

**Step 1: Recognize Need**
```
analytics-engineer-role:
  "I need to implement an incremental model with complex deduplication logic.
   This requires advanced dbt patterns beyond my expertise (confidence <0.60)."
```

**Step 2: Prepare Context**
```
context = {
  "task": "Implement incremental model for customer_transactions",
  "complexity": "Complex deduplication logic, late-arriving data, historical restatements",
  "current_state": "Existing full refresh model, 50M+ rows, 5-hour runtime",
  "requirements": "Reduce to <30 min, handle late data, support historical updates",
  "constraints": "Must maintain referential integrity with existing marts"
}
```

**Step 3: Delegate to Specialist**
```
DELEGATE TO: dbt-expert
PROVIDE: context (above)
REQUEST: "Design optimal incremental strategy with validation"
```

**Step 4: Specialist Uses MCP Tools**
```
dbt-expert:
  1. Uses dbt-mcp → Get current model metadata, compile existing SQL
  2. Uses git-mcp → Find similar incremental patterns in other models
  3. Uses snowflake-mcp → Analyze table clustering, partition strategy
  4. Uses sequential-thinking-mcp → Reason through deduplication logic
  5. Applies incremental model expertise
  6. Returns: Detailed implementation plan with dbt code
```

**Step 5: Validate Specialist Output**
```
analytics-engineer-role:
  ✅ Review dbt code for correctness
  ✅ Validate business logic alignment
  ✅ Confirm performance expectations
  ✅ Execute implementation
```

---

## 2. Data Engineer Role → Specialist Delegation

### 2.1 Delegation Decision Tree

```
Task: Data pipeline/orchestration work

├─ Is this a standard batch ingestion pipeline?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it involve Orchestra workflow orchestration?
│  ├─ YES → DELEGATE to orchestra-expert
│  └─ NO → Continue to next question
│
├─ Does it involve Prefect flow development?
│  ├─ YES → DELEGATE to prefect-expert
│  └─ NO → Continue to next question
│
├─ Does it require Airbyte/dlthub connector setup?
│  ├─ YES → DELEGATE to dlthub-expert
│  └─ NO → Continue to next question
│
├─ Does it involve AWS infrastructure changes?
│  ├─ YES → DELEGATE to aws-expert
│  └─ NO → Continue to next question
│
├─ Does it require Snowflake warehouse optimization?
│  ├─ YES → DELEGATE to snowflake-expert
│  └─ NO → Continue to next question
│
├─ Is there architectural complexity?
│  ├─ YES → DELEGATE to da-architect
│  └─ NO → Handle directly
│
└─ Does it require comprehensive testing?
   ├─ YES → DELEGATE to qa-coordinator
   └─ NO → Handle directly
```

### 2.2 Specialist Assignment Matrix

| Task Type | Confidence | Specialist | MCP Tools Used | Expected Output |
|-----------|-----------|------------|----------------|-----------------|
| Orchestra DAG design | <0.60 | orchestra-expert | orchestra-mcp, prefect-mcp, airbyte-mcp | Optimized workflow definition |
| Prefect flow optimization | <0.60 | prefect-expert | prefect-mcp, orchestra-mcp | Optimized flow implementation |
| Source connector setup | <0.60 | dlthub-expert | airbyte-mcp, snowflake-mcp | Complete ingestion pipeline |
| AWS pipeline infrastructure | <0.60 | aws-expert | aws-api-mcp, aws-knowledge-mcp | Infrastructure deployment plan |
| Warehouse loading optimization | <0.60 | snowflake-expert | snowflake-mcp, sequential-thinking-mcp | Loading strategy optimization |
| System architecture | <0.60 | da-architect | All relevant MCP tools | Architecture design document |

### 2.3 Delegation Protocol Example

**Scenario**: Complex Orchestra workflow with multiple dependencies

**Step 1: Recognize Need**
```
data-engineer-role:
  "I need to orchestrate a complex workflow:
   Airbyte sync → dbt staging → Prefect validation → dbt marts.
   This involves cross-system dependencies beyond my expertise."
```

**Step 2: Prepare Context**
```
context = {
  "task": "Orchestrate multi-system data pipeline",
  "systems": ["Airbyte", "dbt Cloud", "Prefect", "Snowflake"],
  "dependencies": "Airbyte → dbt staging → Prefect validation → dbt marts → Tableau refresh",
  "requirements": "Complete within 2-hour window, handle failures gracefully",
  "current_state": "Manual execution, frequent failures, no error handling"
}
```

**Step 3: Delegate**
```
DELEGATE TO: orchestra-expert
PROVIDE: context
REQUEST: "Design resilient Orchestra workflow with proper error handling"
```

**Step 4: Specialist Uses MCP Tools**
```
orchestra-expert:
  1. Uses orchestra-mcp → Get current workflow definitions, analyze dependencies
  2. Uses airbyte-mcp → Get connector metadata, sync schedules
  3. Uses dbt-mcp → Get job metadata, execution history
  4. Uses prefect-mcp → Get flow metadata, task dependencies
  5. Uses slack-mcp → Configure failure notifications
  6. Applies orchestration expertise
  7. Returns: Complete Orchestra workflow YAML with error handling
```

**Step 5: Validate**
```
data-engineer-role:
  ✅ Review workflow dependencies for correctness
  ✅ Validate error handling logic
  ✅ Confirm SLA windows achievable
  ✅ Execute deployment
```

---

## 3. BI Developer Role → Specialist Delegation

### 3.1 Delegation Decision Tree

```
Task: Dashboard development/optimization

├─ Is this straightforward Tableau dashboard creation?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it involve complex Tableau performance issues?
│  ├─ YES → DELEGATE to tableau-expert
│  └─ NO → Continue to next question
│
├─ Does it require data source optimization in Snowflake?
│  ├─ YES → DELEGATE to snowflake-expert
│  └─ NO → Continue to next question
│
├─ Does it need semantic layer/dbt mart design?
│  ├─ YES → DELEGATE to dbt-expert (via analytics-engineer-role)
│  └─ NO → Continue to next question
│
├─ Does it involve business metric validation?
│  ├─ YES → DELEGATE to business-context
│  └─ NO → Continue to next question
│
├─ Does it require UI/UX design expertise?
│  ├─ YES → DELEGATE to ui-ux-expert
│  └─ NO → Handle directly
│
└─ Does it need documentation?
   ├─ YES → DELEGATE to documentation-expert
   └─ NO → Handle directly
```

### 3.2 Specialist Assignment Matrix

| Task Type | Confidence | Specialist | MCP Tools Used | Expected Output |
|-----------|-----------|------------|----------------|-----------------|
| Dashboard performance issues | <0.60 | tableau-expert | tableau-mcp, snowflake-mcp, filesystem-mcp | Performance optimization plan |
| Data source query optimization | <0.60 | snowflake-expert | snowflake-mcp, dbt-mcp | Optimized queries and indexes |
| Semantic layer design | <0.60 | analytics-engineer-role → dbt-expert | dbt-mcp, business-context via atlassian-mcp | Semantic model design |
| Business metric validation | <0.60 | business-context | atlassian-mcp, dbt-mcp | Validated metric definitions |
| Dashboard UX design | <0.60 | ui-ux-expert | filesystem-mcp, notion-mcp | UX design recommendations |
| User documentation | <0.60 | documentation-expert | confluence-mcp, tableau-mcp | End-user guide |

---

## 4. Cloud Manager Role → Specialist Delegation

### 4.1 Delegation Decision Tree

```
Task: Cloud infrastructure management

├─ Is this routine AWS resource management?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it involve complex AWS architecture decisions?
│  ├─ YES → DELEGATE to aws-expert
│  └─ NO → Continue to next question
│
├─ Does it require cost optimization analysis?
│  ├─ YES → DELEGATE to cost-optimization-specialist
│  └─ NO → Continue to next question
│
├─ Does it involve data platform infrastructure?
│  ├─ YES → DELEGATE to da-architect
│  └─ NO → Continue to next question
│
├─ Does it need deployment automation?
│  ├─ YES → DELEGATE to aws-expert (with github-mcp)
│  └─ NO → Continue to next question
│
└─ Does it require multi-cloud strategy?
   ├─ YES → DELEGATE to multi-cloud-specialist (if available) or da-architect
   └─ NO → Handle directly
```

### 4.2 Specialist Assignment Matrix

| Task Type | Confidence | Specialist | MCP Tools Used | Expected Output |
|-----------|-----------|------------|----------------|-----------------|
| AWS architecture design | <0.60 | aws-expert | aws-api-mcp, aws-knowledge-mcp, aws-docs-mcp | Well-Architected solution design |
| Cost anomaly investigation | <0.60 | cost-optimization-specialist | aws-api-mcp, snowflake-mcp, sequential-thinking-mcp | Cost reduction recommendations |
| Data platform infrastructure | <0.60 | da-architect | aws-mcp, snowflake-mcp, dbt-mcp | Infrastructure architecture |
| CI/CD pipeline setup | <0.60 | aws-expert + github-sleuth-expert | aws-api-mcp, github-mcp | Automated deployment pipeline |

---

## 5. Project Manager Role → Specialist Delegation

### 5.1 Delegation Decision Tree

```
Task: Project management/coordination

├─ Is this standard project tracking in Jira?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it require GitHub repository investigation?
│  ├─ YES → DELEGATE to github-sleuth-expert
│  └─ NO → Continue to next question
│
├─ Does it need technical documentation creation/updates?
│  ├─ YES → DELEGATE to documentation-expert
│  └─ NO → Continue to next question
│
├─ Does it involve business requirements gathering?
│  ├─ YES → DELEGATE to business-context
│  └─ NO → Continue to next question
│
├─ Does it require comprehensive QA planning?
│  ├─ YES → DELEGATE to qa-coordinator
│  └─ NO → Continue to next question
│
└─ Does it need system architecture assessment?
   ├─ YES → DELEGATE to da-architect
   └─ NO → Handle directly
```

### 5.2 Specialist Assignment Matrix

| Task Type | Confidence | Specialist | MCP Tools Used | Expected Output |
|-----------|-----------|------------|----------------|-----------------|
| Repository analysis/PR review | <0.60 | github-sleuth-expert | github-mcp, git-mcp | Code review findings, pattern analysis |
| Technical documentation | <0.60 | documentation-expert | confluence-mcp, github-mcp | GraniteRock-standard documentation |
| Requirements gathering | <0.60 | business-context | atlassian-mcp, slack-mcp | Validated business requirements |
| QA strategy development | <0.60 | qa-coordinator | dbt-mcp, snowflake-mcp, github-mcp | Comprehensive test plan |
| Architecture review | <0.60 | da-architect | All relevant MCP tools | Architecture assessment |

---

## 6. UI/UX Developer Role → Specialist Delegation

### 6.1 Delegation Decision Tree

```
Task: UI/UX development

├─ Is this straightforward React component development?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it involve AWS infrastructure deployment?
│  ├─ YES → DELEGATE to aws-expert
│  └─ NO → Continue to next question
│
├─ Does it require complex React patterns?
│  ├─ YES → DELEGATE to react-expert
│  └─ NO → Continue to next question
│
├─ Does it need backend data integration?
│  ├─ YES → DELEGATE to data-engineer-role or analytics-engineer-role
│  └─ NO → Continue to next question
│
├─ Does it involve UX design decisions?
│  ├─ YES → DELEGATE to ui-ux-expert
│  └─ NO → Continue to next question
│
└─ Does it need comprehensive testing?
   ├─ YES → DELEGATE to qa-coordinator
   └─ NO → Handle directly
```

### 6.2 Specialist Assignment Matrix

| Task Type | Confidence | Specialist | MCP Tools Used | Expected Output |
|-----------|-----------|------------|----------------|-----------------|
| AWS deployment (ECS, ALB, CloudFront) | <0.60 | aws-expert | aws-api-mcp, aws-knowledge-mcp | Deployment architecture and configs |
| Complex React patterns | <0.60 | react-expert | github-mcp, git-mcp | React implementation patterns |
| Data API integration | <0.60 | data-engineer-role | snowflake-mcp, dbt-mcp | API design and implementation |
| UX design optimization | <0.60 | ui-ux-expert | filesystem-mcp, notion-mcp | UX design recommendations |
| Frontend testing strategy | <0.60 | qa-coordinator | github-mcp | Test automation framework |

---

## 7. Data Architect Role → Specialist Delegation

### 7.1 Delegation Decision Tree

```
Task: System architecture/design

├─ Is this high-level architecture conceptual design?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it require deep AWS infrastructure expertise?
│  ├─ YES → CONSULT with aws-expert (collaborative)
│  └─ NO → Continue to next question
│
├─ Does it need Snowflake-specific architecture?
│  ├─ YES → CONSULT with snowflake-expert (collaborative)
│  └─ NO → Continue to next question
│
├─ Does it involve dbt transformation architecture?
│  ├─ YES → CONSULT with dbt-expert (collaborative)
│  └─ NO → Continue to next question
│
├─ Does it require orchestration design?
│  ├─ YES → CONSULT with orchestra-expert (collaborative)
│  └─ NO → Continue to next question
│
└─ Does it need cost optimization focus?
   ├─ YES → CONSULT with cost-optimization-specialist
   └─ NO → Handle directly
```

**Note**: Data Architect primarily CONSULTS with specialists (collaborative pattern) rather than delegating

### 7.2 Collaboration Matrix

| Architecture Component | Collaborating Specialist | MCP Tools (Shared Access) | Collaborative Output |
|------------------------|-------------------------|---------------------------|---------------------|
| AWS infrastructure layer | aws-expert | aws-mcp suite | Infrastructure architecture component |
| Data warehouse layer | snowflake-expert | snowflake-mcp | Warehouse architecture component |
| Transformation layer | dbt-expert | dbt-mcp | Transformation architecture component |
| Orchestration layer | orchestra-expert | orchestra-mcp, prefect-mcp | Orchestration architecture component |
| Cost optimization | cost-optimization-specialist | aws-api-mcp, snowflake-mcp | Cost-optimized architecture |

---

## 8. DBA Role → Specialist Delegation

### 8.1 Delegation Decision Tree

```
Task: Database administration

├─ Is this routine database maintenance?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it involve Snowflake-specific optimization?
│  ├─ YES → DELEGATE to snowflake-expert
│  └─ NO → Continue to next question
│
├─ Does it require query performance tuning (dbt context)?
│  ├─ YES → COLLABORATE with dbt-expert + snowflake-expert
│  └─ NO → Continue to next question
│
├─ Does it need data quality validation?
│  ├─ YES → DELEGATE to data-quality-specialist
│  └─ NO → Continue to next question
│
└─ Does it involve architecture changes?
   ├─ YES → DELEGATE to da-architect
   └─ NO → Handle directly
```

---

## 9. QA Engineer Role → Specialist Delegation

### 9.1 Delegation Decision Tree

```
Task: Quality assurance/testing

├─ Is this straightforward manual testing?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it require comprehensive QA strategy?
│  ├─ YES → DELEGATE to qa-coordinator
│  └─ NO → Continue to next question
│
├─ Does it involve dbt test automation?
│  ├─ YES → DELEGATE to dbt-expert
│  └─ NO → Continue to next question
│
├─ Does it need data quality framework?
│  ├─ YES → DELEGATE to data-quality-specialist
│  └─ NO → Continue to next question
│
├─ Does it require UI testing automation?
│  ├─ YES → DELEGATE to react-expert or qa-coordinator
│  └─ NO → Handle directly
│
└─ Does it involve pipeline testing?
   ├─ YES → DELEGATE to orchestra-expert or prefect-expert
   └─ NO → Handle directly
```

---

## 10. Business Analyst Role → Specialist Delegation

### 10.1 Delegation Decision Tree

```
Task: Business analysis/requirements

├─ Is this straightforward requirements documentation?
│  ├─ YES → Handle directly (Primary Expertise ≥0.85)
│  └─ NO → Continue to next question
│
├─ Does it require technical feasibility analysis?
│  ├─ YES → DELEGATE to business-context (technical translation)
│  └─ NO → Continue to next question
│
├─ Does it involve metric definition validation?
│  ├─ YES → COLLABORATE with business-context + dbt-expert
│  └─ NO → Continue to next question
│
├─ Does it need data model design?
│  ├─ YES → DELEGATE to analytics-engineer-role → dbt-expert
│  └─ NO → Continue to next question
│
└─ Does it require dashboard design?
   ├─ YES → DELEGATE to bi-developer-role
   └─ NO → Handle directly
```

---

## 11. Delegation Best Practices

### 11.1 Context Preparation Checklist

Before delegating to any specialist, prepare:

**Essential Context**:
- [ ] Clear task description
- [ ] Current state analysis
- [ ] Requirements and constraints
- [ ] Success criteria
- [ ] Timeline expectations
- [ ] Dependencies and blockers
- [ ] Relevant file paths or resource IDs

**Example**:
```json
{
  "task": "Optimize slow-running dbt model",
  "current_state": {
    "model": "models/marts/customer_lifetime_value.sql",
    "runtime": "45 minutes",
    "target_runtime": "<5 minutes",
    "row_count": "10M rows",
    "warehouse": "TRANSFORMING_MEDIUM"
  },
  "requirements": {
    "maintain_accuracy": true,
    "incremental_preferred": true,
    "must_complete_by": "6am daily"
  },
  "constraints": {
    "cannot_change_grain": "customer_id",
    "must_maintain_history": "2 years"
  },
  "blockers": [],
  "dependencies": ["dim_customers", "fact_transactions"]
}
```

### 11.2 Specialist Output Validation

After receiving specialist recommendations, validate:

**Correctness Checks**:
- [ ] Recommendations address stated requirements
- [ ] Solution is technically feasible
- [ ] Quality standards met
- [ ] No unintended side effects
- [ ] Costs within acceptable range
- [ ] Timeline realistic

**Integration Checks**:
- [ ] Compatible with existing systems
- [ ] Follows organizational standards
- [ ] Documentation complete
- [ ] Testing strategy included
- [ ] Rollback plan provided

### 11.3 Multi-Specialist Coordination

For complex tasks requiring multiple specialists:

**Sequential Pattern** (dependency chain):
```
business-analyst-role
    ↓ (gather requirements)
business-context (validate business logic)
    ↓ (technical feasibility)
analytics-engineer-role
    ↓ (complex transformation)
dbt-expert (implement model)
    ↓ (query optimization)
snowflake-expert (optimize performance)
    ↓ (testing)
qa-coordinator (comprehensive validation)
```

**Parallel Pattern** (independent analysis):
```
project-manager-role
    ├─ github-sleuth-expert (code analysis)
    ├─ documentation-expert (docs review)
    ├─ qa-coordinator (test coverage)
    └─ business-context (requirements validation)

project-manager-role (synthesize findings)
```

### 11.4 Delegation Anti-Patterns (Avoid These)

**❌ Premature Delegation**:
```
# BAD: Delegating simple tasks within role expertise
analytics-engineer-role → dbt-expert for basic SELECT query
```

**❌ Delegation Loops**:
```
# BAD: Circular delegation
analytics-engineer-role → dbt-expert → analytics-engineer-role
```

**❌ Insufficient Context**:
```
# BAD: Vague delegation
"Fix the dbt model" (no context, requirements, or current state)
```

**❌ Ignoring Specialist Recommendations**:
```
# BAD: Requesting specialist input then ignoring it
Request dbt-expert analysis → Implement different approach anyway
```

**✅ Correct Patterns**:
- Delegate when confidence <0.60
- Provide complete context
- Validate specialist output
- Implement recommendations (or discuss why not)
- Learn from specialist expertise

---

## 12. Success Metrics

### 12.1 Delegation Effectiveness

Track these metrics:

**Delegation Frequency**:
- % of tasks delegated vs. handled directly
- Delegation patterns by role
- Most-used specialists

**Delegation Quality**:
- % of specialist recommendations implemented
- % of tasks requiring re-delegation
- User satisfaction with specialist output

**Time Metrics**:
- Average time from delegation to resolution
- Comparison: delegated vs. direct handling
- Specialist response time

**Outcome Metrics**:
- % of delegated tasks successful on first attempt
- % reduction in errors (delegated vs. direct)
- Quality improvement (delegated vs. direct)

### 12.2 Continuous Improvement

**Monthly Review**:
- Analyze delegation patterns
- Identify gaps in specialist coverage
- Assess specialist MCP tool usage
- Update delegation decision trees

**Quarterly Review**:
- Evaluate specialist effectiveness
- Consider new specialist roles needed
- Assess MCP server enhancement needs
- Update confidence thresholds

---

## 13. Quick Reference Cards

### 13.1 Analytics Engineer Quick Reference

**I should delegate when**:
- Complex dbt patterns (macros, packages) → dbt-expert
- Warehouse performance issues → snowflake-expert
- Business logic validation → business-context
- Data quality framework → data-quality-specialist
- Technical documentation → documentation-expert

**I provide this context**:
- Model/task description
- Current runtime/performance
- Target metrics
- Business requirements
- Constraints

**I validate by checking**:
- dbt code correctness
- Performance expectations
- Business logic alignment
- Test coverage

### 13.2 Data Engineer Quick Reference

**I should delegate when**:
- Orchestra workflow complexity → orchestra-expert
- Prefect flow optimization → prefect-expert
- Source connector setup → dlthub-expert
- AWS infrastructure → aws-expert
- Warehouse optimization → snowflake-expert

**I provide this context**:
- Pipeline description
- Source/destination details
- SLA requirements
- Current state/issues
- Dependencies

**I validate by checking**:
- Pipeline reliability
- Error handling
- SLA compliance
- Resource optimization

### 13.3 Cloud Manager Quick Reference

**I should delegate when**:
- AWS architecture decisions → aws-expert
- Cost optimization → cost-optimization-specialist
- Data platform infrastructure → da-architect
- Multi-cloud strategy → multi-cloud-specialist

**I provide this context**:
- Infrastructure requirements
- Current architecture
- Budget constraints
- Performance needs
- Security requirements

**I validate by checking**:
- Well-Architected compliance
- Cost within budget
- Security best practices
- Performance meets SLAs

---

**Document Status**: Delegation Framework Complete
**Next Steps**: Create architecture migration plan
**Usage**: Reference this framework for all role-specialist delegation decisions
