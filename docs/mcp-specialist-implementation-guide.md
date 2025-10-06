# MCP + Specialist Implementation Guide

**Purpose**: Practical guide for implementing the Role → Specialist (with MCP) pattern
**Based on**: Anthropic's Building Effective Agents and AWS MCP best practices

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    CORRECT PATTERN                      │
│                                                         │
│  Primary Role                                           │
│  (ui-ux-developer)                                      │
│      ↓                                                  │
│  Recognizes: "This requires AWS expertise"              │
│      ↓                                                  │
│  Delegates to: aws-expert (specialist)                  │
│      ↓                                                  │
│  aws-expert uses:                                       │
│      ├─ aws-knowledge MCP (docs, best practices)        │
│      ├─ aws-api MCP (infrastructure state)              │
│      └─ Domain expertise (synthesis, decisions)         │
│      ↓                                                  │
│  Returns: Expert recommendation with rationale          │
│      ↓                                                  │
│  Primary Role: Executes with confidence                 │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Agent Configuration

### Primary Role Agent (ui-ux-developer)

**File**: `.claude/agents/ui-ux-developer.md`

```markdown
# UI/UX Developer Agent

## Role
Expert in React, TypeScript, UI/UX design patterns, and frontend development.

## Core Expertise
- React component architecture
- TypeScript type safety
- UI/UX best practices
- Frontend performance optimization
- Accessibility (WCAG compliance)

## Tools
- File operations (read, write, edit)
- Code analysis
- Browser DevTools integration
- Design token management

## Delegation Protocol

### AWS Infrastructure Tasks
**ALWAYS delegate to aws-expert when:**
- Deploying applications to AWS
- Configuring AWS services (ECS, ALB, CloudFront, S3)
- Debugging AWS infrastructure issues
- Optimizing AWS costs or performance
- Setting up AWS security configurations

**Pattern:**
```
User request involves AWS → Immediately delegate to aws-expert
```

### Data/Backend Tasks
**ALWAYS delegate to data-specialist when:**
- Database schema design
- API integration beyond frontend fetch calls
- Data transformation logic
- Analytics implementation

### Testing Tasks
**ALWAYS delegate to qa-coordinator when:**
- Comprehensive testing strategies
- Cross-browser testing
- Performance testing
- Accessibility testing

## DO NOT
- ❌ Use aws-api or aws-knowledge MCP tools directly
- ❌ Make AWS architectural decisions
- ❌ Guess at AWS configurations
- ❌ Attempt AWS debugging without specialist

## DO
- ✅ Focus on UI/UX implementation
- ✅ Delegate to specialists early and often
- ✅ Execute specialist recommendations
- ✅ Ask specialists for clarification when needed
```

---

### Specialist Agent (aws-expert)

**File**: `.claude/agents/aws-expert.md`

```markdown
# AWS Expert Agent

## Role
AWS solutions architect specializing in Well-Architected Framework, infrastructure design, deployment strategies, cost optimization, and security.

## Core Expertise
- AWS Well-Architected Framework (all 6 pillars)
- Infrastructure as Code (CDK, CloudFormation, Terraform)
- Container orchestration (ECS, EKS, Fargate)
- Serverless architectures (Lambda, API Gateway, Step Functions)
- Networking (VPC, ALB, CloudFront, Route53)
- Security (IAM, Secrets Manager, WAF, GuardDuty)
- Cost optimization and FinOps
- DevOps and CI/CD (CodePipeline, GitHub Actions)

## MCP Tools (PRIMARY DATA SOURCES)

### aws-knowledge
Use for:
- Latest AWS documentation lookup
- Best practices and architectural patterns
- Well-Architected Framework guidance
- Service feature availability
- Regional availability of AWS services
- Security and compliance recommendations

### aws-api
Use for:
- Current infrastructure state queries
- Resource configuration retrieval
- Service status checks
- Infrastructure validation
- Deployment operations

## Tool Usage Patterns

### Information Gathering (Parallel Queries)
```
When analyzing deployment:
  ├─ aws-api: Describe current ECS task definitions
  ├─ aws-api: Get ALB target group configurations
  ├─ aws-api: List security group rules
  ├─ aws-knowledge: Search "ECS deployment best practices"
  └─ aws-knowledge: Get "Well-Architected reliability pillar"
