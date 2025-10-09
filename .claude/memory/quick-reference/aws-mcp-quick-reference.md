# AWS MCP Quick Reference Card

**Purpose**: Fast lookup for AWS infrastructure operations and documentation
**Primary Users**: aws-expert, data-engineer-role, ui-ux-developer-role, data-architect-role
**Servers**: aws-api (execution) + aws-docs (documentation)

---

## 🚀 Most Common Operations

### AWS API MCP (aws-api)

#### 1. Command Execution

**Execute AWS CLI command** (read-only):
```bash
mcp__aws-api__call_aws \
  cli_command="aws sts get-caller-identity"
```

**List EC2 instances**:
```bash
mcp__aws-api__call_aws \
  cli_command="aws ec2 describe-instances --region us-west-2"
```

**List ECS services**:
```bash
mcp__aws-api__call_aws \
  cli_command="aws ecs list-services --cluster my-cluster --region us-west-2"
```

**Get ECS service details**:
```bash
mcp__aws-api__call_aws \
  cli_command="aws ecs describe-services --cluster my-cluster --services my-service --region us-west-2"
```

**List S3 buckets**:
```bash
mcp__aws-api__call_aws \
  cli_command="aws s3 ls"
```

**Get RDS instances**:
```bash
mcp__aws-api__call_aws \
  cli_command="aws rds describe-db-instances --region us-west-2"
```

**List Lambda functions**:
```bash
mcp__aws-api__call_aws \
  cli_command="aws lambda list-functions --region us-west-2"
```

**Check CloudFormation stacks**:
```bash
mcp__aws-api__call_aws \
  cli_command="aws cloudformation list-stacks --region us-west-2"
```

---

#### 2. Command Discovery (RAG-Based)

**Find command for task** (when unsure):
```bash
mcp__aws-api__suggest_aws_commands \
  query="list all running EC2 instances in us-east-1 region"
```

**Discover S3 operations**:
```bash
mcp__aws-api__suggest_aws_commands \
  query="get the size of my S3 bucket named 'my-backup-bucket'"
```

**Find Lambda configuration command**:
```bash
mcp__aws-api__suggest_aws_commands \
  query="update the memory allocation of my Lambda function 'data-processor' to 1024MB"
```

**Note**: Returns top 10 most likely commands with confidence scores

---

### AWS Docs MCP (aws-docs)

#### 1. Documentation Search

**Search for best practices**:
```bash
mcp__aws-docs__search_documentation \
  search_phrase="ECS Fargate best practices" \
  limit=5
```

**Find service limits**:
```bash
mcp__aws-docs__search_documentation \
  search_phrase="Lambda function concurrency limits" \
  limit=3
```

**Search for specific configuration**:
```bash
mcp__aws-docs__search_documentation \
  search_phrase="RDS parameter group configuration" \
  limit=5
```

---

#### 2. Read Documentation Page

**Read specific doc page**:
```bash
mcp__aws-docs__read_documentation \
  url="https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html" \
  max_length=5000
```

**Read with pagination** (long docs):
```bash
# First chunk
mcp__aws-docs__read_documentation \
  url="https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html" \
  max_length=5000 \
  start_index=0

# Next chunk
mcp__aws-docs__read_documentation \
  url="https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html" \
  max_length=5000 \
  start_index=5000
```

---

#### 3. Recommendations (Related Content)

**Get related documentation**:
```bash
mcp__aws-docs__recommend \
  url="https://docs.aws.amazon.com/ecs/latest/developerguide/Welcome.html"
```

**Find newly released features**:
```bash
# 1. Get service welcome page
# 2. Call recommend with that URL
# 3. Check "New" recommendation type for recent releases
mcp__aws-docs__recommend \
  url="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"
```

**Returns 4 types**:
- **Highly Rated**: Popular pages within service
- **New**: Recently added pages (NEW FEATURES)
- **Similar**: Related topics
- **Journey**: Commonly viewed next

---

## 🎯 Common Workflows

### Workflow 1: Infrastructure Discovery
```bash
# 1. Check current AWS account/region
mcp__aws-api__call_aws \
  cli_command="aws sts get-caller-identity"

# 2. List ECS clusters
mcp__aws-api__call_aws \
  cli_command="aws ecs list-clusters --region us-west-2"

# 3. Get services in cluster
mcp__aws-api__call_aws \
  cli_command="aws ecs list-services --cluster my-cluster --region us-west-2"

# 4. Get service details
mcp__aws-api__call_aws \
  cli_command="aws ecs describe-services --cluster my-cluster --services my-service --region us-west-2"

# 5. Check task definitions
mcp__aws-api__call_aws \
  cli_command="aws ecs describe-task-definition --task-definition my-task:latest --region us-west-2"
```

