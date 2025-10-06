# MCP Tools vs Specialist Agents: Quick Decision Tree

**Purpose**: Fast reference for when to use MCP tools directly vs delegate to specialist agents

---

## Decision Flow

```
┌─────────────────────────────────────────────────────┐
│  TASK ARRIVES AT PRIMARY ROLE (e.g., ui-ux-developer) │
└─────────────────────────────────────────────────────┘
                          ↓

┌─────────────────────────────────────────────────────┐
│  Does task require domain expertise?                │
│  (AWS, data architecture, security, etc.)           │
└─────────────────────────────────────────────────────┘
           ↓ NO                          ↓ YES

┌────────────────────┐          ┌────────────────────────────┐
│ Primary role       │          │ Continue to expertise      │
│ handles directly   │          │ assessment →               │
└────────────────────┘          └────────────────────────────┘
                                             ↓

                    ┌────────────────────────────────────────────┐
                    │  Is this ONLY information lookup?          │
                    │  (No decisions, just facts)                │
                    └────────────────────────────────────────────┘
                              ↓ YES              ↓ NO

                    ┌──────────────────┐    ┌────────────────────┐
                    │ Consider: Could  │    │ DELEGATE TO        │
                    │ use MCP directly │    │ SPECIALIST AGENT   │
                    │                  │    │                    │
                    │ BUT for         │    │ ✓ Architectural    │
                    │ CORRECTNESS:     │    │   decisions        │
                    │ Still delegate   │    │ ✓ Multi-service    │
                    │ to specialist    │    │   coordination     │
                    └──────────────────┘    │ ✓ Security config  │
                              ↓             │ ✓ Performance opt  │
                              │             │ ✓ Cost analysis    │
                              ↓             │ ✓ Debugging        │
                    ┌──────────────────┐    └────────────────────┘
                    │ DELEGATE TO      │             ↓
                    │ SPECIALIST       │
                    │ (when in doubt)  │
                    └──────────────────┘
                              ↓                      ↓

            ┌───────────────────────────────────────────────────┐
            │  SPECIALIST AGENT (e.g., aws-expert)              │
            │                                                   │
            │  1. Uses MCP tools in parallel:                   │
            │     ├─ aws-knowledge (docs, best practices)       │
            │     ├─ aws-api (infrastructure state)             │
            │     └─ Other domain-specific tools                │
            │                                                   │
            │  2. Applies domain expertise:                     │
            │     ├─ Interprets MCP data                        │
            │     ├─ Applies architectural patterns             │
            │     ├─ Considers trade-offs                       │
            │     └─ Synthesizes recommendations                │
            │                                                   │
            │  3. Returns expert recommendation                 │
            └───────────────────────────────────────────────────┘
                              ↓

            ┌───────────────────────────────────────────────────┐
            │  PRIMARY ROLE executes with confidence            │
            │  ✓ Expert-validated approach                      │
            │  ✓ Complete context and rationale                 │
            │  ✓ Reduced error risk                             │
            └───────────────────────────────────────────────────┘
```

---

## Quick Reference: MCP vs Specialist

### ✅ Use MCP Tools Directly (Rare - Usually still delegate)

**Simple Information Lookup** (but delegation is safer):
```
Question: "What AWS regions support ECS Fargate?"
Answer: Simple fact lookup from aws-knowledge MCP
Risk: Low (factual query)
Recommendation: Could use directly, but specialist can validate context
```

**Well-Defined Operations** (with caution):
```
Task: "List all S3 buckets in us-east-1"
Tool: aws-api MCP with clear parameters
Risk: Low (read-only query)
Recommendation: Safe for primary role if no decisions needed
```

### ✅ Delegate to Specialist (Default - Correctness First)

**Architectural Decisions**:
```
Task: "Should we use ECS or Lambda for this React app?"
Why Specialist: Requires cost/performance/complexity trade-off analysis
Tools Specialist Uses: aws-knowledge (best practices) + aws-api (current state)
```

**Multi-Service Coordination**:
```
Task: "Set up ALB → ECS → RDS deployment"
Why Specialist: Requires understanding service interactions, security, networking
Tools Specialist Uses: aws-api (config all services) + aws-knowledge (patterns)
```

**Security Configuration**:
```
Task: "Configure IAM policies for ECS task"
Why Specialist: Requires least-privilege principle, compliance knowledge
Tools Specialist Uses: aws-knowledge (security best practices) + aws-api (validate)
```

