# dbt Project Learning System - Implementation Plan

## Quick Summary

Enable dbt-expert to automatically learn about a user's specific dbt project during setup, ensuring all recommendations match the user's existing conventions, not generic best practices.

## Problem

**Every user has a unique dbt project** with:
- Custom naming (e.g., `stg_jde_prod__f4111` vs standard patterns)
- Specific macros, packages, testing strategies
- Project-specific known issues
- Particular dbt version/type (Core vs Cloud)

**Current state**: dbt-expert gives generic advice that often doesn't match user's actual project.

**Goal**: Make dbt-expert instantly aware of USER'S project specifics.

## Solution Overview

Three-phase system:
1. **Discovery**: During `/setup`, automatically analyze user's dbt project
2. **Profile**: Generate `.claude/memory/dbt-project-profile.yaml` with project context
3. **Integration**: dbt-expert loads profile before all tasks for project-aware recommendations

## Implementation Roadmap

### Week 1: Core Learning System

**Goal**: Basic project analysis and profile generation

#### Deliverables

1. **Project Analysis Script** (`scripts/analyze_dbt_project.py`)
   - Parse `dbt_project.yml` for metadata
   - Read `manifest.json` (if exists) for model inventory
   - Detect naming patterns from model names
   - Count materializations and layers
   - **Acceptance**: Successfully analyzes test project, outputs valid YAML

2. **Shell Wrapper** (`scripts/analyze-dbt-project.sh`)
   - Validates dbt project path
   - Calls Python analysis script
   - Handles errors gracefully
   - **Acceptance**: Can be called from command line, creates profile

3. **Profile Schema** (`.claude/memory/dbt-project-profile.yaml`)
   - Define complete YAML structure
   - Include metadata, conventions, materializations, testing
   - **Acceptance**: Valid YAML, human-readable, agent-parseable

4. **Setup Integration** (`.claude/commands/setup.md`)
   - Add dbt project discovery step after tool detection
   - Prompt for project path with auto-detection
   - Run analysis and show summary
   - **Acceptance**: Setup flow includes dbt learning, creates profile

5. **dbt-expert Update** (`.claude/agents/specialists/dbt-expert.md`)
   - Add "Load Project Profile" as step 0 in Memory Check Protocol
   - Define project-aware recommendation pattern
   - Add version compatibility checks
   - **Acceptance**: dbt-expert references profile in recommendations

#### Testing
- [ ] Test on 3 different dbt projects (Core + Cloud, various sizes)
- [ ] Validate profile accuracy against actual projects
- [ ] Verify dbt-expert uses profile in recommendations
- [ ] User test: Does setup feel natural? Is output clear?

### Week 2: Enhanced Analysis

**Goal**: Deeper project understanding

#### Deliverables

1. **Macro Analysis**
   - Scan `macros/` directory
   - Parse `packages.yml` for package dependencies
   - Identify commonly used macros
   - **Acceptance**: Profile includes custom + package macros

2. **Testing Pattern Detection**
   - Analyze generic test usage from manifest
   - Identify singular tests in `tests/` directory
   - Detect test coverage patterns
   - **Acceptance**: Profile shows testing strategy

3. **Semantic Layer Discovery**
   - Check for `semantic_models/` or `metrics/`
   - Count metrics and common dimensions
   - **Acceptance**: Profile indicates if semantic layer is used

4. **Source Analysis**
   - Extract sources from manifest
   - Count tables per source
   - Detect source naming patterns
   - **Acceptance**: Profile lists primary sources

#### Testing
- [ ] Validate macro detection on projects with dbt_utils, dbt_expectations
- [ ] Test semantic layer detection on dbt Cloud projects
- [ ] Verify source analysis accuracy

### Week 3: Continuous Learning

**Goal**: Profile improves over time

#### Deliverables

1. **Learning Capture Mechanism**
   - Define learning entry schema
   - Create append function for dbt-expert
   - **Acceptance**: dbt-expert can add learnings to profile

2. **Known Issues Database**
   - Template for documenting project-specific issues
   - Integration with error resolution workflow
   - **Acceptance**: Fixed errors get added to known_issues

3. **Pattern Evolution Tracking**
   - Detect when conventions change
   - Suggest profile updates when patterns diverge
   - **Acceptance**: Profile stays current with project changes

4. **Re-analysis Capability**
   - Allow users to re-run `/setup` for dbt
   - Update profile with new findings
   - Preserve manual learnings
   - **Acceptance**: Re-running setup updates profile without losing data

#### Testing
- [ ] dbt-expert successfully appends learnings after task completion
- [ ] Known issues section grows with resolved errors
- [ ] Re-analysis preserves custom learnings

