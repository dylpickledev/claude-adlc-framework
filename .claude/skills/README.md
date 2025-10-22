# DA Agent Hub Skills Catalog

**Purpose**: Reusable workflow automation for Analytics Development Lifecycle

**Version**: 2.0.0
**Last Updated**: 2025-10-22

---

## What are Skills?

**Skills** are reusable, procedural workflows that automate repetitive tasks through organized folders containing instructions, scripts, and templates. Skills complement the agent system:

- **Skills**: "HOW to execute workflows" (procedural automation)
- **Agents**: "WHO to consult for expertise" (domain knowledge + MCP tools)
- **Patterns**: "WHAT solutions work" (proven approaches)

---

## Quick Start

### Using Skills

```bash
# Skills are invoked automatically by Claude based on your request

"Set up new project for customer-dashboard"
→ Invokes: project-setup skill

"Generate PR description"
→ Invokes: pr-description-generator skill

"Create dbt staging model for orders"
→ Invokes: dbt-model-scaffolder skill
```

### Finding Skills

Browse this catalog by category or search for keywords in descriptions.

---

## Skill Categories

### 1. Project Management Skills
- **project-setup** - Initialize ADLC project structure
- **pr-description-generator** - Generate comprehensive PR descriptions
- **documentation-validator** - Validate documentation completeness

### 2. dbt Universal Skills (Work on Core AND Cloud)
- **dbt-model-scaffolder** - Generate dbt model boilerplate
- **dbt-test-suite-generator** - Generate comprehensive test YAML
- **dbt-incremental-strategy-advisor** - Recommend optimal incremental strategy

### 3. dbt Core Skills (Core ONLY)
- **dbt-core-local-runner** - Run dbt commands locally
- **dbt-core-docs-generator** - Generate and serve docs
- **dbt-core-model-analyzer** - Analyze models via file system

### 4. dbt Cloud Skills (Cloud ONLY)
- **dbt-cloud-job-monitor** - Monitor job runs (read-only)
- **dbt-cloud-semantic-layer-explorer** - Explore Semantic Layer metrics
- **dbt-cloud-discovery-navigator** - Navigate models via Discovery API

---

## Skills Library

### Project Management

#### project-setup
**Platform**: Universal (all ADLC projects)
**Version**: 1.0.0

Initialize new ADLC project with standard directory structure, documentation templates, and git branch.

**Saves**: 10-15 minutes per project setup
**Frequency**: 2-4x per month

**Trigger Phrases**:
- "Set up new project for [name]"
- "Initialize project structure"
- "Create new ADLC project"

**Outputs**:
- `projects/active/{project-name}/README.md`
- `projects/active/{project-name}/spec.md`
- `projects/active/{project-name}/context.md`
- `projects/active/{project-name}/tasks/current-task.md`
- Git branch: `feature/{project-name}`

---

#### pr-description-generator
**Platform**: Universal (all git projects)
**Version**: 1.0.0

Generate comprehensive PR descriptions from project context and git changes.

**Saves**: 5-10 minutes per PR
**Frequency**: Every PR (10-20x per month)

**Trigger Phrases**:
- "Generate PR description"
- "Create pull request description"
- "What should I put in the PR description?"

**Outputs**:
- Structured PR description with summary, files changed, test plan, quality checklist
- Co-authored-by Claude footer

---

#### documentation-validator
**Platform**: Universal (all ADLC projects)
**Version**: 1.0.0

Validate documentation completeness before project closure.

**Saves**: 10-15 minutes
**Frequency**: Every project completion
**Used by**: `/complete` command

**Checks**:
- Required files exist (README, spec, context, tasks)
- Required sections present
- Internal links work
- No placeholder content ("TBD")

**Outputs**:
- Validation report with pass/fail/warnings
- Recommendations for fixes

---

### dbt Universal Skills

#### dbt-model-scaffolder
**Platform**: dbt Core AND dbt Cloud
**Version**: 2.0.0 (Enhanced with version awareness + MCP integration)

Generate dbt model boilerplate with tests, documentation, and best practices.

**Saves**: 15-20 minutes per model
**Frequency**: 5-10x per month

**Tech Requirements**:
- dbt version: 1.0+ (basic), 1.8+ (unit tests), 1.9+ (microbatch)
- Adapters: All (Snowflake, BigQuery, Redshift, etc.)

