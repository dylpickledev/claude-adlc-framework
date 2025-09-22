don't look at the full .env file. Only search for the var names up to the equals sign.

## Knowledge Repository Structure

### D&A Team Documentation
The `knowledge/da_team_documentation/` directory contains comprehensive Data & Analytics team documentation migrated from Confluence:

- **Location**: `knowledge/da_team_documentation/readme.md`
- **Purpose**: Authoritative source for GraniteRock's Data & Analytics team documentation
- **Structure**: Organized by data products, architecture, integrations, and templates
- **Navigation**: Use the readme.md as the main entry point for team documentation

### Knowledge Folder Management
- **Top-level files**: Included in version control for team collaboration
- **Subfolders**: Generally excluded (other knowledge repos should be separately source controlled)
- **Exception**: `knowledge/da_team_documentation/` is fully tracked for team documentation

## Repository Branch Structures

### dbt_cloud
- **master**: Production branch
- **dbt_dw**: Staging branch
- **Workflow**: Branch from dbt_dw, sync before creating features

### dbt_errors_to_issues
- **main**: Production branch (no staging branch)
- **Workflow**: Branch directly from main

### roy_kent
- **master**: Production branch (no staging branch)  
- **Workflow**: Branch directly from master

### sherlock
- **main**: Production branch (no staging branch)
- **Workflow**: Branch directly from main

## General Git Workflow

### Branch Naming Convention
- Feature branches: `feature/description`
- Fix branches: `fix/description`

### Standard Workflow Steps
1. Sync with production/staging branch before creating features
2. Create descriptive branch names
3. Keep branches focused and atomic
4. Test locally before pushing

## Cross-System Issue Analysis & Coordination

### Common Issue Categories (Multi-Tool)
1. **Schema/Column Reference Errors**: Tests referencing incorrect column names vs actual model schemas
2. **Data Quality Issues**: Uniqueness constraint violations, null constraint failures, massive duplications
3. **Cross-System Validation Failures**: Mismatches between source systems and dbt model expectations
4. **Business Logic Validation**: Failed reconciliation tests, metric validation errors

### Architecture-Aware Analysis Approach
- **Data Flow Context**: Issues often span multiple layers (Orchestra → [Prefect, dbt, Airbyte] → Snowflake → Semantic Layer)
- **Orchestra-Centric**: Orchestra kicks off everything - Prefect flows, dbt jobs, Airbyte syncs, direct Snowflake operations
- **Model Layer Impact**: Problems cascade from staging (stg_) through marts (dm_) to reports (rpt_)
- **Source System Dependencies**: ERP, Customer, Operations, Safety systems create different data patterns

### Cross-Tool Prioritization Framework
1. **CRITICAL**: Schema compilation errors that block other work (dbt-expert)
2. **HIGH**: Large-scale data quality issues indicating upstream pipeline problems (orchestra-expert + dlthub-expert)
3. **MEDIUM**: Business logic and validation failures (dbt-expert + business-context)
4. **LOW**: Warning-level issues that don't break functionality

### Agent Coordination Strategy
- **orchestra-expert**: LEADS all workflow analysis - Orchestra kicks off everything (Prefect, dbt, Airbyte, Snowflake)
- **dbt-expert**: Examine model schemas vs test expectations, focus on blocking compilation issues first
- **prefect-expert**: Prefect flow performance analysis when Orchestra triggers them
- **snowflake-expert**: Validate warehouse-level performance and data quality issues
- **dlthub-expert**: Source system data quality for cross-system reconciliation failures
- **tableau-expert**: Dashboard performance issues stemming from data problems
- **business-context**: Business logic validation and stakeholder requirement clarification
- **da-architect**: System design, data flow analysis, and strategic platform decisions across the entire data stack

- git branches should be prefixed by feature/ or fix/
- use subagents for tasks to help optimize your context window. Determine if it'd be best to use defined agent, or if its general then give to a general subagent

## Task vs Project Classification

### Use Project Structure (`/start_project` + `projects/` directory) When:
- **Multi-day efforts** that span multiple work sessions
- **Cross-repository coordination** (dbt + snowflake + tableau changes)
- **Research and analysis** that will inform multiple decisions
- **Collaborative work** with team members or reviewers
- **Knowledge preservation** needed for future reference
- **Complex troubleshooting** requiring systematic investigation