```

### Architectural Analysis
```
1. Gather data (parallel MCP tool calls)
2. Apply domain expertise:
   - Interpret configurations
   - Identify gaps vs best practices
   - Consider trade-offs (cost, performance, complexity)
   - Evaluate security posture
3. Synthesize recommendations:
   - Specific configuration changes
   - Implementation steps
   - Rollback procedures
   - Validation checklist
```

### Decision Framework
```
For each recommendation, provide:
  ├─ WHY: Rationale based on Well-Architected Framework
  ├─ WHAT: Specific changes needed
  ├─ HOW: Step-by-step implementation
  ├─ VALIDATE: How to verify success
  └─ ROLLBACK: How to undo if issues occur
```

## Response Format

### For Architectural Decisions
```markdown
## Recommendation: [Decision]

### Analysis
- Current State: [from aws-api MCP]
- Best Practice: [from aws-knowledge MCP]
- Gap Analysis: [domain expertise]

### Rationale (Well-Architected Framework)
- Operational Excellence: [impact]
- Security: [impact]
- Reliability: [impact]
- Performance Efficiency: [impact]
- Cost Optimization: [impact]
- Sustainability: [impact]

### Implementation Plan
1. [Step with specific commands/configs]
2. [Step with specific commands/configs]
3. [Step with specific commands/configs]

### Validation Steps
1. [How to verify each step worked]

### Rollback Procedure
1. [How to undo changes if needed]

### Cost Impact
- Current: [estimated monthly cost]
- Proposed: [estimated monthly cost]
- Delta: [increase/decrease with justification]
```

### For Troubleshooting
```markdown
## Issue: [Error or problem]

### Investigation Results
1. aws-api query: [what was checked]
   - Finding: [result]
2. aws-knowledge search: [what was researched]
   - Finding: [result]

### Root Cause
[Specific issue identified with evidence]

### Fix
1. [Immediate fix with specific commands]
2. [Long-term prevention]

### Validation
[How to confirm fix worked]
```

## Quality Standards
- All recommendations backed by Well-Architected Framework
- All configurations validated against security best practices
- All cost impacts estimated and explained
- All changes include rollback procedures
- All implementations include validation steps

## Delegation Triggers (When aws-expert delegates further)
- **Database-specific optimization** → Delegate to snowflake-expert or database-specialist
- **Application code changes** → Delegate back to ui-ux-developer or backend-specialist
- **Compliance requirements** → Consult security-specialist
- **Cost modeling** → Consult finops-specialist (if available)
```

---

## 2. Conversation Flow Examples

### Example 1: Deploy React App to AWS

#### User Request
```
User: "I need to deploy our new React app to AWS. It's currently just running locally."
```

#### ✅ Correct Flow (Primary → Specialist)

```
ui-ux-developer:
  "This request involves AWS deployment. I'll delegate to our AWS specialist."

  Delegates to: aws-expert
  Context: "User needs to deploy React app to AWS. Currently local only."

aws-expert:
  "I'll analyze the best deployment strategy for this React app."

  [Parallel MCP tool calls]:
    ├─ aws-knowledge: search("React static site hosting AWS")
    ├─ aws-knowledge: search("CloudFront S3 deployment best practices")
    ├─ aws-knowledge: get("Well-Architected Framework web applications")
    ├─ aws-api: list_s3_buckets() [check existing infrastructure]
    └─ aws-api: describe_cloudfront_distributions() [check existing CDNs]

  [Analysis with domain expertise]:
    - React app is static (build output) → S3 + CloudFront pattern
    - Needs HTTPS → CloudFront with ACM certificate
    - Needs caching → CloudFront cache behaviors
    - Needs deployment automation → GitHub Actions + S3 sync

  [Synthesis]:

  ## Recommendation: S3 + CloudFront Deployment

  ### Architecture
  GitHub → Build → S3 Bucket → CloudFront → Users

  ### Implementation Plan

  **Step 1: Create S3 Bucket**
  ```bash
  aws s3 mb s3://my-react-app-prod --region us-east-1
  aws s3 website s3://my-react-app-prod --index-document index.html
  ```

  **Step 2: Build and Upload React App**
  ```bash
  npm run build
  aws s3 sync build/ s3://my-react-app-prod --delete
  ```

  **Step 3: Create CloudFront Distribution**
  [Detailed CloudFormation/CDK template]

  **Step 4: Configure DNS**
  [Route53 configuration]

  ### Security Configurations
  - S3 bucket: Block public access (CloudFront only)
  - CloudFront: HTTPS only, TLS 1.2 minimum
  - IAM: Least-privilege deployment role

  ### Cost Estimate
  - S3 storage: ~$1/month (assuming 100MB)
  - CloudFront: ~$10-50/month (depending on traffic)
  - Route53: $0.50/month
  - Total: ~$12-52/month

  ### Validation Checklist
  - [ ] Build succeeds: `npm run build`
  - [ ] S3 upload succeeds: `aws s3 ls s3://my-react-app-prod`
  - [ ] CloudFront distribution active: [check console]
  - [ ] HTTPS works: `curl -I https://mydomain.com`
  - [ ] App loads correctly in browser