**Performance Optimization**:
```
Task: "Our ECS tasks are slow"
Why Specialist: Requires domain knowledge to diagnose and optimize
Tools Specialist Uses: aws-api (metrics) + aws-knowledge (optimization patterns)
```

**Cost Analysis**:
```
Task: "Reduce AWS costs for our deployment"
Why Specialist: Requires understanding cost levers and business trade-offs
Tools Specialist Uses: aws-api (current usage) + aws-knowledge (cost optimization)
```

**Complex Debugging**:
```
Task: "Deployment is failing with intermittent errors"
Why Specialist: Requires systematic investigation and domain expertise
Tools Specialist Uses: aws-api (logs, states) + aws-knowledge (troubleshooting)
```

---

## Pattern Comparison: Correctness Analysis

### ❌ ANTI-PATTERN: Role → MCP → Guess

```
ui-ux-developer
    ↓
aws-api MCP: "Show me ECS config"
    ↓
MCP returns: [complex JSON with 50+ parameters]
    ↓
ui-ux-developer: "I'll change this value... probably?"
    ↓
❌ High risk of errors
❌ No architectural validation
❌ Missing security considerations
❌ Potential production issues
```

**Token Cost**: Lower
**Latency**: Faster
**Quality**: Poor
**Error Risk**: HIGH

---

### ✅ RECOMMENDED: Role → Specialist (with MCP)

```
ui-ux-developer: "Need to update ECS deployment"
    ↓
Delegate to: aws-expert
    ↓
aws-expert parallel tool usage:
    ├─ aws-api: Get current ECS task definition
    ├─ aws-api: Get ALB configuration
    ├─ aws-api: Get security group rules
    ├─ aws-knowledge: Search ECS best practices
    └─ aws-knowledge: Get Well-Architected guidance
    ↓
aws-expert synthesis:
    ├─ Analyzes current vs optimal configuration
    ├─ Identifies security gaps
    ├─ Calculates cost impact
    ├─ Validates performance settings
    └─ Creates deployment plan
    ↓
aws-expert returns: [complete, validated recommendation]
    ↓
ui-ux-developer: Executes with confidence
    ↓
✓ Expert validation
✓ Comprehensive analysis
✓ Security validated
✓ Cost optimized
✓ Low error risk
```

**Token Cost**: Higher (15x in multi-agent systems per Anthropic)
**Latency**: Slower
**Quality**: Excellent
**Error Risk**: LOW

---

## When In Doubt: The Correctness-First Rule

```
╔═══════════════════════════════════════════════════════╗
║  GOLDEN RULE: Delegate to Specialist                  ║
║                                                       ║
║  Delegating to specialist is NOT added complexity.    ║
║  It's proper separation of concerns.                  ║
║                                                       ║
║  Using tools without expertise IS added complexity.   ║
║  It requires learning, interpreting, deciding         ║
║  outside your domain.                                 ║
╚═══════════════════════════════════════════════════════╝
```

### Cost of Wrong Decision:

**Using MCP directly when specialist needed**:
- ❌ Incorrect configuration deployed
- ❌ Security vulnerabilities introduced
- ❌ Production downtime
- ❌ Hours of debugging
- ❌ Loss of user trust
- ❌ Potential data loss

**Using specialist when MCP direct might work**:
- ✓ Slight increase in tokens (acceptable cost)
- ✓ Slight increase in latency (seconds, not hours)
- ✓ Expert validation (peace of mind)
- ✓ Learning opportunity (specialist explains reasoning)

**The math is simple: Always delegate when AWS expertise needed.**

---

## Real-World Examples

### Example 1: Simple Lookup (Could use MCP, but delegate is safer)

**Task**: "What's the latest version of AWS SDK for JavaScript?"

**Option A - Direct MCP**:
```
ui-ux-developer → aws-knowledge MCP → Get answer
Risk: Low (simple fact)
```

**Option B - Via Specialist**:
```
ui-ux-developer → aws-expert → aws-expert uses aws-knowledge → Get answer + context
Benefit: Specialist also mentions breaking changes, migration notes, compatibility
```

**Recommendation**: Option B for quality, but Option A is acceptable if time-critical

---

### Example 2: Architectural Decision (MUST use specialist)

**Task**: "Should I use ECS Fargate or EC2 launch type for our React app?"

**Option A - Direct MCP** ❌:
```
ui-ux-developer → aws-knowledge MCP → Get generic comparison
→ User must interpret trade-offs
→ Lacks specific use case analysis
→ May choose incorrectly
```

