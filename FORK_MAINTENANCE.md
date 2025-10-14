# 🔒 Fork Maintenance & Security Guide

> **For Personal Portfolio Use** - Guidelines for keeping your public showcase fork secure and up-to-date

---

## 🎯 Purpose of This Fork

This is a **showcase fork** demonstrating the DA Agent Hub architecture and capabilities. It's designed to:

✅ **Demonstrate technical skills** and system design
✅ **Share innovative patterns** with the data community
✅ **Serve as a portfolio piece** for career discussions
✅ **Remain safe for public viewing** (no credentials, no proprietary info)

❌ **NOT for production use** without proper security setup
❌ **NOT including company-specific** implementations or data
❌ **NOT containing credentials** or sensitive configuration

---

## 🔐 Security Checklist (CRITICAL)

### Before Every Push to Public Fork

Run this manual security audit:

```bash
# 1. Check for .env files (should only be .env.template)
find . -name ".env" -not -name ".env.template" -type f

# 2. Search for credential patterns
rg -i "(password|secret|token|api[_-]?key)" --type-not gitignore

# 3. Check for company-specific URLs
rg -i "graniterock\.com|@graniterock"

# 4. Verify repositories.json is sanitized
cat config/repositories.json  # Should be example version

# 5. Review recent changes
git diff origin/main...HEAD
```

**🚨 IF ANY CHECKS FAIL**: Do NOT push. Investigate and sanitize first.

### Automated Protection

Your fork includes enhanced `.gitignore` rules:

```gitignore
# Environment files (CRITICAL - Never commit credentials)
.env
*.env
!.env.template

# Sensitive configuration (CRITICAL - Company-specific)
config/repositories.json.local
**/secrets/
**/*secret*
**/*credential*
**/*password*
**/*token*
.ssh/
*.pem
*.key
*.p12
*.pfx
```

**Always verify** `.gitignore` is up to date before committing.

---

## 🔄 Syncing with Upstream (GraniteRock)

### One-Time Setup
```bash
# Add upstream remote (if not already done)
cd ~/da-agent-hub
git remote add upstream https://github.com/graniterock/da-agent-hub.git
git remote add fork https://github.com/dmoditto/da-agent-hub.git

# Verify remotes
git remote -v
# origin → graniterock/da-agent-hub (private)
# upstream → graniterock/da-agent-hub (private, explicit)
# fork → dmoditto/da-agent-hub (public)
```

### Regular Sync Workflow

**IMPORTANT**: Never blindly merge upstream. Always review for sensitive data.

```bash
# 1. Fetch latest from GraniteRock
git fetch upstream main

# 2. Review changes BEFORE merging
git log --oneline --graph upstream/main ^main
git diff main...upstream/main

# 3. Look for sensitive additions
git diff main...upstream/main | rg -i "(password|secret|token|\.env[^.template]|graniterock\.com)"

# 4. Merge if safe
git checkout main
git merge upstream/main

# 5. Run security audit (see above)
./scripts/security-audit.sh  # If you create this helper

# 6. Push to fork
git push fork main
```

### What to Sync, What to Skip

**✅ Safe to Sync**:
- Agent prompt improvements (`.claude/agents/`)
- Workflow script enhancements (`scripts/`)
- Documentation updates (`knowledge/`, `docs/`)
- Architecture patterns (`.claude/memory/patterns/`)
- GitHub Actions workflows (`.github/workflows/`)

**⚠️ Review Carefully**:
- Configuration changes (`config/`)
- New MCP server setups (`.claude/mcp.json`, `.mcp.json`)
- Project completions (`projects/completed/`)
- Knowledge base updates (`knowledge/da_obsidian/`, `knowledge/da_team_documentation/`)

**❌ Never Sync**:
- `.env` files (use `.env.template` only)
- Company-specific repository URLs
- Internal documentation with sensitive business context
- Completed projects with proprietary implementations

---

## 📝 Sanitization Patterns

### Configuration Files

**Before**:
```json
{
  "dbt_cloud": {
    "url": "https://github.com/graniterock/dbt_cloud.git",
    "branch": "dbt_dw"
  }
}
```

**After**:
```json
{
  "dbt_cloud": {
    "url": "https://github.com/YOUR_ORG/dbt_cloud.git",
    "branch": "main"
  }
}
```

### Environment Templates

**Good** (`.env.template`):
```bash
SNOWFLAKE_ACCOUNT=your_account_here
SNOWFLAKE_USER=your_username
DBT_TOKEN=your_dbt_token
```

**Bad** (NEVER commit):
```bash
SNOWFLAKE_ACCOUNT=graniterock.us-west-2
SNOWFLAKE_USER=dylan.morrish@graniterock.com
DBT_TOKEN=dbt_ghp_abc123xyz...
```

### Documentation Content

**Safe** (System architecture):
```markdown
## Orchestration Hierarchy
- Level 1: Orchestra (master orchestrator)
- Level 2: Prefect flows, dbt jobs, Airbyte syncs
- Level 3: Data warehouses
```