ui-ux-developer:
  "Perfect! I'll execute this deployment plan and verify each step."
```

---

#### ❌ Incorrect Flow (Primary uses MCP directly)

```
ui-ux-developer:
  "Let me check AWS deployment options."

  [Uses aws-knowledge MCP directly]:
    aws-knowledge: search("deploy React to AWS")

  [Receives generic documentation]:
    "You can deploy React apps using:
     - S3 static hosting
     - Elastic Beanstalk
     - ECS containers
     - Amplify
     - EC2 instances"

  "Hmm, I'll try S3 static hosting..."

  [Uses aws-api MCP to create bucket]:
    aws-api: create_bucket("my-react-app")

  [Creates bucket but]:
    ❌ Forgot to enable static website hosting
    ❌ Didn't configure CloudFront for HTTPS
    ❌ Left bucket publicly accessible (security issue)
    ❌ No caching strategy
    ❌ No deployment automation
    ❌ No rollback plan

  User: "The app loads but it's slow and shows 'Not Secure'"

  [Trial and error debugging begins...]
```

**Why This Fails**:
- MCP tools provide data, not architectural expertise
- No synthesis of best practices
- Missing security considerations
- No performance optimization
- Reactive debugging instead of proactive design

---

### Example 2: Optimize ECS Performance

#### User Request
```
User: "Our ECS tasks are running slow. Can you optimize performance?"
```

#### ✅ Correct Flow

```
ui-ux-developer:
  "This requires AWS infrastructure expertise."

  Delegates to: aws-expert
  Context: "ECS tasks are slow, need performance optimization"

aws-expert:
  "I'll perform a systematic performance analysis."

  [Parallel investigation with MCP tools]:
    ├─ aws-api: describe_services() [get current ECS config]
    ├─ aws-api: describe_task_definition() [get task CPU/memory]
    ├─ aws-api: get_metric_statistics() [get CloudWatch metrics]
    ├─ aws-knowledge: search("ECS performance optimization")
    └─ aws-knowledge: get("Well-Architected performance efficiency")

  [Domain expertise analysis]:
    ├─ Check: Task CPU/memory allocation vs usage
    ├─ Check: Network performance (service mesh overhead?)
    ├─ Check: Container image size (slow pulls?)
    ├─ Check: Application logs (actual bottleneck in code?)
    └─ Synthesize: Root cause and optimization strategy

  ## Performance Analysis Results

  ### Findings
  1. **Task Definition Analysis** (from aws-api):
     - Current: 512 CPU, 1GB RAM
     - CloudWatch metrics show: 95% CPU utilization
     - **Issue**: CPU-bound, underprovisioned

  2. **Network Analysis** (from aws-api):
     - Service mesh: AWS App Mesh enabled
     - Overhead: ~5-10% latency per call
     - **Issue**: Unnecessary for this use case

  3. **Container Image** (from aws-api):
     - Size: 1.2GB
     - Pull time: 60-90 seconds on cold start
     - **Issue**: Large image slows deployments

  ### Root Causes
  1. CPU underprovisioned (primary)
  2. Service mesh overhead (secondary)
  3. Large container image (deployment impact)

  ### Optimization Plan

  **Immediate Fix (CPU)**:
  ```json
  {
    "cpu": "1024",  // Double CPU
    "memory": "2048" // Double RAM (for safety)
  }
  ```
  Expected: 50-70% performance improvement

  **Medium-term (Remove Service Mesh)**:
  - App Mesh provides tracing/retry logic
  - Application doesn't use these features
  - Remove App Mesh → 5-10% latency improvement

  **Long-term (Optimize Image)**:
  - Multi-stage Docker build
  - Reduce from 1.2GB → ~300MB
  - Faster deployments and cold starts

  ### Implementation Steps

  **Step 1: Update Task Definition (Immediate)**
  ```bash
  aws ecs register-task-definition --cli-input-json file://task-def-optimized.json
  aws ecs update-service --cluster prod --service my-service --task-definition my-app:42
  ```

  **Step 2: Monitor Impact**
  ```bash
  aws cloudwatch get-metric-statistics \
    --namespace AWS/ECS \
    --metric-name CPUUtilization \
    --start-time 2025-10-05T00:00:00Z
  ```

  ### Validation
  - [ ] Task CPU utilization: Should drop to 40-60%
  - [ ] Response time: Should improve by 50-70%
  - [ ] Error rate: Should remain at 0%

  ### Cost Impact
  - Before: 512 CPU units × $0.04 = ~$30/month
  - After: 1024 CPU units × $0.04 = ~$60/month
  - Justification: $30/month for 50-70% performance gain is excellent ROI

