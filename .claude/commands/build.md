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
- **Option A - From existing idea**: Searches `ideas/organized/` and `ideas/pipeline/`, promotes and archives idea
- **Option B - Ad-hoc creation**: If no matching idea found, creates project directly from provided description
- **Creates project structure**: Integrates with `work-init.sh` for full project setup
- **Idea management**: Archives source idea if found, or creates retrospective idea record if needed
- **Provides development guidance**: Next steps for implementation

## Claude Instructions

When user runs `/build [idea-name-or-description]`:

1. **Search for existing idea**: Look in `ideas/organized/` and `ideas/pipeline/` for matching idea
2. **Handle creation path**:
   - **If idea found**: Execute `./scripts/build.sh [idea-name]` (formal process)
   - **If no idea found**: Use `./scripts/work-init.sh` directly with description as project name
3. **Manage idea lifecycle**:
   - **Existing idea**: Archive source idea with project reference
   - **Ad-hoc creation**: Optionally create retrospective idea record in archive
4. **Validate structure**: Confirm project directory and files created properly
5. **Guide development**: Explain specialist agent coordination and next steps

### Response Format

#### Option A: From Existing Idea
```
🔧 Building project for idea: [idea-name]
📋 Found idea in organized: [path]
📦 Promoting idea to pipeline...
🏗️ Creating project structure...
✅ Project structure created
📚 Properly archiving source idea...
   ✅ Moved: ideas/[location]/[idea-file] → ideas/archive/
   ✅ Updated with project reference and implementation status

✅ Idea successfully built into project!
📁 Project location: projects/active/[project-name]/
```

#### Option B: Ad-hoc Creation
```
🔧 Building project: [description]
🔍 No existing idea found - creating project directly
🏗️ Creating project structure via work-init.sh...
✅ Project structure created
📝 Creating retrospective idea record (optional)...

✅ Project created successfully!
📁 Project location: projects/active/[project-name]/
💡 Note: No source idea - ad-hoc creation
```

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

## Specialist Agent Coordination
The build process enables access to:
- **dbt-expert**: SQL transformations, model optimization, test development
- **snowflake-expert**: Query performance, cost analysis, warehouse optimization
- **tableau-expert**: Dashboard development, report model analysis
- **business-context**: Requirements gathering, stakeholder alignment
- **da-architect**: System design, data flow analysis, strategic decisions
- **orchestra-expert**: Workflow orchestration leadership
- **documentation-expert**: Consistent standards across all outputs

## Examples

### Example 1: Analytics Model
```bash
claude /build customer-churn-prediction
# → Creates: projects/active/feature-customer-churn-prediction/
```

### Example 2: Dashboard Project
```bash
claude /build executive-kpi-dashboard
# → Creates: projects/active/feature-executive-kpi-dashboard/
```

### Example 3: Infrastructure Optimization
```bash
claude /build snowflake-cost-optimization
# → Creates: projects/active/feature-snowflake-cost-optimization/
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