### Week 4: Documentation & Polish

**Goal**: Production-ready release

#### Deliverables

1. **User Documentation**
   - Update `SETUP.md` with dbt project learning section
   - Create troubleshooting guide for analysis failures
   - Document profile schema for power users
   - **Acceptance**: Users understand what's happening and why

2. **Example Profiles**
   - Create sample profiles from test projects
   - Annotate with explanations
   - **Acceptance**: Users can see what a good profile looks like

3. **Error Handling**
   - Graceful fallbacks when manifest missing
   - Clear error messages for invalid projects
   - Partial profile generation if some analysis fails
   - **Acceptance**: Failures are informative, not cryptic

4. **Performance Optimization**
   - Ensure analysis completes in <30 seconds for large projects
   - Cache analysis results
   - **Acceptance**: Fast enough for setup flow

5. **Release Notes**
   - Announce feature to users
   - Highlight benefits
   - Provide before/after examples
   - **Acceptance**: Users excited to try it

#### Testing
- [ ] Full end-to-end test with fresh setup
- [ ] User acceptance testing with 3-5 real users
- [ ] Documentation review for clarity
- [ ] Performance test on large project (2000+ models)

## Metrics for Success

### Quantitative
- **Accuracy**: 90% of detected patterns match actual project conventions
- **Speed**: Analysis completes in <30 seconds for most projects
- **Coverage**: Profile captures 80%+ of project-specific patterns
- **Adoption**: 80% of users complete dbt project learning during setup

### Qualitative
- **User Feedback**: "dbt-expert gets my project" vs "doesn't understand my setup"
- **Correction Rate**: Fewer user corrections to dbt-expert recommendations
- **Trust**: Users rely on dbt-expert for project-specific advice

## Risks & Mitigation

### Risk 1: Analysis Takes Too Long
**Mitigation**:
- Start with quick analysis (project structure only)
- Deep analysis runs in background if needed
- Cache results, reuse across sessions

### Risk 2: Profile Inaccurate
**Mitigation**:
- Test on diverse projects before release
- Provide user feedback mechanism
- Allow manual profile editing

### Risk 3: Adds Complexity to Setup
**Mitigation**:
- Make it optional (skip if user declines)
- Show value immediately (profile summary)
- Keep UI simple (progress bar, clear output)

### Risk 4: Different dbt Versions/Structures
**Mitigation**:
- Graceful degradation (partial profiles OK)
- Clear error messages for unsupported versions
- Fallback to manual configuration

## Dependencies

### Required
- Python 3.8+ (for analysis script)
- PyYAML library (for YAML parsing)
- Access to user's dbt project files

### Optional
- `manifest.json` (for detailed analysis - generated by `dbt compile`)
- dbt-mcp access (for live project queries)

## Timeline

| Week | Focus | Key Deliverables | Gate |
|------|-------|------------------|------|
| 1 | Core Learning | Analysis scripts, schema, integration | Working prototype |
| 2 | Enhanced Analysis | Macros, testing, semantic layer | Comprehensive profiles |
| 3 | Continuous Learning | Learning capture, re-analysis | Self-improving system |
| 4 | Documentation & Polish | Docs, examples, release notes | Production ready |

## Launch Checklist

- [ ] All code complete and tested
- [ ] Documentation written and reviewed
- [ ] User testing completed with positive feedback
- [ ] Performance validated on large projects
- [ ] Error handling comprehensive
- [ ] Example profiles created
- [ ] Release notes written
- [ ] Team aligned on launch
- [ ] Monitoring plan in place
- [ ] Rollback plan documented

## Post-Launch

### Week 5-6: Monitor & Iterate
- Collect user feedback
- Fix bugs and edge cases
- Optimize performance
- Enhance documentation based on questions

### Week 7-8: Advanced Features
- Multi-project support
- Team profile sharing
- Pattern validation scoring
- Migration assistance (dbt version upgrades)

---

## Quick Start for Developers

```bash
# 1. Create feature branch
git checkout -b feature/dbt-project-learning

# 2. Implement core analysis
python3 scripts/analyze_dbt_project.py <test_project> .claude/memory/dbt-project-profile.yaml

# 3. Test profile generation
cat .claude/memory/dbt-project-profile.yaml

# 4. Integrate with setup
# Edit .claude/commands/setup.md

# 5. Update dbt-expert
# Edit .claude/agents/specialists/dbt-expert.md

# 6. Test end-to-end
claude /setup
# Follow prompts, analyze project
# Verify profile created
# Ask dbt-expert a question, check it uses profile
```

---

*Transform dbt-expert from generic consultant → YOUR project's specialist in ~4 weeks.*
