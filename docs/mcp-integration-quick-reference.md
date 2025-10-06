# MCP Integration Quick Reference Card

> **One-page guide for using MCP tools with role-based agents**

---

## 🎯 The Pattern (in 10 seconds)

**Role agents use MCP tools directly. Consult specialists when confidence drops below 0.85.**

```
Role (80%) → MCP Tools → Specialist (20%)
```

---

## 🔧 Available AWS MCP Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **aws-api** | Infrastructure state | List resources, get configs, gather metrics |
| **aws-docs** | Latest documentation | Syntax validation, code examples, service details |
| **aws-knowledge** | Best practices | Well-Architected patterns, security, cost optimization |

---

## 📊 Confidence Decision Tree

```
Task Confidence ≥ 0.85?
    ├─ YES → Use MCP tools directly
    │        └─ Implement solution independently
    │
    └─ NO → Consult specialist
            └─ Collaborate on implementation
```

### Confidence Thresholds

**Independent (≥0.85):**
- Standard ECS/Lambda/ALB configurations ✓
- Common cost optimization patterns ✓
- Well-documented security practices ✓

**Consult Specialist (<0.85):**
- SageMaker ML deployment (0.45) ✗
- EKS Kubernetes management (0.50) ✗
- Step Functions complex workflows (0.55) ✗
- Organizations multi-account (0.48) ✗

---

## 🚀 Quick Start Workflow

### Step 1: Assess Task
```yaml
Question: What's my confidence level on this task?
- ≥0.85: Continue to Step 2
- <0.85: Skip to Step 4 (consult specialist)
```

### Step 2: Select MCP Tool
```yaml
Need current state? → aws-api
Need latest syntax? → aws-docs
Need best practices? → aws-knowledge
```

### Step 3: Execute with MCP
```yaml
1. Query MCP tool(s) directly
2. Analyze results
3. Implement solution
4. Done! (80% of tasks end here)
```

### Step 4: Consult Specialist
```yaml
1. Identify specific gap (e.g., "SageMaker deployment")
2. Consult aws-expert with context
3. Receive expert guidance
4. Collaborate on implementation
5. Done! (20% of tasks need this)
```

---

## 💡 Common Use Cases

### Infrastructure Audit
```
cloud-manager-role
    ↓ aws-api: List all resources
    ↓ aws-knowledge: Get Well-Architected patterns
    ↓ Confidence 0.95? Implement independently ✓
```

### Cost Optimization
```
cloud-manager-role
    ↓ aws-api: Query actual usage
    ↓ aws-knowledge: Get cost patterns
    ↓ Confidence 0.95? Create recommendations ✓
```

### Complex Lambda Pattern
```
cloud-manager-role
    ↓ aws-docs: Get Lambda syntax
    ↓ Confidence 0.65 on cold starts? Consult aws-expert
        ↓ aws-expert: Deep optimization patterns
        ↓ Collaborate on implementation ✓
```

---

## 📈 MCP Confidence Boost

| Task | Before MCP | After MCP | Boost |
|------|------------|-----------|-------|
| Infrastructure audits | 0.65 | 0.95 | +0.30 |
| Cost analysis | 0.89 | 0.95 | +0.06 |
| Security review | 0.70 | 0.90 | +0.20 |
| Compliance validation | 0.60 | 0.88 | +0.28 |

---

## ⚡ Performance Metrics

**Old Architecture (Tool-Specific Agents):**
- 6 agents → 5 handoffs → 3 hours

**New Architecture (Role + MCP + Specialist):**
- 2 agents → 1 optional handoff → 1 hour

**Result: 50-70% faster**

---

## 🔑 Key Principles

### 1. **Direct Access First**
Role agents have direct access to MCP tools within their domain.
- ✓ Reduces coordination overhead
- ✓ Maintains context ownership
- ✓ Enables faster execution

### 2. **Confidence-Driven Delegation**
Explicitly delegate when confidence <0.85.
- ✓ Clear decision criteria
- ✓ Objective threshold
- ✓ Consistent quality

