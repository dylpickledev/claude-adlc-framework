MISSION Turn rough project ideas into well-defined, structured projects with proper directory organization and clear objectives.

PROTOCOL
0 IDEATION PHASE
   - Apply ideate.md protocol to clarify scope, deliverables, and success criteria
   - Determine project type: feature, fix, research, refactor, docs
   - Confirm this needs project structure (vs simple task execution)

1 PROJECT SCOPING
   Ask clarifying questions about:
   - **Cross-repository impact**: Does this span multiple repos (dbt, snowflake, tableau, etc.)?
   - **Timeline**: Multi-day effort or quick task?
   - **Collaboration**: Will others contribute or review?
   - **Knowledge preservation**: Will findings benefit future work?
   
2 PROJECT TYPE VALIDATION
   Confirm project type and naming:
   - **feature/**: New functionality or enhancements
   - **fix/**: Bug fixes or error resolution  
   - **research/**: Investigation or analysis work
   - **refactor/**: Code improvements or reorganization
   - **docs/**: Documentation creation or updates

3 ECHO CHECK 
   Reply with: **"PROJECT: [type]-[description] | SCOPE: [key deliverable] | CONSTRAINT: [hardest challenge]"**
   End with: **✅ INITIALIZE PROJECT / ❌ REVISE SCOPE / ⚫ SIMPLE TASK INSTEAD**. WAIT.

4 PROJECT INITIALIZATION (if ✅)
   - Execute `./scripts/work-init.sh [type] "[description]"`
   - Update `projects/active/[project-name]/spec.md` with detailed requirements from ideation:
     * Specific end goals and success criteria
     * Implementation plan with phases
     * Technical requirements and constraints
     * Acceptance criteria and risk assessment
   - Initialize `projects/active/[project-name]/context.md` with current state
   - Create git branch matching project name
   - Confirm project structure is ready for work

5 SPECIFICATION DEVELOPMENT
   Based on ideation findings, populate spec.md with:
   - **End Goal**: Clear, measurable outcomes from ideation
   - **Success Criteria**: Specific metrics for completion
   - **Implementation Plan**: Step-by-step approach with phases
   - **Technical Requirements**: Systems, tools, dependencies
   - **Risk Assessment**: Potential blockers and mitigations
   - **Timeline Estimate**: Realistic effort estimation

6 AGENT ASSIGNMENT & COORDINATION
   - Identify which sub-agents will contribute based on technical requirements
   - Create `projects/active/[project-name]/tasks/current-task.md` with agent assignments
   - Brief relevant sub-agents on project context from spec.md
   - Establish communication patterns: agents read spec.md, write to tasks/

⚫ SIMPLE TASK PATH (if selected in step 3)
   - Use standard TodoWrite for task tracking
   - Execute work directly without project structure
   - For quick tasks, bug fixes, or single-file changes

USAGE EXAMPLES:
- "I want to optimize our Snowflake costs" → research/snowflake-cost-optimization
- "Dashboard loading is slow" → fix/tableau-dashboard-performance  
- "Need new customer metrics" → feature/customer-analytics-metrics
- "Quick typo fix in README" → ⚫ SIMPLE TASK

Respond once with: **"Ready—what project do you want to start?"**