### Workflow 2: Documentation-First Deployment
```bash
# 1. Search for deployment best practices
mcp__aws-docs__search_documentation \
  search_phrase="ECS Fargate deployment best practices" \
  limit=5

# 2. Read specific best practices page
mcp__aws-docs__read_documentation \
  url="https://docs.aws.amazon.com/ecs/latest/bestpracticesguide/..."

# 3. Get related documentation
mcp__aws-docs__recommend \
  url="https://docs.aws.amazon.com/ecs/latest/bestpracticesguide/..."

# 4. Validate current infrastructure state
mcp__aws-api__call_aws \
  cli_command="aws ecs describe-services --cluster my-cluster --services my-service --region us-west-2"

# 5. Provide deployment recommendations based on docs
```

### Workflow 3: Command Discovery for New Task
```bash
# 1. Not sure which AWS CLI command to use
mcp__aws-api__suggest_aws_commands \
  query="configure CloudWatch alarms for high CPU utilization on my RDS instance"

# 2. Review suggested commands with confidence scores
# Output: Top 10 commands ranked by relevance

# 3. Execute recommended command
mcp__aws-api__call_aws \
  cli_command="aws cloudwatch put-metric-alarm ..."
```

### Workflow 4: New Feature Discovery
```bash
# 1. Get Lambda service welcome page URL
# 2. Get recommendations to find new features
mcp__aws-docs__recommend \
  url="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

# 3. Check "New" recommendation type for recent releases

# 4. Read new feature documentation
mcp__aws-docs__read_documentation \
  url="[URL from New recommendations]"

# 5. Search for implementation guides
mcp__aws-docs__search_documentation \
  search_phrase="[new feature name] implementation guide"
```

### Workflow 5: Cost Analysis & Optimization
```bash
# 1. List current resources
mcp__aws-api__call_aws \
  cli_command="aws ec2 describe-instances --region us-west-2"

# 2. Search for cost optimization docs
mcp__aws-docs__search_documentation \
  search_phrase="EC2 cost optimization strategies" \
  limit=5

# 3. Read cost optimization guide
mcp__aws-docs__read_documentation \
  url="[cost optimization guide URL]"

# 4. Check resource utilization
mcp__aws-api__call_aws \
  cli_command="aws cloudwatch get-metric-statistics ..."

# 5. Provide optimization recommendations
```

---

## ⚠️ Important Notes

### AWS API Security (READ-ONLY Mode)

**READ_OPERATIONS_ONLY=true** (Default):
- ✅ **Describe** operations (infrastructure inventory)
- ✅ **List** operations (resource discovery)
- ✅ **Get** operations (configuration details)
- ❌ **Create** operations (blocked)
- ❌ **Delete** operations (blocked)
- ❌ **Modify** operations (blocked)
- ❌ **Update** operations (blocked)

**Why read-only**: Prevents accidental infrastructure changes

**Pattern**: aws-expert provides recommendations, human implements

**Command Restrictions**:
- ❌ No shell operators (pipes `|`, redirection `>`, command substitution `$()`)
- ❌ No bash/zsh tools (grep, awk, sed, etc.)
- ✅ Use absolute paths only (no relative paths)
- ✅ Database-agnostic SQL syntax only

### AWS Docs Currency (CRITICAL)

**aws-docs provides CURRENT documentation** (not just training data from Jan 2025):
- ✅ Latest service limits
- ✅ New features and releases
- ✅ Updated best practices
- ✅ Current API parameters
- ✅ Security recommendations

**Always verify with aws-docs before recommending**:
- Service configurations (limits may have changed)
- API parameters (new parameters added)
- Best practices (updated for new features)
- Security guidelines (evolving threat landscape)

### Performance Considerations

**aws-api**:
- No built-in pagination in MCP tool
- Use AWS CLI pagination flags: `--max-items`, `--starting-token`
- Large result sets can timeout
- Filter at source when possible