**Features**:
- ✅ Version-aware generation (1.8+ unit tests, 1.9+ microbatch)
- ✅ MCP-enhanced (uses Discovery API if available)
- ✅ Semantic Layer integration (if configured)
- ✅ Adapter-specific optimizations
- ✅ Layer-specific templates (staging, intermediate, mart)

**Trigger Phrases**:
- "Create new dbt model [name]"
- "Scaffold dbt model"
- "Generate dbt staging/intermediate/mart model"

**Workflow**:
1. Detect dbt platform (Core vs Cloud)
2. Detect dbt version (for feature support)
3. Check project size (if Cloud + MCP available)
4. Check Semantic Layer (if Cloud Team/Enterprise)
5. Ask for model details (name, layer, description)
6. Generate model SQL with appropriate template
7. Generate schema.yml with tests
8. Add version-specific features (unit tests, microbatch)

**Outputs**:
- `models/{layer}/{model_name}.sql`
- `models/{layer}/schema.yml` (created or updated)

---

#### dbt-test-suite-generator
**Platform**: dbt Core AND dbt Cloud
**Version**: 2.0.0

Generate comprehensive test YAML based on model layer and version.

**Saves**: 10-15 minutes per model
**Frequency**: 5-10x per month

**Tech Requirements**:
- dbt version: 1.0+ (data tests), 1.8+ (unit tests), 1.9+ (documented tests)
- MCP: Optional (enhances column detection)

**Features**:
- ✅ Layer-appropriate test generation
- ✅ Version-aware (unit tests for v1.8+)
- ✅ MCP-enhanced column detection (if available)
- ✅ Relationship test inference from model dependencies

**Trigger Phrases**:
- "Generate tests for model [name]"
- "Create test suite"
- "Add dbt tests to [model]"

**Workflow**:
1. Detect dbt version
2. Read model SQL (or use MCP get_model_details)
3. Identify columns and data types
4. Generate layer-appropriate tests:
   - **Staging**: unique, not_null on PK, relationships to source
   - **Intermediate**: grain tests, referential integrity
   - **Mart**: full data quality suite
5. Add unit tests (if v1.8+)
6. Create/update schema.yml

**Outputs**:
- Updated `models/{layer}/schema.yml` with comprehensive tests

---

#### dbt-incremental-strategy-advisor
**Platform**: dbt Core AND dbt Cloud
**Version**: 2.0.0

Recommend optimal incremental strategy based on data patterns and dbt version.

**Saves**: 20-25 minutes per optimization
**Frequency**: 1-2x per month

**Tech Requirements**:
- dbt version: 1.0+ (basic incremental), 1.9+ (microbatch)
- Adapters: Strategy recommendations vary by adapter

**Features**:
- ✅ Version-aware (microbatch for v1.9+)
- ✅ Adapter-specific strategies
- ✅ Performance estimation
- ✅ Deduplication pattern recommendations

**Trigger Phrases**:
- "Recommend incremental strategy for [model]"
- "Optimize [model] for large dataset"
- "Convert [model] to incremental"

**Workflow**:
1. Analyze model SQL and data patterns
2. Check dbt version (1.9+ enables microbatch)
3. Check adapter (Snowflake, BigQuery, Redshift)
4. Recommend strategy:
   - v1.9+ event data → **microbatch**
   - v1.0-1.8 updates → **merge**
   - v1.0-1.8 append-only → **append**
   - Adapter-specific → **delete+insert** or **insert_overwrite**
5. Generate config block with strategy
6. Add deduplication logic if needed
7. Estimate performance improvement

**Outputs**:
- Updated model SQL with incremental config
- Performance estimates (before/after)
- Testing recommendations

---

### dbt Core Skills

#### dbt-core-local-runner
**Platform**: dbt Core ONLY
**Version**: 1.0.0

Run dbt commands locally and display results.

**Saves**: 5 minutes per run (convenience)
**Frequency**: 10-20x per day

**Tech Requirements**:
- dbt Core with local CLI access
- STOPS if dbt Cloud detected

**Trigger Phrases**:
- "Run dbt model [name]"
- "Test model [name]"
- "Build [model]"

**Workflow**:
1. Validate platform is dbt Core
2. Execute dbt command: `dbt run --select {model}`
3. Capture and display output
4. Show any errors with context

**Alternative for Cloud**: Use dbt Cloud IDE 'Preview' button

---

#### dbt-core-docs-generator
**Platform**: dbt Core ONLY
**Version**: 1.0.0

Generate and serve dbt documentation locally.

**Saves**: 3-5 minutes
**Frequency**: As needed for documentation review