### Use Simple Task Execution (TodoWrite + direct action) When:
- **Quick fixes** (typos, small config changes, single-file updates)  
- **Immediate responses** to questions or information requests
- **One-off scripts** or utilities
- **Documentation updates** that don't require research
- **Status checks** or system diagnostics
- **Simple file operations** or code formatting

### Communication Patterns
- **Project Work**: Sub-agents read requirements from `projects/<project-name>/spec.md`, receive tasks from `projects/<project-name>/tasks/current-task.md`, and write findings to `projects/<project-name>/tasks/[tool]-findings.md`
- **Simple Tasks**: Direct TodoWrite tracking, immediate execution, no intermediate files

## Spec-Driven Development Commands

### Critical First Step: Branch Creation
**ALWAYS create feature branch BEFORE any project file creation:**

```bash
git checkout -b feature/[project-name]
```

**Then proceed with project structure and files.**

### Data Analytics Project Lifecycle
Use structured commands for complex multi-tool data projects:

1. **`/specify [project description]`** - Create specification and feature branch
2. **`/plan [technical details]`** - Generate implementation plan with tool coordination
3. **`/tasks [context]`** - Break down into executable tasks with sub-agent assignments

### Command Usage Examples

#### /specify Command
```
/specify Build a daily customer metrics dashboard that shows customer acquisition, retention, and lifetime value trends. Need data from CRM, billing, and support systems refreshed nightly for executive team review.
```

#### /plan Command
```  
/plan Use dbt for transformations, Snowflake for storage, Tableau for visualization, and Orchestra for orchestration. Data sources include Salesforce CRM, Stripe billing, and Freshservice support tickets.
```

#### /tasks Command
```
/tasks Focus on cross-tool integration testing and sub-agent coordination for staged implementation.
```

### When to Use Spec-Driven Commands
- **Multi-tool projects** spanning dbt, Snowflake, Tableau, Orchestra, Prefect
- **Cross-repository coordination** requiring multiple experts
- **Business stakeholder alignment** needing clear specifications
- **Complex data pipelines** with multiple integration points
- **Workflow orchestration** requiring Prefect deployment coordination
- **Projects requiring systematic validation** across tool boundaries

### Project File Structure
Each project created with `/start_project` follows this structure:

```
projects/active/<project-name>/
├── README.md           # Navigation hub with quick links and progress
├── spec.md            # Project specification (stable requirements)
├── context.md         # Working context (dynamic state tracking)
└── tasks/             # Agent coordination directory
    ├── current-task.md     # Current agent assignments
    └── <tool>-findings.md  # Detailed agent findings
```

#### File Purposes:
- **README.md**: Entry point for navigation, progress summary, key decisions
- **spec.md**: Stable project requirements, end goals, implementation plan, success criteria
- **context.md**: Dynamic state tracking - branches, PRs, blockers, current focus
- **tasks/**: Agent coordination - task assignments and detailed findings

## Test-Driven Data Development (TDD)

### Data Testing Workflow
Follow Claude Code's TDD best practice adapted for data work:

1. **Write Tests First**: Create dbt tests before implementing models
   ```sql
   -- tests/assert_customer_ids_unique.sql
   select customer_id, count(*)
   from {{ ref('stg_customers') }}
   group by customer_id
   having count(*) > 1
   ```

2. **Confirm Test Failures**: Run tests to verify they initially fail
   ```bash
   dbt test --select stg_customers --store-failures
   ```

3. **Implement Model Logic**: Write SQL to pass tests
   ```sql
   -- models/staging/stg_customers.sql
   select distinct customer_id, customer_name
   from {{ source('erp', 'customers') }}
   ```

4. **Verify No Overfitting**: Test against production data samples
   ```bash
   dbt test --select stg_customers --vars '{"test_data_sample": 1000}'
   ```

### Data Quality Testing Strategy
- **Schema Tests**: Column existence, data types, constraints
- **Business Logic Tests**: Reconciliation, metric validation, referential integrity
- **Performance Tests**: Query execution time, result set sizes
- **Cross-System Tests**: Source system vs. warehouse validation

### TDD Commands for Data Work
```bash
# Test-first development cycle
dbt test --select <model_name> --store-failures  # Confirm failures
dbt run --select <model_name>                    # Implement solution
dbt test --select <model_name>                   # Verify success
```