**aws-docs**:
- `read_documentation`: Default 5000 chars, max 1,000,000
- Use `start_index` for pagination on long docs
- `search_documentation`: Returns top 10-50 results
- Self-cleaning 15-minute cache (faster repeat access)

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: "Invalid credentials" OR "Access Denied"
- **Cause**: AWS credentials not configured OR insufficient IAM permissions
- **Fix**: Check AWS credentials (env vars, ~/.aws/credentials, SSO), verify IAM role/user permissions

**Issue**: "Region not specified"
- **Cause**: Missing `--region` flag in command
- **Fix**: Add `--region us-west-2` (or appropriate region) to command

**Issue**: "Command not allowed (write operation)"
- **Cause**: Attempting Create/Delete/Update operation with READ_OPERATIONS_ONLY=true
- **Fix**: aws-expert provides recommendations, human implements via AWS Console or AWS CLI directly

**Issue**: "Documentation search returns no results"
- **Cause**: Search terms too specific OR service documentation uses different terminology
- **Fix**: Try broader search terms, check AWS docs site for correct terminology

**Issue**: "Documentation page redirects to different host"
- **Cause**: AWS docs moved or URL structure changed
- **Fix**: Use redirect URL provided in error message for new `read_documentation` call

---

## 📊 Confidence Levels

| Operation | Confidence | Notes |
|-----------|------------|-------|
| call_aws (describe/list/get) | HIGH (0.92) | Standard infrastructure queries |
| suggest_aws_commands | HIGH (0.88) | RAG-based command discovery |
| search_documentation | HIGH (0.95) | Official AWS docs search |
| read_documentation | HIGH (0.92) | Current documentation access |
| recommend | HIGH (0.90) | Related content discovery |

---

## 🎓 When to Delegate to aws-expert

**Direct use OK** (data-engineer-role, ui-ux-developer-role):
- ✅ List resources (EC2, ECS, S3, Lambda)
- ✅ Get service details (describe operations)
- ✅ Search documentation for known service
- ✅ Read specific documentation pages

**Delegate to specialist** (confidence <0.60):
- ❌ Complex multi-service architecture decisions
- ❌ Security configuration recommendations
- ❌ Cost optimization analysis
- ❌ Performance tuning (EC2 sizing, Lambda config)
- ❌ Infrastructure design (network, IAM, resource organization)
- ❌ Deployment strategy (Blue/Green, Canary, Rolling)

---

## 📚 Related Resources

- **Full AWS API Documentation**: `knowledge/mcp-servers/aws-api/`
- **Full AWS Docs Documentation**: `knowledge/mcp-servers/aws-docs/`
- **aws-expert Agent**: `.claude/agents/specialists/aws-expert.md`
- **MCP Integration Guide**: `.claude/memory/patterns/agent-mcp-integration-guide.md`
- **AWS CLI Reference**: https://docs.aws.amazon.com/cli/

---

## 🔗 Integration Patterns

### With aws-docs (Documentation-First Pattern)
```
1. search_documentation → Find relevant guides
2. read_documentation → Understand current best practices
3. recommend → Discover related content
4. call_aws → Validate current state
5. aws-expert → Provide recommendations
```

### With dbt-mcp + snowflake-mcp (Data Platform)
```
1. call_aws → Check RDS/DMS infrastructure
2. snowflake-mcp → Validate Snowflake resources
3. dbt-mcp → Check transformation jobs
4. aws-expert → Optimize cross-platform architecture
```

### With github-mcp (Infrastructure as Code)
```
1. call_aws → Get current infrastructure state
2. github-mcp → Read CloudFormation/Terraform templates
3. aws-expert → Recommend infrastructure updates
4. github-mcp → Create PR with recommendations
```

---

## 🌟 Key Differentiators

**aws-api vs Direct AWS CLI**:
- ✅ MCP: Safer (READ_OPERATIONS_ONLY prevents accidents)
- ✅ MCP: Integrated with Claude Code workflow
- ✅ MCP: Command validation before execution
- ❌ MCP: No write operations (aws-expert recommends, human implements)

**aws-docs vs Web Search**:
- ✅ aws-docs: CURRENT documentation (post-training cutoff)
- ✅ aws-docs: Official AWS content only
- ✅ aws-docs: Structured markdown output
- ✅ aws-docs: Related content discovery
- ❌ Web Search: May return outdated information

---

*Created: 2025-10-08*
*Last Updated: 2025-10-08*
*Quick Reference for rapid MCP tool lookup*
