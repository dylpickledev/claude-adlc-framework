# Evaluator-Optimizer Quality Workflow

## Purpose
Iterative quality improvement through systematic feedback loops. Based on Anthropic's Claude Cookbook Evaluator-Optimizer pattern.

**When to Use**: Any task where quality and correctness are critical and iteration can improve outcomes.

---

## Pattern Overview

```
┌─────────────┐
│  Generator  │ Create initial output
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Evaluator  │ Assess quality, identify issues
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Optimizer  │ Improve based on feedback
└──────┬──────┘
       │
       ▼
  Quality >= 8.5/10? ─── NO ──> Loop back to Evaluator
       │
      YES
       │
       ▼
┌─────────────┐
│   Complete  │ Deliver high-quality output
└─────────────┘
```

---

## When to Use This Workflow

### HIGH PRIORITY (Always Use)
- **Code review iterations** - Multiple rounds of improvement
- **Production deployments** - Zero-defect requirement
- **Architecture decisions** - Long-term impact, must be right
- **Documentation for stakeholders** - Clarity and completeness critical
- **Dashboard/BI design** - User experience and accuracy paramount

### MEDIUM PRIORITY (Use When Time Permits)
- **Complex SQL queries** - Performance and correctness important
- **Data model design** - Quality impacts downstream consumers
- **Integration code** - Cross-system reliability needed
- **Technical specifications** - Accuracy prevents misunderstandings

### LOW PRIORITY (Optional)
- **Routine updates** - Low risk, well-understood patterns
- **Internal documentation** - Lower stakes
- **Exploratory analysis** - Iteration happens naturally

---

## The Process

### Step 1: Generate Initial Output

**Who**: Role agent or Specialist (depending on task)

**Deliverable**: First draft/version of the solution

**Example**:
```markdown
Task: Create dbt model for customer lifetime value calculation

Initial Output:
- dbt SQL model: models/marts/analytics/customer_ltv.sql
- Documentation: models/marts/analytics/schema.yml
- Tests: 3 data tests defined
```

---

### Step 2: Evaluate Quality

