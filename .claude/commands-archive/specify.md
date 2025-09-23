---
name: specify
description: "Start a new data analytics feature by creating a specification and feature branch. This is the first step in the Data-Driven Development lifecycle."
---

Start a new data analytics feature by creating a specification and feature branch.

This is the first step in the Data-Driven Development lifecycle for analytics projects.

Given the feature description provided as an argument, do this:

1. Run the script `scripts/create-new-project.sh --json "{ARGS}"` from repo root and parse its JSON output for BRANCH_NAME and SPEC_FILE. All file paths must be absolute.
2. Load `templates/data-spec-template.md` to understand required sections for data projects.
3. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.
4. Focus on data-specific requirements:
   - Identify data sources, business metrics, and stakeholder needs
   - Define data quality requirements and business rules
   - Map cross-system integration needs (dbt, Snowflake, Tableau, Orchestra)
   - Specify data governance and compliance requirements
5. Mark any unclear business logic, data sources, or requirements with [NEEDS CLARIFICATION: specific question]
6. Report completion with branch name, spec file path, and readiness for the /plan phase.

Note: The script creates and checks out the new project branch and initializes the spec file before writing.

**Data Analytics Focus Areas**:
- Business questions and metrics to answer
- Data source systems and refresh requirements  
- User personas and data consumption patterns
- Data quality thresholds and validation needs
- Cross-tool workflow requirements (pipeline → warehouse → visualization)