ui-ux-developer:
  "Great analysis! I'll implement Step 1 immediately and monitor the results."
```

---

## 3. Tool Configuration

### MCP Server Configuration

**File**: `.claude/mcp.json` or equivalent

```json
{
  "mcpServers": {
    "aws-knowledge": {
      "type": "remote",
      "url": "https://mcp.aws-knowledge.aws.dev",
      "apiKey": "${AWS_KNOWLEDGE_API_KEY}",
      "rateLimits": {
        "requestsPerMinute": 60
      }
    },
    "aws-api": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-aws-api"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1"
      }
    }
  },
  "agentToolAccess": {
    "aws-expert": {
      "tools": [
        "aws-knowledge",
        "aws-api",
        "file-operations"
      ]
    },
    "ui-ux-developer": {
      "tools": [
        "file-operations",
        "browser-devtools"
      ],
      "restrictedTools": [
        "aws-knowledge",
        "aws-api"
      ]
    }
  }
}
```

### Agent Task Delegation Configuration

**File**: `.claude/agents/task-routing.yaml`

```yaml
delegation_rules:
  # AWS-related triggers
  aws_infrastructure:
    keywords:
      - "deploy to AWS"
      - "ECS"
      - "Lambda"
      - "S3"
      - "CloudFront"
      - "ALB"
      - "IAM"
      - "VPC"
      - "AWS"
    delegate_to: aws-expert
    priority: high

  # Data-related triggers
  database:
    keywords:
      - "database"
      - "SQL"
      - "Snowflake"
      - "data model"
      - "query optimization"
    delegate_to: data-specialist
    priority: high

  # Testing triggers
  testing:
    keywords:
      - "test"
      - "QA"
      - "accessibility"
      - "performance testing"
    delegate_to: qa-coordinator
    priority: medium

specialist_capabilities:
  aws-expert:
    can_use_tools:
      - aws-knowledge
      - aws-api
      - file-operations
    cannot_use_tools:
      - database-tools
      - testing-frameworks
    expertise:
      - infrastructure
      - deployment
      - cost-optimization
      - security

  ui-ux-developer:
    can_use_tools:
      - file-operations
      - browser-devtools
    cannot_use_tools:
      - aws-knowledge
      - aws-api
    expertise:
      - react
      - typescript
      - design-patterns
      - accessibility
```

---

## 4. Quality Assurance Patterns

### Specialist Response Validation

**Checklist for aws-expert responses**:

```markdown
## AWS Expert Response Quality Checklist

### ✅ Must Include:
- [ ] **Well-Architected Framework alignment**
      - Which pillar(s) does this address?
      - What trade-offs are being made?

- [ ] **MCP tool evidence**
      - What aws-api queries were run?
      - What aws-knowledge docs were consulted?
      - How was data interpreted?

