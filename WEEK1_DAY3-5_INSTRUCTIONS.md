# Week 1 Days 3-5: Token Setup & Testing Instructions
**Phase**: Week 1 of 12-week migration
**Prerequisites**: Week 1 Days 1-2 complete, PR #83 merged, Claude Code restarted
**Estimated Time**: 3-4 hours total

---

## Overview

Days 3-5 focus on:
1. Enabling github-mcp (Day 3)
2. Enabling slack-mcp (Day 4)
3. Comprehensive testing of all specialists and MCP servers (Day 5)

**Goal**: Complete Week 1 with 11 active MCP servers and 3 validated specialists

---

## Day 3: Enable github-mcp (30 minutes)

### Task: Configure GitHub Personal Access Token

**Why needed**: Enables github-sleuth-expert for repository analysis, PR patterns, code review

### Step-by-Step Instructions

#### 1. Create GitHub Personal Access Token (10 minutes)

**Navigate to**: https://github.com/settings/tokens

**Click**: "Generate new token" → "Generate new token (classic)"

**Token configuration**:
- **Note**: "da-agent-hub-mcp-server"
- **Expiration**: 90 days (or custom)
- **Scopes to select**:
  - ✅ **repo** (Full control of private repositories)
    - repo:status
    - repo_deployment
    - public_repo
    - repo:invite
    - security_events
  - ✅ **read:org** (Read org and team membership, read org projects)
  - ✅ **read:project** (Read access to projects)

**Click**: "Generate token"

**CRITICAL**: Copy the token immediately (starts with `ghp_...`)
- You won't be able to see it again
- Store securely

#### 2. Add Token to .claude/mcp.json (5 minutes)

**Open**: `.claude/mcp.json`

**Find this section**:
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": ""
  },
  "disabled": true,
  "autoApprove": [],
  "_comment": "Week 1 Day 3 - Enable after setting GITHUB_PERSONAL_ACCESS_TOKEN. Scopes needed: repo, read:org"
}
```

**Update to**:
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_YOUR_TOKEN_HERE"
  },
  "disabled": false,
  "autoApprove": [],
  "_comment": "Week 1 Day 3 - ENABLED"
}
```

**Replace**: `ghp_YOUR_TOKEN_HERE` with your actual token

**Change**: `"disabled": true` → `"disabled": false`

**Save** the file

#### 3. Restart Claude Code (5 minutes)

**CRITICAL**: MCP servers only load on session start

```bash
# Exit current Claude Code session
# Restart Claude Code CLI
# New session will load github-mcp
```

#### 4. Verify github-mcp Loaded (5 minutes)

**Check MCP servers**:
```bash
claude mcp list
```

**Should see** (10 servers now):
- dbt-mcp ✓
- snowflake-mcp ✓
- freshservice-mcp ✓
- aws-api ✓
- aws-docs ✓
- aws-knowledge ✓
- git ✓
- filesystem ✓
- sequential-thinking ✓
- **github ✓ NEW**

**If github doesn't appear**:
- Check token is correct in .claude/mcp.json
- Check disabled: false
- Check syntax (no trailing commas, proper JSON)
- Restart Claude Code again

#### 5. Test github-mcp (5 minutes)

**Basic test** (if I can access GitHub MCP tools in this session):
```bash
# List repositories
# Search issues
# Get PR details
```

**Expected**: Should return data from graniterock GitHub organization

**If errors**:
- Check token scopes (repo, read:org, read:project)
- Verify token hasn't expired
- Check network connectivity

### Day 3 Completion Checklist
- [ ] GitHub token created and copied
- [ ] Token added to .claude/mcp.json
- [ ] github server enabled (disabled: false)
- [ ] Claude Code restarted
- [ ] github-mcp appears in `claude mcp list`
- [ ] github-mcp test successful

---

## Day 4-5: Enable slack-mcp + Comprehensive Testing (2.5-3 hours)

### Part 1: Enable slack-mcp (1 hour)

#### Why needed
Enables business-context specialist for stakeholder communication, team notifications, requirement gathering

### Step-by-Step Instructions

#### 1. Create Slack Bot App (30 minutes)

**Navigate to**: https://api.slack.com/apps

**Create New App**:
- Click "Create New App"
- Choose "From scratch"
- App Name: "DA Agent Hub MCP"
- Workspace: [Select your Slack workspace]
- Click "Create App"