**Tech Requirements**:
- dbt Core with local CLI
- STOPS if dbt Cloud detected

**Trigger Phrases**:
- "Generate dbt docs"
- "Serve documentation"
- "View dbt docs"

**Workflow**:
1. Validate platform is dbt Core
2. Run: `dbt docs generate`
3. Run: `dbt docs serve --port 8080`
4. Open browser to http://localhost:8080

**Alternative for Cloud**: View docs in dbt Cloud UI under Documentation tab

---

#### dbt-core-model-analyzer
**Platform**: dbt Core ONLY
**Version**: 1.0.0

Analyze dbt models via file system and local CLI.

**Saves**: 5-10 minutes per analysis
**Frequency**: 2-3x per week

**Tech Requirements**:
- dbt Core with local CLI
- Direct file system access

**Trigger Phrases**:
- "Analyze model [name]"
- "Show model details [name]"
- "What does [model] do?"

**Workflow**:
1. Validate platform is dbt Core
2. Read: `models/{model_name}.sql`
3. Parse: `models/schema.yml` for tests/docs
4. Run: `dbt compile --select {model}`
5. Read compiled SQL from `target/compiled/`
6. Display model analysis

**Alternative for Cloud**: Use dbt-cloud-discovery-navigator (MCP-powered)

---

### dbt Cloud Skills

#### dbt-cloud-job-monitor
**Platform**: dbt Cloud ONLY
**Version**: 1.0.0

Monitor dbt Cloud job runs (READ-ONLY observability).

**Saves**: 10-15 minutes per investigation
**Frequency**: 2-4x per week

**Tech Requirements**:
- dbt Cloud (any tier)
- MCP Admin API tools
- STOPS if dbt Core detected

**Features**:
- ✅ Read-only (no job execution)
- ✅ Job history analysis
- ✅ Failure investigation
- ✅ Performance insights
- ❌ NO job triggering or automation

**Trigger Phrases**:
- "Show recent job runs"
- "Check job status"
- "Investigate failed job [run_id]"

**Workflow**:
1. Validate platform is dbt Cloud
2. MCP: `list_jobs_runs(limit=20)`
3. Display recent runs with status, duration
4. If failures: `get_job_run_details(run_id)`
5. Download artifacts if needed
6. Show error context
7. NO retry or trigger options

**User Control**: All job execution remains manual in dbt Cloud UI

**Alternative for Core**: dbt Core doesn't have jobs - use dbt-core-local-runner

---

#### dbt-cloud-semantic-layer-explorer
**Platform**: dbt Cloud Team/Enterprise ONLY
**Version**: 1.0.0

Explore and query Semantic Layer metrics.

**Saves**: 10-15 minutes per metric exploration
**Frequency**: 2-3x per week (if using Semantic Layer)

**Tech Requirements**:
- dbt Cloud Team or Enterprise tier
- Semantic Layer enabled
- Metrics defined in project
- MCP Semantic Layer tools
- STOPS if Core, Developer tier, or no metrics

**Features**:
- ✅ Metric catalog browsing
- ✅ Dimension exploration
- ✅ Metric query preview
- ✅ Compiled SQL viewing

**Trigger Phrases**:
- "Show available metrics"
- "Explore Semantic Layer"
- "Query metric [name]"

**Workflow**:
1. Validate dbt Cloud Team/Enterprise
2. Detect Semantic Layer availability
3. MCP: `list_metrics()`
4. Display metric catalog
5. User selects metric
6. MCP: `get_dimensions(metric)`
7. Show slicing options
8. Optional: `query_metrics()` for preview
9. Show compiled SQL

**Alternative for Core**: Define metrics in YAML locally (no query API)

---

#### dbt-cloud-discovery-navigator
**Platform**: dbt Cloud ONLY
**Version**: 1.0.0

Navigate dbt models using Discovery API (project-size-aware).

**Saves**: 5-10 minutes per model exploration
**Frequency**: 5-10x per week

**Tech Requirements**:
- dbt Cloud (any tier)
- MCP Discovery API tools
- Project size detection
- STOPS if dbt Core detected

**Features**:
- ✅ Project-size-aware (avoids token overflow)
- ✅ Model details via Discovery API
- ✅ Dependency analysis (parents/children)
- ✅ Compiled SQL viewing

**Trigger Phrases**:
- "Show model details [name]"
- "Analyze model [name]"
- "What models depend on [name]?"

**Workflow**:
1. Validate platform is dbt Cloud
2. Detect project size
3. IF LARGE project:
   - Ask user for specific model name
   - Use targeted MCP calls only
