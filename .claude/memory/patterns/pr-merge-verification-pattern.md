# PR Merge Verification Pattern

**Created**: 2025-10-15
**Context**: PR #129 was merged but only included 1 of 2 commits from feature branch
**Criticality**: HIGH - Incomplete merges cause confusion and partial deployments

---

## The Problem

When creating PRs with multiple commits, GitHub may merge only some commits if:
- Squash merge is used (combines all commits into one)
- User cherry-picks specific commits
- Merge strategy only takes certain commits

**What Happened with PR #129**:
- Feature branch had 2 commits:
  1. `2bfad629` - Implement enhanced switch (merged ✅)
  2. `549d55fb` - Replace switch.sh with enhanced version (NOT merged ❌)
- Result: Both `switch.sh` and `switch-enhanced.sh` exist instead of enhanced replacing original

---

## CRITICAL: Pre-Merge Verification Protocol

**BEFORE creating a PR, ALWAYS verify the complete commit sequence:**

```bash
# 1. List all commits on feature branch that aren't on main
git log main..HEAD --oneline

# 2. Verify each commit is intentional and should be merged
# If any commit is WIP or experimental, squash or remove it BEFORE PR creation

# 3. When PR is created, verify GitHub shows ALL commits
gh pr view <PR_NUMBER> --json commits --jq '.commits[] | "\(.oid[0:8]) \(.messageHeadline)"'

# 4. If commits are missing from PR, investigate immediately
```

---

## POST-Merge Verification Protocol

**AFTER PR is merged, ALWAYS verify all commits made it to main:**

```bash
# 1. Pull latest main
git checkout main && git pull origin main

# 2. Check if specific commits from feature branch are in main
git log --oneline --grep="<search term from commit message>"

# 3. Verify all expected files exist
ls -la <expected-files>

# 4. If commits are missing:
#    - Create follow-up PR with missing commits
#    - OR cherry-pick missing commits directly to main (if urgent)
```

---

## Example: Proper PR Merge Verification

```bash
# BEFORE creating PR #129:
git log main..feature/enhanced-switch-anthropic-best-practices --oneline
# Expected output:
# 549d55fb refactor: Replace switch.sh with enhanced version
# 2bfad629 feat: Implement enhanced /switch with Anthropic best practices

# Create PR
gh pr create --title "..." --body "..."

# Verify PR shows all commits
gh pr view 129 --json commits --jq '.commits[] | "\(.oid[0:8]) \(.messageHeadline)"'
# Should show BOTH commits

# AFTER merge:
git checkout main && git pull origin main

# Verify both commits are in main
git log --oneline -5
# Should show merge commit that includes BOTH feature commits

# Verify expected files
ls -la scripts/switch.sh scripts/switch-legacy.sh scripts/switch-enhanced.sh
# Should show:
# - switch-legacy.sh (renamed original)
# - switch.sh (enhanced version)
# - switch-enhanced.sh should NOT exist (was renamed)
```

---

## Red Flags That Indicate Incomplete Merge

1. **Feature branch has N commits, but main only gained N-1 commits**
2. **Expected file renames didn't happen** (e.g., switch-enhanced.sh still exists)
3. **PR description mentions changes not reflected in merged files**
4. **git log on main doesn't show all feature branch commit messages**

---

## Recovery Actions

If incomplete merge is detected:

### Option 1: Follow-up PR (Preferred)
```bash
# Create new branch from main
git checkout main
git pull origin main
git checkout -b fix/complete-pr-129-merge

# Cherry-pick missing commits
git cherry-pick 549d55fb

# Create follow-up PR
gh pr create --title "fix: Complete PR #129 merge - replace switch.sh with enhanced version"
```

### Option 2: Direct Push (If Urgent + Safe)
```bash
# Only if change is low-risk and needs immediate deployment
git checkout main
git pull origin main
git cherry-pick 549d55fb
git push origin main
```

### Option 3: Accept Current State (If Better)
```bash
# Sometimes incomplete merge is actually better
# e.g., Having both switch.sh and switch-enhanced.sh allows gradual migration
# Document this decision in project completion notes
```

---

## Prevention Checklist

**Every PR Creation**:
- [ ] Run `git log main..HEAD --oneline` to see all commits
- [ ] Verify each commit is intentional (no WIP/debug commits)
- [ ] If multiple commits do related work, consider squashing
- [ ] Document all commits in PR description

**Every PR Merge**:
- [ ] Pull latest main after merge
- [ ] Run `git log --oneline -10` to verify commits present
- [ ] Check expected files exist with `ls -la`
- [ ] If discrepancy detected, create follow-up PR immediately

---

## Pattern Integration

**Where This Pattern Applies**:
- All feature branch → main merges
- All PR creation and merge workflows
- Especially important for refactoring commits (renames, deletions, restructuring)

**When to Use**:
- BEFORE: Every PR creation
- DURING: PR review (reviewer should verify commit list)
- AFTER: Every PR merge

**Tools Required**:
- `git log` for commit verification
- `gh pr view` for GitHub PR inspection
- `ls -la` for file verification

---

## Success Criteria

✅ **Successful merge verification**:
- All commits from feature branch present in main
- All expected files exist (or don't exist if deleted)
- PR description matches actual changes in main
- No confusion about "missing" features

❌ **Failed merge verification**:
- Feature branch commits missing from main
- Expected files missing or renamed incorrectly
- PR description describes changes not in main
- Team asks "where is feature X that was supposedly merged?"

---

## Lessons Learned from PR #129

1. **Don't assume GitHub merged everything** - Always verify
2. **File renames are high-risk** - Double-check these specifically
3. **Multi-commit PRs need extra verification** - More commits = more risk
4. **Post-merge verification is critical** - Prevents confusion later

---

## Memory Pattern Trigger

**When Claude creates a PR, ALWAYS**:
1. List commits before creating PR
2. Verify PR shows all commits after creation
3. After user says "PR merged", verify all commits in main
4. If discrepancy found, alert user and offer recovery options

**Search Terms for Future Reference**:
- PR merge verification
- Incomplete merge detection
- Feature branch commit verification
- Git merge completion check

---

*Pattern created to prevent incomplete merges like PR #129*
*Criticality: HIGH - This pattern prevents production confusion and incomplete deployments*
