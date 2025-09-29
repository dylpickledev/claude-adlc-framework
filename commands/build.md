# /build Command Protocol

## Purpose
Execute highest priority ideas as complete projects. Implements ADLC Develop + Test + Deploy phases with specialist agent coordination and full project management integration.

## Usage
```bash
claude /build [idea-name]
```

## Protocol

### 1. Execute build.sh Script
```bash
./scripts/build.sh [idea-name]
```

### 2. Complete Project Creation Workflow
- **Finds organized ideas**: Searches `ideas/organized/` and `ideas/pipeline/`
- **Promotes to pipeline**: Uses `ideate-promote.sh` for idea enhancement
- **Creates project structure**: Integrates with `work-init.sh` for full project setup
- **Archives idea**: Links idea to active project with traceability
- **Provides development guidance**: Next steps for implementation

## Claude Instructions

When user runs `/build [idea-name]`:

1. **Execute the script**: Run `./scripts/build.sh [idea-name]`
2. **Monitor project creation**: Display each step of the promotion and setup
3. **Validate structure**: Confirm project directory and files created properly
4. **Analyze project requirements**: Read the created spec.md to understand project scope
5. **Identify relevant agents**: Use the Agent Identification Logic below
6. **Create coordination plan**: Generate specific agent assignments and workflow
7. **Guide development**: Present agent recommendations and next steps

### Response Format
```
🔧 Building project for idea: [idea-name]
📋 Found idea in organized: [path]
📦 Promoting idea to pipeline...
🏗️ Creating project structure...
✅ Project structure created
📚 Archiving idea with project reference...

✅ Idea successfully built into project!
📁 Project location: projects/active/[project-name]/

🎯 Next steps:
   1. Review project spec: projects/active/[project-name]/spec.md
   2. Begin development work
   3. When complete: ./scripts/finish.sh [project-name]
```

## Integration with ADLC
- **ADLC Develop Phase**: Human-readable code with specialist agent guidance
- **ADLC Test Phase**: Quality assurance through agent coordination
- **ADLC Deploy Phase**: Integration with existing CI/CD workflows
- **Cross-layer context**: Maintains links from planning through operations

## Project Structure Created
```
projects/active/feature-[idea-name]/
├── README.md           # Navigation hub with progress tracking
├── spec.md            # Project specification from enhanced idea
├── context.md         # Dynamic state tracking
└── tasks/             # Agent coordination directory
    ├── current-task.md     # Current agent assignments
    └── [tool]-findings.md  # Detailed agent findings
```

## Agent Identification Logic

After project creation, analyze the spec.md to automatically identify which specialist agents should be coordinated. Use these keyword patterns and project characteristics:

### Agent Selection Matrix

| Agent | Primary Keywords | Project Characteristics |
|-------|-----------------|------------------------|
| **da-architect** | architecture, design, integration, system, platform, multi-tool, optimization, strategy | Cross-repository work, strategic decisions, technology selection, complex integrations |
| **dbt-expert** | dbt, model, transformation, SQL, test, mart, staging, incremental | dbt model development, SQL transformations, data testing, dbt project structure |
| **snowflake-expert** | snowflake, warehouse, query, performance, cost, compute, storage | Query optimization, warehouse configuration, cost analysis, Snowflake-specific features |
| **tableau-expert** | tableau, dashboard, visualization, report, workbook, prep | Dashboard development, Tableau Prep flows, visualization design, user experience |
| **orchestra-expert** | orchestra, workflow, pipeline, orchestration, dependency, scheduling | Workflow design, pipeline orchestration, job scheduling, dependency management |
| **dlthub-expert** | dlthub, ingestion, source, extraction, connector, API | Data ingestion, source system integration, API connections, data loading |
| **prefect-expert** | prefect, flow, task, legacy, migration | Prefect-specific work, legacy pipeline maintenance, flow performance |
| **business-context** | requirements, stakeholder, business logic, validation, domain, safety, construction, materials | Requirements gathering, business rule validation, domain expertise needed |
| **documentation-expert** | documentation, guide, standards, readme, user guide | Creating comprehensive documentation, user guides, team standards |