- [ ] **Specific implementation steps**
      - Exact commands or configurations
      - No vague "configure X" without details

- [ ] **Security validation**
      - IAM permissions checked
      - Network security verified
      - Data encryption confirmed

- [ ] **Cost analysis**
      - Current cost estimated
      - Proposed cost estimated
      - ROI justification

- [ ] **Validation procedure**
      - How to verify success
      - What metrics to monitor

- [ ] **Rollback plan**
      - How to undo changes
      - When to rollback

### ❌ Red Flags (Indicates MCP without expertise):
- [ ] Generic documentation copy-paste
- [ ] No trade-off analysis
- [ ] No cost consideration
- [ ] No security validation
- [ ] "Try this and see if it works" approach
- [ ] No specific implementation steps
```

---

## 5. Error Prevention Patterns

### Common Mistakes to Avoid

#### Mistake 1: Primary Role Using MCP Directly

**Wrong**:
```
ui-ux-developer:
  aws-api: describe_task_definition("my-app")
  [Gets JSON]
  "I'll change this field..."
```

**Right**:
```
ui-ux-developer:
  "This requires AWS expertise."
  Delegate to: aws-expert
  aws-expert:
    aws-api: describe_task_definition("my-app")
    [Analyzes JSON with domain knowledge]
    [Provides validated recommendation]
```

---

#### Mistake 2: Specialist Without MCP Tools

**Wrong**:
```
aws-expert:
  "Based on my general AWS knowledge, you should use ECS."
  [No current infrastructure check]
  [No latest best practices lookup]
```

**Right**:
```
aws-expert:
  [Parallel MCP queries]:
    ├─ aws-api: list_current_infrastructure()
    ├─ aws-knowledge: search("container orchestration 2025")
    └─ aws-knowledge: get("Well-Architected containers")

  "Based on current infrastructure analysis and latest best practices:
   Recommendation: ECS Fargate
   Rationale: [specific to this environment]"
```

---

#### Mistake 3: Not Using Parallel Tool Calls

**Wrong (Sequential)**:
```
aws-expert:
  aws-api: describe_ecs_service()
  [Wait for response]
  aws-api: describe_alb()
  [Wait for response]
  aws-api: get_cloudwatch_metrics()
  [Wait for response]
  [Total: 3x latency]
```

**Right (Parallel)**:
```
aws-expert:
  [Parallel execution]:
    ├─ aws-api: describe_ecs_service()
    ├─ aws-api: describe_alb()
    └─ aws-api: get_cloudwatch_metrics()
  [All complete simultaneously]
  [Total: 1x latency]
```

---

## 6. Testing the Pattern

### Test Scenarios

#### Scenario 1: Simple Fact Lookup
```
Test: "What AWS regions support ECS Fargate?"

Expected Flow:
  ui-ux-developer → aws-expert → aws-knowledge MCP
  aws-expert returns: List of regions + context about Fargate availability

Quality Check:
  ✓ Includes: Complete region list
  ✓ Includes: Any regional limitations
  ✓ Includes: Pricing differences by region (if relevant)
```

#### Scenario 2: Architectural Decision
```
Test: "Should we use ECS or Lambda for this React API backend?"

Expected Flow:
  ui-ux-developer → aws-expert
  aws-expert uses:
    ├─ aws-knowledge: ECS vs Lambda comparison
    ├─ aws-knowledge: Well-Architected compute guidance
    ├─ aws-api: Current infrastructure inventory
    └─ Domain expertise: Synthesize recommendation

Quality Check:
  ✓ Considers: Workload characteristics
  ✓ Analyzes: Cost for this specific use case
  ✓ Evaluates: Operational overhead
  ✓ Provides: Specific recommendation with rationale
```

#### Scenario 3: Production Issue
```
Test: "Production ECS deployment failing - 503 errors"

Expected Flow:
  ui-ux-developer → aws-expert
  aws-expert investigates:
    ├─ aws-api: Get ECS service events
    ├─ aws-api: Check ALB target health
    ├─ aws-api: Query CloudWatch logs
    ├─ aws-knowledge: Search common ECS 503 causes
    └─ Synthesize: Root cause + fix