**Option B - Via Specialist** ✅:
```
ui-ux-developer → aws-expert
    ↓
aws-expert analysis:
    ├─ aws-knowledge: Get Fargate vs EC2 comparison
    ├─ aws-api: Check current workload patterns
    ├─ Domain expertise: Analyze cost for this specific workload
    ├─ Domain expertise: Consider operational overhead
    └─ Domain expertise: Evaluate future scaling needs
    ↓
aws-expert recommendation:
    "Use Fargate for this React app because:
     - Your workload is stateless (good for Fargate)
     - You lack DevOps team to manage EC2 (Fargate reduces ops)
     - Cost is 10% higher but operational savings are 40%
     - Scaling is automatic (fits your traffic pattern)

     If budget is critical: Consider EC2 with auto-scaling, but
     requires hiring DevOps engineer (negates cost savings)."
```

**Recommendation**: ALWAYS use specialist for architectural decisions

---

### Example 3: Debugging (MUST use specialist)

**Task**: "ECS deployment failing: 'CannotPullContainerError'"

**Option A - Direct MCP** ❌:
```
ui-ux-developer → aws-knowledge MCP → Search error
→ MCP returns: "Could be IAM, ECR permissions, or network"
→ User tries random fixes
→ Hours of trial and error
```

**Option B - Via Specialist** ✅:
```
ui-ux-developer → aws-expert
    ↓
aws-expert systematic investigation:
    1. aws-api: Get ECS task definition (check image URI)
    2. aws-api: Check IAM task execution role (validate ECR permissions)
    3. aws-api: Check VPC/subnet configuration (validate NAT/internet access)
    4. aws-api: Check ECR repository permissions (cross-account?)
    5. aws-knowledge: Review common CannotPullContainerError causes
    6. Synthesize: "Issue is IAM role lacks ecr:GetAuthorizationToken"
    ↓
aws-expert provides:
    - Root cause: Specific IAM permission missing
    - Fix: Exact IAM policy to add
    - Validation: How to verify fix worked
    - Prevention: Checklist for future deployments
```

**Recommendation**: ALWAYS use specialist for debugging

---

## Summary Decision Matrix

| Task Type | Use MCP Direct? | Delegate to Specialist? | Reasoning |
|-----------|----------------|------------------------|-----------|
| **Simple fact lookup** | Maybe (but delegate safer) | ✅ Recommended | Specialist adds context |
| **Architectural decision** | ❌ Never | ✅ Required | Needs expertise to interpret |
| **Multi-service config** | ❌ Never | ✅ Required | Needs understanding of interactions |
| **Security setup** | ❌ Never | ✅ Required | Requires compliance knowledge |
| **Performance tuning** | ❌ Never | ✅ Required | Needs domain-specific optimization |
| **Cost optimization** | ❌ Never | ✅ Required | Requires business trade-off analysis |
| **Debugging** | ❌ Never | ✅ Required | Needs systematic investigation |
| **Infrastructure as Code** | ❌ Never | ✅ Required | Requires template best practices |

---

## Implementation Checklist

### For DA Agent Hub:

**1. Configure Specialist Agents with MCP Tools**:
```yaml
aws-expert:
  tools:
    - aws-knowledge (MCP)
    - aws-api (MCP)
    - File operations (for IaC)
  expertise:
    - AWS Well-Architected Framework
    - Cost optimization
    - Security best practices
    - Performance tuning
```

**2. Train Primary Roles to Delegate**:
```yaml
ui-ux-developer:
  delegation_pattern: |
    When AWS infrastructure is mentioned:
    1. Immediately delegate to aws-expert
    2. Do NOT attempt to use aws-api or aws-knowledge MCP directly
    3. Let specialist use tools with domain expertise
    4. Execute specialist's recommendations
```

**3. Document Specialist Usage Patterns**:
- Create runbook: "When to consult aws-expert"
- Add examples: Real scenarios from projects
- Track quality: Specialist recommendations vs direct tool usage

**4. Measure Correctness Improvements**:
- Track: Deployment failures before vs after specialist pattern
- Measure: Time to resolution with specialist vs trial-and-error
- Calculate: Token cost vs error cost (errors are expensive)

---

**Document Purpose**: Quick decision tree for MCP vs specialist delegation
**Primary Rule**: When in doubt, delegate to specialist
**Quality Priority**: Correctness > Speed ✓