### 3. **80/20 Distribution**
80% handled independently, 20% need consultation.
- ✓ Efficient for most tasks
- ✓ Expertise for edge cases
- ✓ Proven by DA Agent Hub

---

## 🛠️ Implementation Snippet

### For cloud-manager-role.md

```markdown
## MCP Tools Integration

### When I Use MCP Directly (Confidence ≥0.85)

**aws-api MCP:**
- Query infrastructure state
- List ECS/Lambda/ALB/RDS resources
- Get current configurations
- Gather performance metrics

**aws-docs MCP:**
- Validate latest API syntax
- Get code examples
- Check service parameters
- Review current best practices

**aws-knowledge MCP:**
- Query Well-Architected Framework
- Get security best practices
- Find cost optimization patterns
- Review governance guidance

### When I Consult aws-expert (Confidence <0.85)

**Complex Services:**
- SageMaker (0.45) - ML deployment patterns
- EKS (0.50) - Kubernetes management
- Step Functions (0.55) - Complex workflows
- Organizations (0.48) - Multi-account strategies

**Advanced Patterns:**
- Lambda cold start optimization
- VPC endpoint cost analysis
- Multi-region failover design
- Advanced CloudWatch Logs Insights
```

---

## 📋 Checklist for Using MCP

**Before starting:**
- [ ] Assess confidence level on task
- [ ] Identify which MCP tool(s) needed
- [ ] Check if specialist consultation needed

**During execution:**
- [ ] Query MCP tool(s) directly
- [ ] Analyze results for completeness
- [ ] Verify confidence still ≥0.85
- [ ] Implement or consult as appropriate

**After completion:**
- [ ] Document any new patterns learned
- [ ] Update confidence levels if improved
- [ ] Note when specialist was helpful

---

## 🎓 Quick Tips

**Tip 1: MCP enhances, doesn't replace**
Use MCP to boost your existing knowledge, not as a crutch.

**Tip 2: Consult early if uncertain**
Better to consult at 0.80 than struggle at 0.75.

**Tip 3: Document what you learn**
Each specialist consultation is a learning opportunity.

**Tip 4: Combine MCP tools**
Use aws-api (state) + aws-knowledge (patterns) together.

**Tip 5: Update confidence over time**
Track when MCP helps you handle tasks independently.

---

## 📚 Where to Learn More

**Quick reference:** You're reading it! ✓

**Visual learner:** [Architecture Diagrams](./role-mcp-architecture-diagram.md)

**Need context:** [Executive Summary](./role-mcp-integration-summary.md)

**Deep dive:** [Comprehensive Research](./role-based-agent-mcp-integration-research.md)

**Navigation:** [Research Index](./RESEARCH_INDEX.md)

---

## 🚨 Common Mistakes to Avoid

**❌ DON'T:**
- Use specialist as first choice (defeats efficiency gains)
- Ignore confidence thresholds (leads to poor quality)
- Skip MCP tools when available (misses enhancement)
- Delegate without trying MCP first (unnecessary handoffs)

**✓ DO:**
- Try MCP tools first for domain tasks
- Consult specialist when confidence <0.85
- Document patterns for future use
- Update confidence levels over time

---

## 💼 Real-World Example

**Task**: Optimize AWS Lambda cold starts

```bash
# Step 1: Assess
Confidence on Lambda optimization: 0.65
→ Below threshold (0.85), will need specialist

# Step 2: Gather context with MCP
aws-docs MCP: Latest Lambda best practices
aws-knowledge MCP: Performance optimization patterns
→ Now understand problem better

# Step 3: Consult specialist
aws-expert: Deep cold start optimization patterns
→ Provisioned concurrency vs layers vs memory tuning
→ Get specific recommendations

# Step 4: Implement collaboratively
cloud-manager-role + aws-expert guidance
→ Implement optimal solution
→ Document pattern for future (confidence → 0.85)

# Result
✓ High-quality optimization
✓ Knowledge gained for next time
✓ Pattern documented
```

---

**Remember**: Role → MCP → Specialist (when needed)

**Goal**: 80% independent, 20% collaborative, 100% quality

---

Print this page and keep it handy while working with MCP tools! 📄