### Multi-Agent Coordination Patterns

**Pattern 1: Full Stack Data Product**
- Keywords: "end-to-end", "new data product", "source to report"
- Agents: da-architect (lead) → dlthub-expert → dbt-expert → snowflake-expert → tableau-expert → documentation-expert

**Pattern 2: dbt Model Development**
- Keywords: "dbt model", "transformation", "data mart"
- Agents: dbt-expert (lead) → snowflake-expert (performance) → documentation-expert

**Pattern 3: Dashboard/Reporting**
- Keywords: "dashboard", "visualization", "tableau", "report"
- Agents: tableau-expert (lead) → dbt-expert (if model changes needed) → business-context → documentation-expert

**Pattern 4: Performance Optimization**
- Keywords: "slow", "performance", "optimization", "cost"
- Agents: da-architect (analysis) → snowflake-expert/dbt-expert (implementation) → orchestra-expert (if orchestration involved)

**Pattern 5: Data Integration**
- Keywords: "integration", "ingestion", "source system", "API"
- Agents: da-architect (design) → dlthub-expert (implementation) → dbt-expert (transformation) → documentation-expert

**Pattern 6: Research Investigation**
- Keywords: "investigate", "research", "analyze", "troubleshoot"
- Agents: da-architect (coordination) → relevant domain experts based on system → documentation-expert

### Agent Recommendation Output Format

After identifying relevant agents, present recommendations like this:

```markdown
## 🤖 Recommended Agent Coordination Plan

### Primary Agents
1. **[agent-name]** - [specific responsibility]
2. **[agent-name]** - [specific responsibility]

### Supporting Agents
- **[agent-name]**: [when to involve]
- **[agent-name]**: [when to involve]

### Suggested Workflow
1. **Phase 1**: [agent-name] - [task description]
2. **Phase 2**: [agent-name] - [task description]
3. **Phase 3**: [agent-name] - [task description]

### Coordination Notes
- [Any cross-agent dependencies]
- [Sequencing requirements]
- [Integration points between agents]
```

## Specialist Agent Coordination
The build process enables access to:
- **da-architect**: System design, data flow analysis, strategic decisions, agent coordination
- **dbt-expert**: SQL transformations, model optimization, test development
- **snowflake-expert**: Query performance, cost analysis, warehouse optimization
- **tableau-expert**: Dashboard development, report model analysis, Tableau Prep flows
- **orchestra-expert**: Workflow orchestration leadership, dependency management
- **dlthub-expert**: Data ingestion, source system integration, connector development
- **prefect-expert**: Prefect flow performance when Orchestra triggers them
- **business-context**: Requirements gathering, stakeholder alignment, domain expertise
- **documentation-expert**: Consistent standards across all outputs, user guides

## Examples

### Example 1: Analytics Model Development
```bash
claude /build customer-churn-prediction
# → Creates: projects/active/feature-customer-churn-prediction/
```

**Agent Coordination Plan:**
```markdown
## 🤖 Recommended Agent Coordination Plan

### Primary Agents
1. **dbt-expert** - Design and implement churn prediction models
2. **snowflake-expert** - Optimize query performance for large customer datasets

### Supporting Agents
- **business-context**: Define churn criteria and business rules
- **da-architect**: Design overall data product architecture if cross-system
- **documentation-expert**: Create model documentation and user guides

### Suggested Workflow
1. **Phase 1**: business-context - Clarify churn definition and success metrics
2. **Phase 2**: dbt-expert - Implement staging and mart models
3. **Phase 3**: snowflake-expert - Performance tuning and optimization
4. **Phase 4**: documentation-expert - Model documentation and usage guides

### Coordination Notes
- dbt-expert and snowflake-expert should collaborate on query optimization
- business-context validates logic before final deployment
```

### Example 2: Dashboard Project
```bash
claude /build executive-kpi-dashboard
# → Creates: projects/active/feature-executive-kpi-dashboard/
```