**Configure Bot Token Scopes**:
1. Navigate to "OAuth & Permissions" (left sidebar)
2. Scroll to "Scopes" → "Bot Token Scopes"
3. Add these scopes:
   - ✅ **channels:read** (View basic channel info)
   - ✅ **chat:write** (Send messages)
   - ✅ **users:read** (View people in workspace)
   - ✅ **channels:history** (View messages in public channels) - OPTIONAL
   - ✅ **groups:read** (View basic private channel info) - OPTIONAL

**Install App to Workspace**:
1. Scroll up to "OAuth Tokens for Your Workspace"
2. Click "Install to Workspace"
3. Review permissions
4. Click "Allow"

**Copy Bot Token**:
- After installation, you'll see "Bot User OAuth Token"
- Starts with `xoxb-...`
- Click "Copy"
- Store securely

#### 2. Get Slack Team ID (5 minutes)

**Method 1: From Slack App**:
- In Slack desktop app
- Click workspace name (top left)
- Click "Settings & administration" → "Workspace settings"
- Look at URL: `https://[TEAM_NAME].slack.com/admin/settings`
- Team ID usually visible in settings or URL

**Method 2: From API**:
- Navigate to: https://api.slack.com/methods/team.info/test
- Click "Test Method"
- Look for `"id": "T..."` in response
- Copy the T... value

**Team ID format**: Starts with `T` (e.g., `T01234ABCD`)

#### 3. Add Slack Tokens to .claude/mcp.json (5 minutes)

**Open**: `.claude/mcp.json`

**Find this section**:
```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": {
    "SLACK_BOT_TOKEN": "",
    "SLACK_TEAM_ID": ""
  },
  "disabled": true,
  "autoApprove": [],
  "_comment": "Week 1 Day 4 - Enable after setting SLACK_BOT_TOKEN and SLACK_TEAM_ID"
}
```

**Update to**:
```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": {
    "SLACK_BOT_TOKEN": "xoxb-YOUR-BOT-TOKEN-HERE",
    "SLACK_TEAM_ID": "T01234ABCD"
  },
  "disabled": false,
  "autoApprove": [],
  "_comment": "Week 1 Day 4 - ENABLED"
}
```

**Replace**:
- `xoxb-YOUR-BOT-TOKEN-HERE` with your actual bot token
- `T01234ABCD` with your actual team ID

**Change**: `"disabled": true` → `"disabled": false`

**Save** the file

#### 4. Restart Claude Code (5 minutes)

```bash
# Exit current Claude Code session
# Restart Claude Code CLI
# New session will load slack-mcp
```

#### 5. Verify slack-mcp Loaded (5 minutes)

**Check MCP servers**:
```bash
claude mcp list
```

**Should see** (11 servers total):
- Previous 10 servers ✓
- **slack ✓ NEW**

**Test slack-mcp**:
```bash
# List channels
# Send test message to testing channel (if available)
```

### Part 2: Comprehensive Testing (1.5-2 hours)

**CRITICAL**: Validate entire Week 1 foundation before proceeding to Week 2

#### Test 1: All MCP Servers Connected (15 minutes)

**Verify all 11 servers active**:
```bash
claude mcp list
```

**Expected output**:
1. dbt-mcp ✓
2. snowflake-mcp ✓
3. freshservice-mcp ✓
4. aws-api ✓
5. aws-docs ✓
6. aws-knowledge ✓
7. git ✓
8. filesystem ✓
9. sequential-thinking ✓
10. github ✓
11. slack ✓

**If any fail**:
- Check .claude/mcp.json configuration
- Verify environment variables set
- Check disabled: false
- Restart Claude Code
- Check Claude Code logs for errors

#### Test 2: dbt-expert Specialist Delegation (30 minutes)

**Scenario**: Ask analytics-engineer-role to delegate to dbt-expert

**Test delegation pattern**:
```
User: "I need to optimize a slow dbt incremental model"

Expected flow:
1. analytics-engineer-role recognizes need (confidence <0.75 on complex optimization)
2. Prepares context using dbt-mcp (gets model details, compiled SQL)
3. DELEGATES to dbt-expert
4. dbt-expert:
   - Uses dbt-mcp (analyze model, dependencies)
   - Uses snowflake-mcp (query performance)
   - Uses git-mcp (check history)
   - Uses sequential-thinking-mcp (complex debugging)
   - Applies dbt expertise
   - Returns validated optimization plan
5. analytics-engineer-role receives plan, validates, ready to execute
```