**Unsafe** (Specific implementations):
```markdown
## Production Setup
- Orchestra runs on 10.20.30.40 (internal IP)
- Database: graniterock.snowflakecomputing.com
- Admin: dylan.morrish@graniterock.com
```

---

## 🚀 Making Your Fork Stand Out

### What Recruiters/Engineers Look For

1. **Clear Value Proposition**
   - ✅ Read `SHOWCASE.md` first (not buried in main README)
   - ✅ Measurable impact (70% faster, 50% reduction, etc.)
   - ✅ Real-world examples with context

2. **Technical Depth**
   - ✅ Architecture diagrams showing system design
   - ✅ Code samples demonstrating patterns
   - ✅ Explanation of trade-offs and decisions

3. **Thought Process**
   - ✅ "What I learned" sections
   - ✅ "Why I built it this way" explanations
   - ✅ Future enhancements with reasoning

### Recommended Updates

**Add to README.md** (top):
```markdown
> 🎯 **Showcase Portfolio Project** - See [SHOWCASE.md](SHOWCASE.md) for detailed value demonstration and technical highlights.
>
> This fork demonstrates an AI-powered Analytics Development Lifecycle platform.
> Original work developed at GraniteRock, sanitized for public sharing.
```

**Create visual assets**:
- System architecture diagram (Mermaid or draw.io)
- Workflow animation showing `/idea` → `/start` → `/complete`
- Screenshot of agent coordination in action

**Write case studies**:
- Document 2-3 real projects (sanitized)
- Show before/after workflows
- Include code samples and decision rationale

---

## 📊 Tracking Fork Health

### Regular Maintenance Schedule

**Weekly**:
- [ ] Review any new commits to upstream
- [ ] Check GitHub Issues/Discussions on fork
- [ ] Verify no secrets leaked (run security audit)

**Monthly**:
- [ ] Sync with upstream (if valuable improvements)
- [ ] Update SHOWCASE.md with new learnings
- [ ] Review and respond to community engagement

**Quarterly**:
- [ ] Major documentation refresh
- [ ] Add new case studies or examples
- [ ] Consider architectural improvements

### Health Metrics

Track these to gauge fork success:

- **GitHub Stars**: Interest from community
- **Forks**: Others adapting your approach
- **Issues/Discussions**: Engagement and questions
- **Profile Views**: Visibility in search

---

## 🛡️ Incident Response

### If Credentials Are Accidentally Committed

**IMMEDIATELY**:

1. **Revoke the credential** (dbt token, GitHub PAT, Snowflake password, etc.)
2. **Remove from git history**:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/sensitive/file" \
     --prune-empty --tag-name-filter cat -- --all

   git push fork --force --all
   ```
3. **Notify affected services** (GitHub, Snowflake, dbt Cloud admins)
4. **Document the incident** and improve prevention

### If Company Information Is Exposed

1. **Assess sensitivity**: Is it public knowledge or proprietary?
2. **Remove immediately** if proprietary:
   ```bash
   git revert <commit-hash>
   git push fork main
   ```
3. **Force push** if history needs cleaning:
   ```bash
   # Use with extreme caution
   git rebase -i HEAD~N  # Remove sensitive commits
   git push fork main --force
   ```
4. **Contact GraniteRock** if material information was exposed

---

## 🤝 Community Engagement

### How to Handle Questions

**Good Responses**:
- "Great question! This pattern came from needing to coordinate 5+ specialist agents..."
- "Here's how I approached that: [detailed explanation]"
- "I learned this the hard way when... [story + solution]"

**Avoid**:
- Sharing company-specific implementations
- Disclosing proprietary business logic
- Revealing internal tooling details

### Contributing Back

If community improvements are valuable:

1. **Test thoroughly** in your fork
2. **Create PR to GraniteRock** (if appropriate and you still have access)
3. **Document the improvement** with clear rationale
4. **Credit community contributor** in PR description

---

## 📚 Resources & References

### Security
- [GitHub: Removing Sensitive Data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [git-filter-repo Documentation](https://github.com/newren/git-filter-repo)
- [Pre-commit Hooks for Secret Detection](https://github.com/Yelp/detect-secrets)

### Showcase Best Practices
- [How to Build a Great GitHub Portfolio](https://www.freecodecamp.org/news/how-to-build-a-great-github-portfolio/)
- [Writing Technical Case Studies](https://medium.com/technical-writing-is-easy/how-to-write-a-software-case-study-8e7c72b4a7e4)
- [Open Source Project Documentation](https://opensource.guide/best-practices/)

---

## ✅ Pre-Push Checklist

Before every `git push fork main`:

- [ ] No `.env` files (only `.env.template`)
- [ ] `config/repositories.json` is sanitized example
- [ ] No company-specific URLs or emails
- [ ] No credential patterns in code
- [ ] No proprietary business logic
- [ ] Security audit completed
- [ ] Changes reviewed in `git diff`
- [ ] Commit messages are professional and clear

---

**Remember**: This fork is your portfolio. Keep it clean, secure, and impressive. 🚀

*Last updated: October 2025*