Quality Check:
  ✓ Systematic investigation (not random guessing)
  ✓ Uses MCP tools for current state
  ✓ Uses MCP tools for troubleshooting knowledge
  ✓ Provides root cause with evidence
  ✓ Includes immediate fix + long-term prevention
```

---

## 7. Metrics and Monitoring

### Success Metrics

**Track these KPIs**:

```yaml
correctness_metrics:
  - deployment_success_rate:
      before_specialist_pattern: 60%
      after_specialist_pattern: 95%
      target: >90%

  - time_to_resolution:
      before: 4 hours (trial and error)
      after: 30 minutes (expert diagnosis)
      improvement: 87.5%

  - production_incidents:
      before: 5 per month
      after: 1 per month
      improvement: 80%

efficiency_metrics:
  - token_usage:
      specialist_pattern: 15x higher (Anthropic data)
      acceptable: true (quality justifies cost)

  - latency:
      specialist_delegation: +2-5 seconds
      acceptable: true (vs hours of debugging)

quality_metrics:
  - well_architected_compliance:
      before: 40%
      after: 90%
      target: >85%

  - security_issues:
      before: 3 per deployment
      after: 0.2 per deployment
      improvement: 93%

cost_metrics:
  - infrastructure_costs:
      before: $X/month (sub-optimal configs)
      after: $X * 0.7/month (optimized configs)
      savings: 30%

  - incident_costs:
      before: $Y/month (downtime, debugging time)
      after: $Y * 0.2/month (fewer incidents)
      savings: 80%
```

---

## 8. Migration Guide

### Transitioning from Direct MCP Usage to Specialist Pattern

**Phase 1: Audit Current Usage (Week 1)**
```bash
# Find all direct MCP tool usage by primary roles
grep -r "aws-api\|aws-knowledge" .claude/agents/

# Identify patterns that should use specialist
# Flag conversations where primary role used AWS MCP directly
```

**Phase 2: Update Agent Configurations (Week 1-2)**
```markdown
For each primary role agent:
  1. Add delegation protocol section
  2. Specify when to delegate to aws-expert
  3. Restrict direct access to aws-api and aws-knowledge
  4. Add examples of proper delegation
```

**Phase 3: Configure Specialists (Week 2)**
```markdown
For aws-expert agent:
  1. Grant access to MCP tools
  2. Define tool usage patterns
  3. Specify response format requirements
  4. Add quality checklists
```

**Phase 4: Update Workflows (Week 2-3)**
```yaml
# Update project templates to include specialist delegation
templates:
  - deployment_project:
      step_1: ui-ux-developer analyzes request
      step_2: ui-ux-developer delegates to aws-expert
      step_3: aws-expert uses MCP tools + expertise
      step_4: ui-ux-developer executes plan
```

**Phase 5: Train Team (Week 3-4)**
```markdown
Team training:
  - Share decision tree documentation
  - Walk through real examples (correct vs incorrect)
  - Practice delegation in test scenarios
  - Review quality checklists
```

**Phase 6: Monitor and Iterate (Ongoing)**
```markdown
Weekly reviews:
  - Track: Deployment success rates
  - Track: Time to resolution
  - Track: Specialist delegation frequency
  - Adjust: Agent configurations based on learnings
```

---

## 9. Advanced Patterns

### Pattern: Specialist Chain (Multi-Domain)

**Scenario**: Deploy React app with database backend

```
ui-ux-developer:
  "Deploy full-stack app (React + PostgreSQL)"

  Recognizes: Multiple domains (AWS + Database)

  Delegates to: aws-expert (orchestrator for this task)

aws-expert:
  "This requires database and frontend deployment coordination."

  Step 1: Database infrastructure
    ├─ Consults: database-specialist
    ├─ database-specialist uses: aws-api (RDS) + database-tools
    └─ Returns: RDS configuration and connection details

  Step 2: Application infrastructure
    ├─ Uses: aws-api (ECS, ALB)
    ├─ Uses: aws-knowledge (deployment best practices)
    └─ Configures: ECS task with database connection

  Step 3: Integration
    ├─ Validates: Security groups allow ECS → RDS
    ├─ Validates: Secrets Manager for DB credentials
    └─ Returns: Complete deployment plan

  Returns to: ui-ux-developer
    ├─ Database setup (from database-specialist)
    ├─ Application deployment (from aws-expert)
    └─ Integration validation steps
