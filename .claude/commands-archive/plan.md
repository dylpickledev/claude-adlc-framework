---
name: plan
description: "Plan how to implement the specified data analytics feature. This is the second step in the Data-Driven Development lifecycle."
---

Plan how to implement the specified data analytics feature.

This is the second step in the Data-Driven Development lifecycle for analytics projects.

Given the implementation details provided as an argument, do this:

1. Run `scripts/setup-data-plan.sh --json` from the repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, PROJECTS_DIR, BRANCH. All future file paths must be absolute.

2. Read and analyze the feature specification to understand:
   - The business questions and data requirements
   - Data sources and refresh patterns
   - Cross-system integration needs (dbt → Snowflake → Tableau → Orchestra)
   - Data quality and governance requirements
   - Stakeholder consumption patterns

3. Read the data constitution at `/config/data-constitution.md` to understand data governance requirements.

4. Execute the implementation plan template:
   - Load `/templates/data-plan-template.md` (already copied to IMPL_PLAN path)
   - Set Input path to FEATURE_SPEC
   - Run the Execution Flow (main) function steps 1-8
   - The template is self-contained and executable
   - Follow error handling and gate checks as specified
   - Let the template guide artifact generation in $PROJECTS_DIR:
     * Phase 0 generates research.md (data sources, tool capabilities)
     * Phase 1 generates data-model.md, contracts/, quickstart.md
     * Phase 2 generates tasks.md (via /tasks command)
   - Incorporate user-provided technical details from arguments into Technical Context: {ARGS}
   - Update Progress Tracking as you complete each phase

5. **Data-Specific Research Areas**:
   - Data source schema validation and availability
   - Tool version compatibility (dbt, Snowflake, Tableau, Orchestra)
   - Performance benchmarks for expected data volumes
   - Integration patterns between selected data tools
   - Data governance and compliance requirements

6. **Cross-Tool Architecture Planning**:
   - Map data flow: Source → dbt → Snowflake → Tableau
   - Define sub-agent coordination points
   - Plan testing strategy across tool boundaries
   - Design monitoring and alerting approach

7. Verify execution completed:
   - Check Progress Tracking shows all phases complete
   - Ensure all required artifacts were generated
   - Confirm no ERROR states in execution
   - Validate data constitution compliance

8. Report results with branch name, file paths, generated artifacts, and sub-agent coordination plan.

Use absolute paths with the repository root for all file operations to avoid path issues.

**Sub-Agent Coordination**: This command prepares handoff instructions for:
- dbt-expert: Model design and testing strategy
- snowflake-expert: Schema design and optimization
- tableau-expert: Dashboard and data source planning  
- orchestra-expert: Pipeline orchestration and monitoring
- business-context: Stakeholder requirements and validation