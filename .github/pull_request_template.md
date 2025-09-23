## Summary
Brief description of changes made in this PR.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Agent improvement/capability enhancement

## 🤖 Claude Completion Decision (REQUIRED)

**Every PR must have a completion decision before merge:**

### ✅ Choose One:
- [ ] **`claude:complete`** - This PR should get automated completion (documentation, agent improvements, knowledge extraction)
- [ ] **`claude:skip`** - Skip completion for this PR (time constraints, already comprehensive, sensitive content)
- [ ] **`claude:no-need`** - No completion needed (dependency updates, pure config changes, deletions only)

### 📋 Decision Criteria:

**Use `claude:complete` for:**
- New agent capabilities or behavior changes
- Documentation that could be enhanced or standardized
- Knowledge patterns worth extracting for future use
- Code requiring final polish or optimization
- Cross-system integration patterns
- Complex implementations with learning value

**Use `claude:skip` for:**
- Simple fixes with time constraints
- Already comprehensive documentation
- Sensitive content requiring manual review
- Work that doesn't fit completion patterns

**Use `claude:no-need` for:**
- Dependency updates or automated changes
- Pure configuration/settings changes
- Deletion-only changes with no replacement logic
- Changes with no documentation improvement potential

### 💰 Cost: ~$0.08-0.18 per completion | Saves: 1-3 hours manual work

## Testing
- [ ] Tested locally
- [ ] All tests pass
- [ ] No breaking changes introduced

## Additional Notes
Any additional context, concerns, or considerations for reviewers.