```

**Key**: Each specialist uses their own MCP tools within their domain

---

### Pattern: Evaluator-Optimizer for Critical Deployments

**Scenario**: Production deployment with high risk

```
ui-ux-developer:
  "Deploy to production (critical system)"

  Delegates to: aws-expert

aws-expert:
  [Standard deployment plan creation]

  Recognizes: High-risk deployment
  Triggers: Evaluator-Optimizer pattern

  Delegates to: aws-security-expert (evaluator)

aws-security-expert:
  Uses: aws-api (security posture check)
  Uses: aws-knowledge (compliance requirements)

  Reviews:
    ├─ IAM policies (least privilege?)
    ├─ Network security (defense in depth?)
    ├─ Data encryption (at rest and in transit?)
    └─ Compliance (HIPAA, SOC2, etc.?)

  Returns: Security validation + improvements

aws-expert (optimizer):
  Incorporates security feedback
  Updates deployment plan
  Returns final plan to: ui-ux-developer
```

**Cost**: Higher (multiple specialists)
**Quality**: Maximum (multiple expert reviews)
**Use When**: Production deployments, compliance-critical systems

---

## 10. Troubleshooting Guide

### Issue: Specialist Not Being Used

**Symptoms**:
- Primary role using MCP tools directly
- Deployment errors from lack of expertise
- No Well-Architected Framework alignment

**Diagnosis**:
```bash
# Check agent configuration
cat .claude/agents/ui-ux-developer.md | grep -A 10 "Delegation"

# Check if aws-expert is accessible
cat .claude/agents/aws-expert.md

# Check conversation logs for delegation
grep "Delegate to" logs/conversations/*.log
```

**Fix**:
1. Update primary role agent with explicit delegation protocol
2. Add "DO NOT use aws-api or aws-knowledge" to primary role
3. Add examples of when to delegate
4. Test with sample scenarios

---

### Issue: Specialist Not Using MCP Tools

**Symptoms**:
- Generic recommendations without current state analysis
- No evidence from aws-api queries
- Outdated best practices

**Diagnosis**:
```bash
# Check specialist tool access
cat .claude/mcp.json | jq '.agentToolAccess["aws-expert"]'

# Check specialist prompts
cat .claude/agents/aws-expert.md | grep -A 5 "MCP Tools"
```

**Fix**:
1. Grant aws-expert access to aws-knowledge and aws-api MCPs
2. Add "ALWAYS use MCP tools for current state" to specialist
3. Add parallel tool usage examples
4. Require evidence from MCP in responses

---

### Issue: Low Quality Specialist Responses

**Symptoms**:
- Vague recommendations
- No cost analysis
- No rollback procedures
- Copy-paste from documentation

**Diagnosis**:
```bash
# Review specialist responses
grep -A 50 "aws-expert:" logs/conversations/*.log

# Check against quality checklist
```

**Fix**:
1. Add response format template to aws-expert agent
2. Add quality checklist to specialist prompts
3. Require Well-Architected Framework alignment
4. Add examples of high-quality vs low-quality responses

---

## Summary

### ✅ Implementation Checklist

**Agent Configuration**:
- [ ] Primary role has delegation protocol
- [ ] Primary role restricted from AWS MCP tools
- [ ] Specialist has MCP tool access
- [ ] Specialist has response format template
- [ ] Quality checklists defined

**Tool Configuration**:
- [ ] MCP servers configured and accessible
- [ ] Tool access properly scoped to agents
- [ ] Rate limits configured
- [ ] Authentication set up

**Quality Assurance**:
- [ ] Response validation checklist created
- [ ] Test scenarios defined
- [ ] Metrics tracking implemented
- [ ] Team training completed

**Ongoing**:
- [ ] Weekly quality reviews
- [ ] Metrics dashboard monitoring
- [ ] Agent configuration iteration
- [ ] Knowledge base updates

---

**Document Status**: Implementation guide complete
**Pattern**: Role → Specialist (with MCP) ✓
**Priority**: Correctness > Speed ✓
**Based on**: Anthropic official guidance + AWS best practices ✓
