---
name: tasks
description: "Break down the data analytics plan into executable tasks with sub-agent coordination. This is the third step in the Data-Driven Development lifecycle."
---

Break down the data analytics plan into executable tasks with sub-agent coordination.

This is the third step in the Data-Driven Development lifecycle for analytics projects.

Given the context provided as an argument, do this:

1. Run `scripts/check-data-task-prerequisites.sh --json` from repo root and parse PROJECT_DIR and AVAILABLE_DOCS list. All paths must be absolute.

2. Load and analyze available design documents:
   - Always read plan.md for data stack and tool selection
   - IF EXISTS: Read data-model.md for entities and metrics
   - IF EXISTS: Read contracts/ for data contracts and APIs
   - IF EXISTS: Read research.md for technical decisions
   - IF EXISTS: Read quickstart.md for test scenarios

   Note: Data projects typically have:
   - dbt projects have data-model.md and contracts/
   - Dashboard projects have visualization contracts
   - Pipeline projects focus on orchestration contracts
   - Generate tasks based on what's available

3. Generate tasks following the data analytics template:
   - Use `/templates/data-tasks-template.md` as the base
   - Replace example tasks with actual tasks based on:
     * **Setup tasks**: Tool configs, database schemas, permissions
     * **Data Foundation tasks [P]**: Source validation, staging models, raw schemas
     * **Business Logic tasks**: Intermediate models, calculations, marts
     * **Integration tasks**: Cross-tool coordination, end-to-end testing
     * **Deployment tasks**: Production setup, user training, go-live

4. **Data-Specific Task Generation Rules**:
   - Each data source → source validation task marked [P]
   - Each dbt model layer → separate implementation tasks (staging → intermediate → marts)
   - Each dashboard → visualization task with data source dependency
   - Each pipeline → orchestration task with monitoring
   - Each data contract → integration test marked [P]
   - Different tools = can be parallel [P]
   - Same dbt models = sequential (no [P])

5. **Sub-Agent Task Assignment**:
   - **dbt-expert**: All dbt model tasks, data quality tests
   - **snowflake-expert**: Schema setup, query optimization, permissions
   - **tableau-expert**: Dashboard creation, data source optimization
   - **orchestra-expert**: Pipeline setup, monitoring, failure handling
   - **business-context**: Stakeholder validation, user training

6. Order tasks by data pipeline dependencies:
   - Setup before everything (schemas, permissions, configs)
   - Data quality tests before transformations (TDD for data)
   - Staging before intermediate before marts
   - Data models before dashboards
   - Individual tool tasks before integration
   - Integration before deployment

7. Include parallel execution examples:
   - Group [P] tasks by tool boundaries
   - Show actual sub-agent Task commands
   - Map critical integration points

8. Create PROJECT_DIR/tasks.md with:
   - Correct feature name from implementation plan
   - Numbered tasks (T001, T002, etc.) with sub-agent assignments
   - Clear file paths and data dependencies
   - Cross-tool integration notes
   - Parallel execution guidance with tool coordination

Context for task generation: {ARGS}

**Critical Integration Points to Include**:
- dbt staging → intermediate handoff
- dbt marts → Tableau data sources
- Snowflake optimization → dashboard performance
- Orchestra scheduling → dbt execution
- Data quality monitoring across all tools

The tasks.md should be immediately executable by sub-agents - each task must specify the responsible expert and include enough context for autonomous execution within the da-agent-hub framework.