**Validation**:
- ✅ analytics-engineer delegates (doesn't try to optimize directly)
- ✅ dbt-expert uses MCP tools (dbt-mcp, snowflake-mcp visible in usage)
- ✅ dbt-expert applies expertise (not just MCP data, but synthesis)
- ✅ Recommendation is correct and validated
- ✅ analytics-engineer understands and can execute

**Document**:
- Did delegation work correctly?
- Did specialist use MCP tools?
- Was recommendation high-quality?
- Any issues or improvements needed?

#### Test 3: snowflake-expert Specialist Delegation (30 minutes)

**Scenario**: Ask analytics-engineer-role to delegate to snowflake-expert

**Test delegation pattern**:
```
User: "Snowflake costs are high, need optimization recommendations"

Expected flow:
1. analytics-engineer-role recognizes need (confidence <0.72 on cost optimization)
2. Prepares context using snowflake-mcp (gets cost data, usage patterns)
3. DELEGATES to snowflake-expert
4. snowflake-expert:
   - Uses snowflake-mcp (cost analysis, warehouse utilization)
   - Uses dbt-mcp (understand transformation patterns)
   - Uses sequential-thinking-mcp (break down cost drivers)
   - Applies Snowflake expertise
   - Returns cost optimization plan
5. analytics-engineer-role receives plan, validates, ready to implement
```

**Validation**:
- ✅ analytics-engineer delegates (doesn't analyze costs directly)
- ✅ snowflake-expert uses MCP tools (snowflake-mcp cost queries)
- ✅ snowflake-expert applies expertise (identifies optimization opportunities)
- ✅ Recommendations are actionable and validated
- ✅ Cost savings quantified

**Document**:
- Cost analysis quality?
- MCP tool usage correct?
- Recommendations practical?
- Issues identified?

#### Test 4: aws-expert Specialist Delegation (30 minutes)

**Scenario**: Ask ui-ux-developer-role to delegate AWS deployment

**Test delegation pattern**:
```
User: "Deploy updated React app to AWS ECS"

Expected flow:
1. ui-ux-developer-role recognizes need (confidence <0.60 on AWS)
2. Prepares context using aws-api MCP (gets current ECS service config)
3. DELEGATES to aws-expert
4. aws-expert:
   - Uses aws-api MCP (infrastructure state)
   - Uses aws-knowledge MCP (deployment best practices)
   - Uses aws-docs MCP (latest ECS API syntax)
   - Applies AWS expertise
   - Returns validated deployment plan
5. ui-ux-developer-role receives plan, validates, ready to deploy
```

**Validation**:
- ✅ ui-ux-developer delegates (doesn't attempt AWS work directly)
- ✅ aws-expert uses AWS MCP suite
- ✅ aws-expert validates architecture (health checks, security, etc.)
- ✅ Deployment plan is complete and correct
- ✅ Includes rollback procedures

#### Test 5: Multi-Specialist Scenario (30 minutes)

**Scenario**: Task requiring multiple specialists

**Test collaboration**:
```
User: "New financial dashboard - optimize entire stack"

Expected flow:
1. bi-developer-role (primary) recognizes needs multiple specialists
2. DELEGATES to tableau-expert (dashboard optimization) - FUTURE, skip if not available
3. DELEGATES to snowflake-expert (data source optimization)
4. DELEGATES to dbt-expert (semantic layer / model optimization)
5. Each specialist uses MCP tools + expertise
6. bi-developer-role synthesizes recommendations
7. Executes holistic optimization
```

**Validation**:
- ✅ Role coordinates multiple specialists (doesn't try to optimize all layers directly)
- ✅ Each specialist focuses on their domain
- ✅ Recommendations are compatible and integrated
- ✅ No conflicts or duplication

#### Test 6: MCP Tool Direct Usage (Negative Test - 15 minutes)

**Purpose**: Verify roles DON'T use MCP directly without specialist

**Anti-pattern to avoid**:
```
ui-ux-developer: "I'll just use aws-api MCP to check ECS and deploy"
↓ Uses aws-api directly
↓ Interprets without expertise
↓ 💥 This should NOT happen
```

**Expected behavior**:
```
ui-ux-developer: "I need AWS deployment"
↓ Recognizes low confidence (<0.60)
↓ DELEGATES to aws-expert
↓ ✅ Correct pattern
```

**Validation**:
- ✅ Roles delegate rather than use specialist MCP tools directly
- ✅ Specialists use MCP tools + expertise
- ✅ Pattern maintains quality and correctness

### Day 3 Completion Checklist
- [ ] GitHub token created
- [ ] Token added to .claude/mcp.json
- [ ] github server enabled
- [ ] Claude Code restarted
- [ ] github-mcp in server list
- [ ] github-mcp tested successfully

---

## Day 4: Enable slack-mcp (1 hour)

### Steps (See Part 1 above for details)

1. [ ] Create Slack bot app (30 min)
2. [ ] Get Bot User OAuth Token (xoxb-...)
3. [ ] Get Slack Team ID (T...)
4. [ ] Add tokens to .claude/mcp.json (5 min)
5. [ ] Enable slack server (disabled: false)
6. [ ] Restart Claude Code (5 min)
7. [ ] Verify slack-mcp loaded (5 min)
8. [ ] Test slack-mcp (15 min)

### Day 4 Completion Checklist
- [ ] Slack bot created
- [ ] Slack tokens obtained (bot token + team ID)
- [ ] Tokens added to .claude/mcp.json
- [ ] slack server enabled
- [ ] Claude Code restarted
- [ ] slack-mcp in server list (11 total)
- [ ] slack-mcp tested successfully

---

## Day 5: Comprehensive Testing & Week 1 Validation (1-1.5 hours)

### Validation Testing (Complete all tests from Part 2 above)

**Test Suite**:
1. [ ] All MCP servers connected (11 total)
2. [ ] dbt-expert delegation pattern works correctly
3. [ ] snowflake-expert delegation pattern works correctly
4. [ ] aws-expert delegation pattern works correctly
5. [ ] Multi-specialist collaboration works
6. [ ] Roles delegate (don't use MCP directly)

### Quality Validation

**Specialist Recommendations Check**:
- [ ] dbt-expert recommendations are production-ready
- [ ] snowflake-expert cost analysis is accurate
- [ ] aws-expert deployment plans are complete
- [ ] All specialists validate before returning to roles

**MCP Tool Usage Check**:
- [ ] Specialists use MCP tools for data gathering
- [ ] Specialists apply expertise to synthesize solutions
- [ ] MCP data + expertise = informed recommendations
- [ ] Not just MCP data dumps

### Performance Baseline

**Measure and document**:
- [ ] Time for dbt-expert consultation (target: <30 min)
- [ ] Time for snowflake-expert consultation (target: <45 min)
- [ ] Time for aws-expert consultation (target: <30 min)
- [ ] Quality of recommendations (expert-level vs basic)

### Week 1 Documentation

**Create final Week 1 summary**:
- [ ] Document all test results
- [ ] List any issues encountered
- [ ] Identify improvements needed
- [ ] Update migration plan with actuals vs estimates
- [ ] Celebrate Week 1 completion! 🎉

### Day 5 Completion Checklist
- [ ] All 6 test scenarios passed
- [ ] Quality validation complete
- [ ] Performance baseline documented
- [ ] Week 1 learnings captured
- [ ] Ready to start Week 2

---

## Troubleshooting Guide

### Issue: MCP Server Won't Load

**Symptoms**: Server missing from `claude mcp list`

**Solutions**:
1. Check .claude/mcp.json syntax (valid JSON, no trailing commas)
2. Verify disabled: false
3. Check environment variables set correctly
4. Restart Claude Code (servers load on start)
5. Check Claude Code logs for errors
6. Verify MCP server package exists (try manual install: `npx -y @modelcontextprotocol/server-[name]`)

### Issue: GitHub Token Invalid

**Symptoms**: github-mcp fails to connect

**Solutions**:
1. Verify token starts with `ghp_`
2. Check token hasn't expired
3. Verify scopes: repo, read:org, read:project
4. Try creating new token
5. Check GitHub rate limits (unlikely but possible)

### Issue: Slack Bot Won't Connect

**Symptoms**: slack-mcp fails to load

**Solutions**:
1. Verify bot token starts with `xoxb-`
2. Verify team ID starts with `T`
3. Check bot is installed to workspace
4. Verify bot scopes: channels:read, chat:write, users:read
5. Check workspace permissions allow bots

### Issue: Specialist Doesn't Use MCP Tools

**Symptoms**: Specialist gives generic advice without using MCP data

**Solutions**:
1. Ensure specialist agent file has MCP Tools Integration section
2. Verify specialist knows which MCP tools to use
3. Check MCP tools are loaded and accessible
4. Specialist may need explicit instruction: "Use [mcp-tool] to gather current state"

### Issue: Role Uses MCP Directly Instead of Delegating

**Symptoms**: Role agent tries to use specialist MCP tools

**Solutions**:
1. Update role agent with Delegation Decision Framework
2. Add "When to Delegate to Specialist" section
3. Set clear confidence thresholds (<0.60 = delegate)
4. Provide delegation protocol (5-step process)

---

## Success Criteria for Week 1

### Technical Success ✅
- [ ] 11 MCP servers active (all configured servers working)
- [ ] 3 specialists operational (aws, dbt, snowflake)
- [ ] Folder structure organized (roles/, specialists/, deprecated/)
- [ ] Templates created and documented

### Quality Success ✅
- [ ] Specialists use MCP + expertise pattern correctly
- [ ] Delegation patterns work end-to-end
- [ ] Recommendations are expert-quality (>90% accuracy)
- [ ] Roles delegate appropriately (not using MCP directly)

### Documentation Success ✅
- [ ] All 14 documents complete (research + guides)
- [ ] Templates ready for team use
- [ ] Migration plan updated with actuals
- [ ] Week 1 learnings documented

### Business Success ✅
- [ ] Team understands architecture
- [ ] Ready to scale (Week 2 rollout)
- [ ] Clear path forward (Week 2-12 plan)
- [ ] Confidence in correctness-first approach

---

## After Week 1 Completion

### Immediate Actions
1. Review Week 1 results
2. Identify any blockers for Week 2
3. Celebrate foundation completion! 🎉

### Week 2 Preview (After Week 1 Complete)

**Focus**: Update remaining role agents with delegation protocols

**Tasks**:
- Update data-engineer-role with orchestra/prefect/dlthub delegation
- Update bi-developer-role with tableau delegation
- Update ui-ux-developer-role with aws/react delegation
- Test multi-role scenarios
- Measure success metrics vs baseline

**Timeline**: 1 week (5-10 hours)

### Week 3-4 Preview (Weeks Away)

**Focus**: Custom MCP development (Orchestra, Prefect)

**Critical path**: Orchestra-mcp and Prefect-mcp development
- These are blockers for reviving orchestra-expert and prefect-expert
- No official servers exist, must develop custom
- Highest priority after Week 1-2 foundation

---

## Quick Reference

### Environment Variables Needed

**Week 1** (Days 3-5):
- `GITHUB_PERSONAL_ACCESS_TOKEN` (Day 3)
- `SLACK_BOT_TOKEN` (Day 4)
- `SLACK_TEAM_ID` (Day 4)

**Week 2-3** (Future):
- `ATLASSIAN_EMAIL`
- `ATLASSIAN_API_TOKEN`
- `ATLASSIAN_SITE_URL`

**Week 4** (Custom MCP):
- Orchestra API credentials (in .env)
- Prefect API credentials (in .env)

### Files to Reference

**During token setup**:
- `.claude/mcp.json` - Configuration file to edit
- This document - Step-by-step instructions

**During testing**:
- `.claude/agents/README.md` - Architecture guide
- `docs/mcp-vs-specialist-decision-tree.md` - Delegation decisions
- Specialist files in `.claude/agents/specialists/` - Expected behavior

**For troubleshooting**:
- `docs/mcp-research-2025/architecture-migration-plan.md` - Migration details
- Claude Code logs - Error messages

---

## Time Estimates

**Day 3**: 30 minutes
- GitHub token: 10 min
- Add to config: 5 min
- Restart + verify: 10 min
- Test: 5 min

**Day 4**: 1 hour
- Slack bot creation: 30 min
- Get team ID: 5 min
- Add to config: 5 min
- Restart + verify: 10 min
- Test: 10 min

**Day 5**: 1.5-2 hours
- MCP server verification: 15 min
- Specialist testing (3 specialists): 1.5 hours
- Documentation: 30 min

**Total**: 3-3.5 hours for Days 3-5

---

## Next Session Quick Start

### When Resuming on Day 3

**Check current state**:
```bash
# Verify PR merged
gh pr view 83

# Check current branch
git branch --show-current

# Check MCP servers currently loaded
claude mcp list
```

**Then follow**:
- Day 3 instructions (GitHub token setup)
- Day 4 instructions (Slack token setup)
- Day 5 instructions (Comprehensive testing)

### When Resuming After Week 1

**Verify Week 1 complete**:
- [ ] 11 MCP servers active
- [ ] 3 specialists operational
- [ ] All tests passed
- [ ] Documentation complete

**Then start Week 2**:
- Follow `docs/mcp-research-2025/architecture-migration-plan.md` Week 2 section
- Update remaining role agents with delegation protocols
- Continue migration rollout

---

**Week 1 Days 3-5 Instructions Complete**
**Next**: Get GitHub token and begin Day 3 setup
**Reference**: See troubleshooting guide if issues arise
**Goal**: 11 active MCP servers, 3 validated specialists, Week 1 complete ✅