4. IF SMALL/MEDIUM project:
   - Can offer broader discovery
5. MCP: `get_model_details(model_name)`
6. MCP: `get_model_parents(model_name)`
7. MCP: `get_model_children(model_name)`
8. Display comprehensive model analysis

**Alternative for Core**: Use dbt-core-model-analyzer (file-based)

---

## Detection Libraries (Reusable Components)

### platform-detector.md
Detects dbt Core vs dbt Cloud to ensure correct workflows.

**Location**: `.claude/skills/lib/platform-detector.md`

### mcp-project-size-detector.md
Detects project size to avoid MCP token overflow on large projects.

**Location**: `.claude/skills/lib/mcp-project-size-detector.md`

### semantic-layer-detector.md
Detects Semantic Layer availability to avoid unnecessary MCP calls.

**Location**: `.claude/skills/lib/semantic-layer-detector.md`

---

## Skill Development Guidelines

### Creating New Skills

1. **Copy appropriate template**:
   - Universal skill → Use existing universal skill as template
   - Platform-specific → Use platform-specific skill as template

2. **Add detection logic** (Step 0 in every skill):
   - Platform detection (Core vs Cloud)
   - Version detection (feature availability)
   - Project size detection (if using MCP inventory tools)
   - Capability detection (Semantic Layer, etc.)

3. **Implement graceful degradation**:
   - If feature unavailable → Show helpful error with alternatives
   - If MCP unavailable → Fall back to file system/CLI
   - Never fail completely → Always provide value

4. **Document requirements**:
   - Platform requirements
   - Version requirements
   - MCP tool requirements
   - Tier requirements (Cloud only)

5. **Test on both platforms** (if universal):
   - Verify works on dbt Core
   - Verify works on dbt Cloud
   - Test with different versions

---

## Best Practices

### Platform Separation

**DO**:
- ✅ Create separate skills for different platforms when workflows differ
- ✅ Detect platform early (Step 0)
- ✅ Show clear error messages with alternatives
- ✅ Document platform requirements in frontmatter

**DON'T**:
- ❌ Mix Core and Cloud workflows in one skill
- ❌ Assume platform without detection
- ❌ Make Cloud API calls on Core projects
- ❌ Make local CLI calls on Cloud projects

### MCP Usage

**DO**:
- ✅ Detect project size before inventory operations
- ✅ Use targeted MCP calls on large projects
- ✅ Detect capabilities before using (Semantic Layer, Fusion)
- ✅ Provide fallbacks when MCP unavailable

**DON'T**:
- ❌ Use `get_all_models()` on large projects (token overflow)
- ❌ Call Semantic Layer tools without detecting availability
- ❌ Assume MCP is always configured
- ❌ Make unnecessary MCP calls

### User Experience

**DO**:
- ✅ Show detection results to user
- ✅ Explain why features unavailable
- ✅ Suggest alternatives for their setup
- ✅ Save detection results to avoid re-checking

**DON'T**:
- ❌ Silently fail when platform mismatch
- ❌ Show features that aren't available
- ❌ Make user guess what went wrong
- ❌ Repeat detection every time

---

## Troubleshooting

### "Platform Mismatch" Errors

**Problem**: Skill requires different platform than detected

**Solution**:
1. Verify platform detection is correct: Check `.claude/dbt-platform-config.json`
2. If wrong, delete config and re-detect
3. Use alternative skill for your platform (shown in error message)

### "Project Too Large" Errors

**Problem**: MCP inventory tools failing on large projects

**Solution**:
1. Check project size: `.claude/dbt-mcp-config.json`
2. Use targeted model names instead of inventory operations
3. Use `dbt list --select` for discovery
4. Skills will automatically adjust for large projects

### "Semantic Layer Not Available" Errors

**Problem**: Trying to use Semantic Layer features without proper setup

**Solution**:
1. Check Cloud tier (requires Team or Enterprise)
2. Verify Semantic Layer enabled in environment
3. Confirm metrics defined in project
4. Use alternative metric workflows for your tier

---

## Contributing

To add a new skill:

1. Create skill folder: `.claude/skills/{skill-name}/`
2. Create `skill.md` with frontmatter and workflow
3. Add templates if needed: `.claude/skills/{skill-name}/templates/`
4. Update this catalog
5. Test on appropriate platforms
6. Submit PR

---

**Version**: 2.0.0
**Last Updated**: 2025-10-22
**Maintainer**: ADLC Platform Team