**Agent Coordination Plan:**
```markdown
## 🤖 Recommended Agent Coordination Plan

### Primary Agents
1. **tableau-expert** - Dashboard design and development
2. **business-context** - KPI definitions and stakeholder requirements

### Supporting Agents
- **dbt-expert**: Model changes if underlying data needs transformation
- **snowflake-expert**: Performance if dashboard queries are slow
- **documentation-expert**: User guide creation

### Suggested Workflow
1. **Phase 1**: business-context - Gather KPI requirements and user needs
2. **Phase 2**: dbt-expert - Ensure reporting models exist (if needed)
3. **Phase 3**: tableau-expert - Design and build dashboard
4. **Phase 4**: documentation-expert - Create user training materials

### Coordination Notes
- tableau-expert checks with dbt-expert on data availability first
- Iterative design reviews with business-context stakeholders
```

### Example 3: Infrastructure Optimization
```bash
claude /build snowflake-cost-optimization
# → Creates: projects/active/feature-snowflake-cost-optimization/
```

**Agent Coordination Plan:**
```markdown
## 🤖 Recommended Agent Coordination Plan

### Primary Agents
1. **da-architect** - System-wide cost analysis and strategy
2. **snowflake-expert** - Warehouse configuration and query optimization

### Supporting Agents
- **dbt-expert**: Optimize model materialization strategies
- **orchestra-expert**: Adjust scheduling for off-peak compute
- **documentation-expert**: Document optimization patterns

### Suggested Workflow
1. **Phase 1**: da-architect - Analyze current costs and identify opportunities
2. **Phase 2**: snowflake-expert - Implement warehouse-level optimizations
3. **Phase 3**: dbt-expert - Refactor expensive model patterns
4. **Phase 4**: orchestra-expert - Optimize scheduling and clustering
5. **Phase 5**: documentation-expert - Create cost optimization playbook

### Coordination Notes
- All agents should coordinate on shared cost reduction goals
- Measure impact after each phase before proceeding
```

### Example 4: Safety Report Investigation
```bash
claude /build safety-report-investigation
# → Creates: projects/active/research-safety-report-investigation/
```

**Agent Coordination Plan:**
```markdown
## 🤖 Recommended Agent Coordination Plan

### Primary Agents
1. **tableau-expert** - Analyze Tableau Prep flows and workbooks
2. **da-architect** - Coordinate investigation and system analysis

### Supporting Agents
- **business-context**: Understand safety domain requirements
- **dbt-expert**: Check underlying data models if needed
- **documentation-expert**: Create investigation report

### Suggested Workflow
1. **Phase 1**: da-architect - Initial assessment and investigation planning
2. **Phase 2**: tableau-expert - Deep dive into Tableau Prep and workbook analysis
3. **Phase 3**: business-context - Validate findings against business requirements
4. **Phase 4**: dbt-expert - Investigate upstream data quality if issues found
5. **Phase 5**: documentation-expert - Comprehensive investigation report

### Coordination Notes
- Research project with investigation focus
- tableau-expert leads technical analysis
- da-architect ensures comprehensive system view
```

## Success Criteria
- [ ] Idea found and promoted to pipeline successfully
- [ ] Complete project structure created with all required files
- [ ] Idea archived with proper project references and traceability
- [ ] Development guidance provided for next steps
- [ ] Specialist agent coordination enabled

## Development Workflow
After project creation:
1. **Review spec.md**: Understand enhanced requirements and implementation plan
2. **Coordinate with agents**: Use specialist agents for domain expertise
3. **Implement iteratively**: Follow ADLC Develop/Test cycles
4. **Deploy with quality**: Ensure testing and review before deployment
5. **Complete project**: Use `/finish [project-name]` when done

## Error Handling
- **Idea not found**: Lists available ideas with clear naming guidance
- **Project creation fails**: Falls back to basic structure if `work-init.sh` unavailable
- **Missing dependencies**: Provides clear error messages and resolution steps

---

*Complete ADLC Develop + Test + Deploy implementation - from organized idea to production-ready project.*