**Who**: QA Engineer role OR domain specialist (depending on what's being evaluated)

**Evaluation Format**:

```markdown
<evaluation>
## Quality Assessment

### Completeness Score: [1-10]
**Score**: [X/10]
**Assessment**: Does it address all requirements?
- ✅ [Requirement 1]: Fully addressed
- ⚠️ [Requirement 2]: Partially addressed - [specific gap]
- ❌ [Requirement 3]: Missing - [what's missing]

### Correctness Score: [1-10]
**Score**: [X/10]
**Assessment**: Are there errors or inaccuracies?
- ✅ [Aspect 1]: Correct
- ❌ [Aspect 2]: Error found - [description]
- ⚠️ [Aspect 3]: Potential issue - [concern]

### Clarity Score: [1-10]
**Score**: [X/10]
**Assessment**: Is it easy to understand?
- ✅ [Aspect 1]: Clear and well-documented
- ⚠️ [Aspect 2]: Could be clearer - [suggestion]

### Performance Score: [1-10]
**Score**: [X/10]
**Assessment**: Does it meet performance needs?
- ✅ [Metric 1]: Meets target
- ❌ [Metric 2]: Below target - [measurement]

## Overall Score: [Average of above scores]

## Specific Issues Identified

1. **[Issue Category]**: [Detailed description]
   - **Location**: [Where in the code/doc/design]
   - **Impact**: [High/Medium/Low]
   - **Evidence**: [What shows this is an issue]

2. **[Issue Category]**: [Detailed description]
   - **Location**: [Where in the code/doc/design]
   - **Impact**: [High/Medium/Low]
   - **Evidence**: [What shows this is an issue]

## Improvement Recommendations

1. **[Recommendation]**: [Specific, actionable guidance]
   - **Why**: [Rationale]
   - **How**: [Implementation approach]
   - **Expected Improvement**: [What this fixes]

2. **[Recommendation]**: [Specific, actionable guidance]
   - **Why**: [Rationale]
   - **How**: [Implementation approach]
   - **Expected Improvement**: [What this fixes]

## Decision

**Meets Quality Threshold (8.5/10)?** [YES/NO]

- If YES → Proceed to final validation
- If NO → Proceed to optimization (Step 3)
</evaluation>
```

**Example Evaluation**:

```markdown
<evaluation>
## Quality Assessment

### Completeness Score: 7/10
- ✅ LTV calculation logic: Fully implemented
- ⚠️ Historical data handling: Partially addressed - doesn't handle customers with <6 months history
- ❌ Churn prediction integration: Missing - spec required this

### Correctness Score: 6/10
- ✅ SQL syntax: Correct
- ❌ Business logic: Revenue calculation doesn't account for refunds
- ❌ Date range: Using CURRENT_DATE instead of snapshot date for reproducibility

### Clarity Score: 8/10
- ✅ Column names: Clear and descriptive
- ✅ Documentation: Well-documented in schema.yml
- ⚠️ Complex CTE: "revenue_aggregation" CTE could use inline comments

### Performance Score: 5/10
- ❌ Missing indexes: No consideration for query performance
- ❌ Full table scan: Calculating from raw orders table (500M+ rows)
- ⚠️ Materialization: Using view instead of incremental

## Overall Score: 6.5/10

## Specific Issues Identified

1. **Business Logic Error - Refunds Not Handled**
   - **Location**: revenue_aggregation CTE, line 15-20
   - **Impact**: HIGH - LTV will be overstated by ~8% (average refund rate)
   - **Evidence**: SUM(order_amount) doesn't filter WHERE refund_date IS NULL

2. **Performance Issue - Full Table Scan**
   - **Location**: FROM raw.orders join
   - **Impact**: HIGH - Query takes 45 seconds, should be <5s
   - **Evidence**: EXPLAIN plan shows seq scan on 500M row table

3. **Reproducibility Issue - Dynamic Date**
   - **Location**: WHERE order_date <= CURRENT_DATE
   - **Impact**: MEDIUM - Results change daily, can't reproduce historical calculations
   - **Evidence**: dbt snapshot best practice requires fixed snapshot dates

## Improvement Recommendations

1. **Add Refund Handling**
   - **Why**: Business logic correctness
   - **How**: Add `AND refund_date IS NULL` to revenue calculation
   - **Expected Improvement**: Accurate LTV (+2 points correctness)

2. **Optimize Query Performance**
   - **Why**: 45s is unacceptable for dashboard refresh
   - **How**: Change to incremental materialization, add WHERE clause on indexed date column
   - **Expected Improvement**: <5s query time (+4 points performance)

3. **Use Snapshot Date for Reproducibility**
   - **Why**: Results must be reproducible for historical analysis
   - **How**: Use `{{ var('snapshot_date') }}` or dbt snapshot approach
   - **Expected Improvement**: Historical consistency (+1 point correctness)

## Decision

**Meets Quality Threshold (8.5/10)?** NO (6.5/10)

Proceed to optimization (Step 3) - critical issues must be addressed before production.
</evaluation>
```

---

### Step 3: Optimize Based on Feedback

**Who**: Same agent that created initial output (role agent or specialist)

**Process**:
1. Review evaluation carefully
2. Address each recommendation systematically
3. Implement improvements with validation
4. Document what changed and why

**Optimization Format**:

```markdown
<optimization>
## Changes Made (Iteration [N])

### Issue 1: [Issue description from evaluation]
**Fix Applied**:
[What you changed]

**Code/Design Change**:
```[language]
// Before
[old code/design]

// After
[new code/design]
```

**Validation**:
[How you verified the fix works]

**Expected Score Improvement**: [+X points]

### Issue 2: [Issue description]
**Fix Applied**: [What you changed]
**Validation**: [How verified]
**Expected Score Improvement**: [+X points]

## Self-Assessment After Changes

**Completeness**: [X/10] (was [Y/10]) - [what improved]
**Correctness**: [X/10] (was [Y/10]) - [what improved]
**Clarity**: [X/10] (was [Y/10]) - [what improved]
**Performance**: [X/10] (was [Y/10]) - [what improved]

**Estimated Overall**: [X/10] (was [Y/10])

## Ready for Re-Evaluation

Changes complete. Request re-evaluation from [evaluator agent].
</optimization>
```

---

### Step 4: Re-Evaluate

**Who**: Same evaluator (for consistency)

**Process**:
- Review optimized version
- Check if recommendations were addressed
- Assign new scores
- Identify any remaining issues
- Decide: meets threshold (8.5/10) OR needs another iteration

**If score >= 8.5/10**: Proceed to Step 5 (Final Validation)
**If score < 8.5/10**: Loop back to Step 3 (Optimizer)

**Maximum Iterations**: Usually 2-3 cycles achieves 8.5+/10

---

### Step 5: Final Validation

**Who**: User OR Project Manager role (for stakeholder-facing work)

**Validation Checklist**:
```markdown
## Final Quality Validation

- [ ] All evaluation criteria met (score >= 8.5/10)
- [ ] Original requirements fully addressed
- [ ] No critical issues remaining
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] Ready for production/delivery

**Approved by**: [Name/Role]
**Date**: [Date]
**Final Score**: [X/10]
```

---

## Usage Examples

### Example 1: Code Review

**Iteration 1**:
- Generator: Developer writes initial dbt model
- Evaluator: QA Engineer scores 6.5/10, finds business logic error + performance issues
- Optimizer: Developer fixes refund handling, adds incremental materialization
- Re-Evaluator: QA Engineer scores 8.2/10, finds remaining edge case

**Iteration 2**:
- Optimizer: Developer handles edge case (customers with <6 months history)
- Re-Evaluator: QA Engineer scores 9.1/10
- Final Validation: User approves for production

**Outcome**: High-quality code deployed, issues caught before production

---

### Example 2: Dashboard Design

**Iteration 1**:
- Generator: BI Developer creates Tableau dashboard
- Evaluator: Business Analyst scores 7.0/10, clarity issues for stakeholders
- Optimizer: BI Developer simplifies visualizations, adds explanatory text
- Re-Evaluator: Business Analyst scores 8.7/10

**Final Validation**: Stakeholder reviews and approves

**Outcome**: Dashboard meets user needs, no redesign required

---

### Example 3: Architecture Documentation

**Iteration 1**:
- Generator: Data Architect writes system design doc
- Evaluator: Documentation Expert scores 6.8/10, missing diagrams and examples
- Optimizer: Data Architect adds architecture diagrams, concrete examples
- Re-Evaluator: Documentation Expert scores 8.0/10, suggests one more clarification

**Iteration 2**:
- Optimizer: Adds clarifying section on failure modes
- Re-Evaluator: Documentation Expert scores 9.2/10

**Final Validation**: Engineering team reviews and approves

**Outcome**: Clear, comprehensive documentation for team

---

## Integration with Project Workflow

### During `/complete` Command

Add evaluation step before marking project complete:

```bash
# In scripts/finish.sh

echo "Running quality evaluation..."

# Prompt for self-evaluation
# If score < 8.5, recommend Evaluator-Optimizer workflow
# If score >= 8.5, proceed with project completion
```

### During Pull Request Creation

```markdown
## Quality Checklist (Evaluator-Optimizer)

- [ ] Initial implementation complete
- [ ] Evaluation performed (score: X/10)
- [ ] Optimization iteration(s) completed
- [ ] Final score >= 8.5/10
- [ ] All issues addressed

**Evaluator**: [Agent name]
**Final Score**: [X/10]
**Iterations**: [N]
```

---

## Quality Threshold Guidelines

### Score Ranges

**9.0-10.0** - Exceptional
- Production-ready, best-in-class quality
- Exceeds requirements
- Can be used as template/example

**8.5-8.9** - Excellent
- Production-ready, high quality
- Meets all requirements
- Minor improvements possible but not necessary

**7.0-8.4** - Good
- Needs optimization iteration
- Core requirements met, but issues exist
- Not yet production-ready

**5.0-6.9** - Fair
- Significant issues, multiple iterations needed
- Major gaps or errors
- Requires substantial rework

**< 5.0** - Poor
- Fundamental problems
- Consider starting over with different approach
- May need different agent or specialist consultation

---

## Success Metrics

Track effectiveness of Evaluator-Optimizer workflow:

```markdown
## Workflow Metrics (Updated Monthly)

**Total Uses**: [N]
**Average Initial Score**: [X.X/10]
**Average Final Score**: [X.X/10]
**Average Iterations**: [X.X]
**Success Rate** (>= 8.5 achieved): [XX%]

**Common Issues Found**:
1. [Issue type]: [XX%] of evaluations
2. [Issue type]: [XX%] of evaluations

**Most Improved Categories**:
1. [Category]: +[X.X] average improvement
2. [Category]: +[X.X] average improvement
```

---

## Best Practices

### For Generators
- ✅ Do your best work first iteration (don't rely on evaluator to catch obvious issues)
- ✅ Self-evaluate before requesting formal evaluation
- ✅ Document trade-offs and decisions made
- ✅ Test/validate before submitting for evaluation

### For Evaluators
- ✅ Be specific with issues (location, evidence, impact)
- ✅ Provide actionable recommendations, not just criticism
- ✅ Explain WHY something is an issue
- ✅ Be consistent with scoring across iterations
- ✅ Recognize improvements iteration-to-iteration

### For Optimizers
- ✅ Address HIGH impact issues first
- ✅ Validate each fix before re-evaluation
- ✅ Don't introduce new issues while fixing old ones
- ✅ Document what changed and why

---

## When NOT to Use

**Skip Evaluator-Optimizer for**:
- Trivial changes (typo fixes, formatting)
- Exploratory work (POCs, experiments)
- Internal-only, low-stakes documentation
- Time-critical hotfixes (use post-fix evaluation instead)

**Use streamlined version for**:
- Medium-priority work (1 iteration maximum)
- Well-understood patterns (quick validation)
- Internal tools (lower quality threshold OK)

---

*This workflow implements Anthropic's Evaluator-Optimizer pattern from the Claude Cookbook. Consistent use improves output quality by 30-50% while catching issues before production.*
