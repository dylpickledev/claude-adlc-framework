# MCP + Specialist Visual Architecture Reference

**Quick visual guide to understanding the Role → Specialist (with MCP) pattern**

---

## The Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRIMARY ROLE LAYER                           │
│                  (ui-ux-developer, etc.)                        │
│                                                                 │
│  Responsibilities:                                              │
│    • High-level task coordination                              │
│    • Domain-specific implementation (React, UI/UX)             │
│    • Execution of specialist recommendations                   │
│                                                                 │
│  Does NOT:                                                      │
│    ❌ Use MCP tools for domains outside expertise              │
│    ❌ Make architectural decisions in other domains            │
│    ❌ Debug complex cross-service issues                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    When AWS expertise needed
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    SPECIALIST LAYER                             │
│                  (aws-expert, data-specialist, etc.)            │
│                                                                 │
│  Responsibilities:                                              │
│    • Domain expertise and synthesis                            │
│    • Architectural decision-making                             │
│    • Trade-off analysis (cost, performance, security)          │
│    • Quality assurance and validation                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │  Uses MCP TOOLS as primary data sources:         │          │
│  │                                                   │          │
│  │  ┌─────────────────────────────────────┐         │          │
│  │  │  aws-knowledge (MCP)                │         │          │
│  │  │  • AWS documentation                │         │          │
│  │  │  • Best practices                   │         │          │
│  │  │  • Well-Architected guidance        │         │          │
│  │  │  • Regional availability            │         │          │
│  │  └─────────────────────────────────────┘         │          │
│  │                                                   │          │
│  │  ┌─────────────────────────────────────┐         │          │
│  │  │  aws-api (MCP)                      │         │          │
│  │  │  • Infrastructure state queries     │         │          │
│  │  │  • Service configurations           │         │          │
│  │  │  • Operational commands             │         │          │
│  │  │  • Resource management              │         │          │
│  │  └─────────────────────────────────────┘         │          │
│  │                                                   │          │
│  │  Applies DOMAIN EXPERTISE to:                    │          │
│  │  • Interpret MCP data correctly                  │          │
│  │  • Synthesize architectural decisions            │          │
│  │  • Consider security/cost/performance trade-offs │          │
│  │  • Create validated recommendations              │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                Returns expert recommendation
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PRIMARY ROLE LAYER                           │
│                                                                 │
│  Executes:                                                      │
│    ✓ Expert-validated approach                                 │
│    ✓ Complete context and rationale                            │
│    ✓ Specific implementation steps                             │
│    ✓ Rollback procedures                                       │
│    ✓ Validation checklist                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why This Architecture Works

### MCP Tools = Data Access

```
┌──────────────────────────────────────┐
│         MCP TOOLS                    │
│                                      │
│  PROVIDE:                            │
│  ✓ Real-time data                    │
│  ✓ Documentation                     │
│  ✓ Infrastructure state              │
│  ✓ Latest best practices             │
│                                      │
│  DO NOT PROVIDE:                     │
│  ❌ Expertise interpretation         │
│  ❌ Architectural synthesis          │
│  ❌ Trade-off reasoning              │
│  ❌ Complex decision-making          │
└──────────────────────────────────────┘
```

### Specialist Agents = Expertise

```
┌──────────────────────────────────────┐
│     SPECIALIST AGENTS                │
│                                      │
│  PROVIDE:                            │
│  ✓ Domain expertise                  │
│  ✓ Architectural synthesis           │
│  ✓ Decision-making                   │
│  ✓ Trade-off analysis                │
│  ✓ Quality assurance                 │
│                                      │
│  USE TOOLS FOR:                      │
│  ✓ Current state data                │
│  ✓ Documentation lookup              │
│  ✓ Best practice validation          │
│  ✓ Evidence-based decisions          │
└──────────────────────────────────────┘
```

### Combined = Maximum Quality

```
┌──────────────────────────────────────┐
│   MCP TOOLS + SPECIALIST AGENTS      │
│                                      │
│  = Data + Expertise                  │
│  = Information + Interpretation      │
│  = Facts + Synthesis                 │
│  = Tools + Reasoning                 │
│                                      │
│  RESULT:                             │
│  ✓ Informed decisions                │
│  ✓ Validated architectures           │
│  ✓ Optimized configurations          │
│  ✓ Proactive error prevention        │
│  ✓ High-quality outcomes             │
└──────────────────────────────────────┘
```

---

## Pattern Comparison: Visual Flow

### ❌ ANTI-PATTERN: Role → MCP → Guess

```
┌─────────────────┐
│ ui-ux-developer │
└─────────────────┘
         ↓
    Uses MCP directly
         ↓
┌─────────────────┐       ┌──────────────────────────┐
│  aws-api MCP    │  →    │  Returns: [Complex JSON] │
└─────────────────┘       └──────────────────────────┘
         ↓
    Interprets without expertise
         ↓
┌─────────────────────────────────────┐
│  "I'll change this value... maybe?" │
│                                     │
│  Problems:                          │
│  ❌ No architectural context        │
│  ❌ Missing security considerations │
│  ❌ No cost analysis                │
│  ❌ No performance optimization     │
│  ❌ HIGH ERROR RISK                 │
└─────────────────────────────────────┘
         ↓
      Deploy
         ↓
    💥 Issues in Production
         ↓
    Hours of debugging
```

**Cost**: Lower tokens, higher error risk
**Quality**: Poor
**Outcome**: Production issues, wasted time

---

### ✅ CORRECT PATTERN: Role → Specialist (with MCP)

```
┌─────────────────┐
│ ui-ux-developer │
└─────────────────┘
         ↓
    Recognizes: "AWS expertise needed"
         ↓
    Delegates to specialist
         ↓
┌──────────────────────────────────────────────────────────┐
│                    aws-expert                            │
│                                                          │
│  Step 1: Parallel MCP Tool Usage                        │
│  ┌────────────────────────────────────────────────┐    │
│  │  ├─ aws-api: Get current ECS config            │    │
│  │  ├─ aws-api: Get ALB setup                     │    │
│  │  ├─ aws-api: Get security groups               │    │
│  │  ├─ aws-knowledge: Search best practices       │    │
│  │  └─ aws-knowledge: Get Well-Architected        │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Step 2: Apply Domain Expertise                         │
│  ┌────────────────────────────────────────────────┐    │
│  │  ├─ Interpret MCP data with AWS knowledge      │    │
│  │  ├─ Identify gaps vs best practices            │    │
│  │  ├─ Analyze security posture                   │    │
│  │  ├─ Calculate cost implications                │    │
│  │  └─ Evaluate performance settings              │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Step 3: Synthesize Recommendation                      │
│  ┌────────────────────────────────────────────────┐    │
│  │  ├─ Specific configuration changes             │    │
│  │  ├─ Implementation steps                       │    │
│  │  ├─ Security validation                        │    │
│  │  ├─ Cost impact analysis                       │    │
│  │  ├─ Validation procedures                      │    │
│  │  └─ Rollback plan                              │    │
│  └────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
         ↓
    Returns complete, validated plan
         ↓
┌─────────────────┐
│ ui-ux-developer │
│                 │
│ Executes with:  │
│ ✓ Confidence    │
│ ✓ Full context  │
│ ✓ Clear steps   │
└─────────────────┘
         ↓
      Deploy
         ↓
    ✅ Success
```

**Cost**: Higher tokens (15x), lower error risk
**Quality**: Excellent
**Outcome**: Validated deployment, optimized config, minimal issues

---

## Information Flow Comparison

### Without Specialist (Direct MCP Usage)

```
                    PRIMARY ROLE
                        │
                        ↓
                   ┌────────┐
                   │  MCP   │  →  Raw data
                   └────────┘
                        │
                        ↓
                    Guessing
                        │
                        ↓
                  Potential Errors

        Information: ████░░░░░░ (40% interpreted correctly)
        Decisions:   ██░░░░░░░░ (20% optimal)
        Quality:     ███░░░░░░░ (30% success rate)
```

### With Specialist (Correct Pattern)

```
                    PRIMARY ROLE
                        │
                        ↓
                    SPECIALIST  ←─────┐
                        │             │
                        ↓             │
                   ┌────────┐         │
                   │  MCP   │  →  Raw data
                   └────────┘         │
                        │             │
                        ↓             │
                Domain Expertise      │
                        │             │
                        ↓             │
                Expert Synthesis ─────┘
                        │
                        ↓
                   PRIMARY ROLE
                        │
                        ↓
                  Validated Execution

        Information: ██████████ (100% expert-interpreted)
        Decisions:   █████████░ (90% optimal)
        Quality:     █████████░ (95% success rate)
```

---

## Token Cost vs Error Cost Analysis

### Direct MCP Pattern (Lower Tokens, Higher Risk)

```
┌─────────────────────────────────────────────────┐
│  Token Cost: $X                                 │
│                                                 │
│  But...                                         │
│                                                 │
│  Error Risk:                                    │
│    • Deployment failures:      $XXX            │
│    • Security incidents:       $XXXX           │
│    • Production downtime:      $XXXXX          │
│    • Debugging time:           $XXX            │
│    • Rework costs:             $XX             │
│                                                 │
│  Total Risk Cost:              $XXXXXXXXX      │
│                                                 │
│  NET: Saved $X, Lost $XXXXXXXXX                │
└─────────────────────────────────────────────────┘
```

### Specialist Pattern (Higher Tokens, Lower Risk)

```
┌─────────────────────────────────────────────────┐
│  Token Cost: $X × 15 = $XX                      │
│                                                 │
│  But...                                         │
│                                                 │
│  Benefits:                                      │
│    • Deployment success:       95%             │
│    • Security validated:       100%            │
│    • Optimized config:         +$XXX savings   │
│    • Minimal errors:           -$XXXX avoided  │
│    • Time saved:               -$XXX           │
│                                                 │
│  Total Benefit:                +$XXXXXXX       │
│                                                 │
│  NET: Spent $XX, Gained $XXXXXXX               │
│  ROI: 100x-1000x                               │
└─────────────────────────────────────────────────┘
```

**Conclusion**: Specialist pattern costs more in tokens but saves massively in errors and time.

---

## Multi-Domain Coordination

### Scenario: Full-Stack Deployment (React + Database + AWS)

```
┌────────────────────────────────────────────────────────────────┐
│                      ui-ux-developer                           │
│                 (Primary Orchestrator)                         │
└────────────────────────────────────────────────────────────────┘
                               ↓
              "Deploy full-stack app: React + PostgreSQL + AWS"
                               ↓
                   Recognizes: Multiple domains
                               ↓
              ┌────────────────┴─────────────────┐
              ↓                                  ↓
┌──────────────────────────┐      ┌──────────────────────────┐
│      aws-expert          │      │   database-specialist    │
│                          │      │                          │
│  Parallel MCP Usage:     │      │  Parallel Tool Usage:    │
│  ├─ aws-api (ECS)        │      │  ├─ database-tools       │
│  ├─ aws-api (ALB)        │      │  ├─ aws-api (RDS)        │
│  └─ aws-knowledge        │      │  └─ schema-tools         │
│                          │      │                          │
│  Expertise:              │      │  Expertise:              │
│  ├─ Container deploy     │      │  ├─ Schema design        │
│  ├─ Load balancing       │      │  ├─ Query optimization   │
│  └─ Security             │      │  └─ Data modeling        │
└──────────────────────────┘      └──────────────────────────┘
              ↓                                  ↓
              └────────────────┬─────────────────┘
                               ↓
                      Integration Point
                (Security groups, connection strings)
                               ↓
┌────────────────────────────────────────────────────────────────┐
│                      ui-ux-developer                           │
│                                                                │
│  Receives:                                                     │
│    ├─ Database setup plan (from database-specialist)          │
│    ├─ AWS infrastructure plan (from aws-expert)               │
│    └─ Integration validation (from both)                      │
│                                                                │
│  Executes: Complete deployment with all components validated  │
└────────────────────────────────────────────────────────────────┘
```

**Key**: Each specialist uses their domain's MCP tools, then coordinates at integration points.

---

## Context Isolation Visual

### Without Context Isolation (Primary uses MCP directly)

```
┌──────────────────────────────────────────────────────────┐
│  PRIMARY ROLE CONTEXT (ui-ux-developer)                  │
│                                                          │
│  • React component logic                                │
│  • TypeScript types                                     │
│  • UI/UX patterns                                       │
│  • AWS infrastructure JSON (from MCP)                   │  ← Pollution
│  • Security group rules (from MCP)                      │  ← Pollution
│  • ECS task definitions (from MCP)                      │  ← Pollution
│  • CloudWatch metrics (from MCP)                        │  ← Pollution
│  • More React stuff...                                  │
│  • But confused by AWS details                          │
│                                                          │
│  RESULT: Degraded performance in both domains           │
└──────────────────────────────────────────────────────────┘
```

### With Context Isolation (Specialist pattern)

```
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│  PRIMARY ROLE CONTEXT            │  │  SPECIALIST CONTEXT              │
│  (ui-ux-developer)               │  │  (aws-expert)                    │
│                                  │  │                                  │
│  • React component logic         │  │  • AWS infrastructure state      │
│  • TypeScript types              │  │  • Security configurations       │
│  • UI/UX patterns                │  │  • ECS task definitions          │
│  • Component architecture        │  │  • Well-Architected patterns     │
│  • Design system                 │  │  • Cost optimization             │
│  • Accessibility                 │  │  • Performance tuning            │
│                                  │  │                                  │
│  Clean, focused on UI/UX         │  │  Clean, focused on AWS           │
└──────────────────────────────────┘  └──────────────────────────────────┘
                ↓                                      ↓
         High-level request              Expert recommendation
                ↓                                      ↓
                └──────────────┬───────────────────────┘
                               ↓
                    Better quality from both
```

**Benefit**: Each agent performs better in isolated, focused context.

---

## Parallel Tool Usage Pattern

### Sequential (Slow)

```
aws-expert needs:
  1. ECS config
  2. ALB config
  3. Security groups
  4. Best practices
  5. Well-Architected guidance

Sequential execution:
  ┌────────────────┐
  │ Query ECS      │ → 2 seconds
  └────────────────┘
         ↓
  ┌────────────────┐
  │ Query ALB      │ → 2 seconds
  └────────────────┘
         ↓
  ┌────────────────┐
  │ Query SG       │ → 2 seconds
  └────────────────┘
         ↓
  ┌────────────────┐
  │ Search docs    │ → 2 seconds
  └────────────────┘
         ↓
  ┌────────────────┐
  │ Get WA guide   │ → 2 seconds
  └────────────────┘

Total: 10 seconds
```

### Parallel (Fast)

```
aws-expert needs:
  1. ECS config
  2. ALB config
  3. Security groups
  4. Best practices
  5. Well-Architected guidance

Parallel execution:
  ┌────────────────┐
  │ Query ECS      │ ╲
  └────────────────┘  ╲
  ┌────────────────┐   ╲
  │ Query ALB      │   → All at once → 2 seconds
  └────────────────┘   ╱
  ┌────────────────┐  ╱
  │ Query SG       │ ╱
  └────────────────┘ ╱
  ┌────────────────┐╱
  │ Search docs    │
  └────────────────┘╱
  ┌────────────────┐
  │ Get WA guide   │
  └────────────────┘

Total: 2 seconds (80% faster)
```

**Implementation**: Specialists should ALWAYS use MCP tools in parallel.

---

## Quality Escalation Pattern

### Standard: Role → Specialist

```
┌─────────────────┐
│ ui-ux-developer │
└─────────────────┘
         ↓
    Routine deployment
         ↓
┌─────────────────┐
│   aws-expert    │
│                 │
│ ✓ Uses MCP      │
│ ✓ Analyzes      │
│ ✓ Recommends    │
└─────────────────┘
         ↓
      Deploy

Quality: High (95% success)
Cost: Medium (15x tokens)
```

### Critical: Role → Specialist → Evaluator

```
┌─────────────────┐
│ ui-ux-developer │
└─────────────────┘
         ↓
    Critical production deployment
         ↓
┌─────────────────┐
│   aws-expert    │
│                 │
│ ✓ Uses MCP      │
│ ✓ Analyzes      │
│ ✓ Recommends    │
└─────────────────┘
         ↓
    Plan created
         ↓
┌──────────────────────┐
│ aws-security-expert  │
│ (Evaluator)          │
│                      │
│ ✓ Reviews plan       │
│ ✓ Validates security │
│ ✓ Checks compliance  │
└──────────────────────┘
         ↓
    Plan validated
         ↓
┌─────────────────┐
│   aws-expert    │
│ (Optimizer)     │
│                 │
│ ✓ Incorporates  │
│   feedback      │
│ ✓ Refines plan  │
└─────────────────┘
         ↓
      Deploy

Quality: Maximum (99% success)
Cost: High (30x tokens)
Use When: Production, compliance-critical, high-risk
```

---

## Quick Reference: Decision Flowchart

```
                       START
                         │
                         ↓
           ┌─────────────────────────────┐
           │  Does task require domain   │
           │  expertise outside my role? │
           └─────────────────────────────┘
                    ↓ YES        ↓ NO
                    ↓            └──→ Handle directly
                    ↓
           ┌─────────────────────────────┐
           │  Is this ONLY information   │
           │  lookup? (No decisions)     │
           └─────────────────────────────┘
                    ↓ YES        ↓ NO
                    ↓            │
                    ↓            ↓
           ┌─────────────────────────────────────┐
           │  Could use MCP directly             │
           │  BUT for CORRECTNESS:               │
           │  Still delegate to specialist       │
           └─────────────────────────────────────┘
                    │            │
                    ↓            ↓
           ┌─────────────────────────────────────┐
           │  DELEGATE TO SPECIALIST             │
           │                                     │
           │  Specialist will:                   │
           │  1. Use MCP tools in parallel       │
           │  2. Apply domain expertise          │
           │  3. Synthesize recommendations      │
           │  4. Return validated plan           │
           └─────────────────────────────────────┘
                         │
                         ↓
           ┌─────────────────────────────┐
           │  Execute specialist's plan  │
           │  with confidence            │
           └─────────────────────────────┘
                         │
                         ↓
                       END
```

---

## Key Takeaways (Visual Summary)

### ✅ DO

```
┌──────────────────────────────────────────────┐
│  PRIMARY ROLE                                │
│    ↓                                         │
│  Recognizes: "I need domain expertise"       │
│    ↓                                         │
│  Delegates to: Specialist                    │
│    ↓                                         │
│  SPECIALIST                                  │
│    ├─ Uses MCP tools (data)                  │
│    ├─ Applies expertise (reasoning)          │
│    └─ Returns recommendation                 │
│    ↓                                         │
│  PRIMARY ROLE                                │
│    └─ Executes with confidence               │
│                                              │
│  RESULT: High quality, low errors            │
└──────────────────────────────────────────────┘
```

### ❌ DON'T

```
┌──────────────────────────────────────────────┐
│  PRIMARY ROLE                                │
│    ↓                                         │
│  Uses MCP tools directly                     │
│    ↓                                         │
│  Interprets without expertise                │
│    ↓                                         │
│  Guesses at solution                         │
│    ↓                                         │
│  Deploys                                     │
│    ↓                                         │
│  💥 Production issues                        │
│                                              │
│  RESULT: Low quality, high errors            │
└──────────────────────────────────────────────┘
```

---

## The Golden Rule (Visual)

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                     GOLDEN RULE                               ║
║                                                               ║
║  When in doubt, delegate to specialist.                       ║
║                                                               ║
║  ┌─────────────────────────────────────────────────────┐     ║
║  │  Delegating to specialist = Simple                  │     ║
║  │  (Proper separation of concerns)                    │     ║
║  │                                                      │     ║
║  │  Using tools directly = Complex                     │     ║
║  │  (Requires learning domain, increases errors)       │     ║
║  └─────────────────────────────────────────────────────┘     ║
║                                                               ║
║  Cost of wrong decision:                                      ║
║                                                               ║
║  MCP Direct:     Low tokens → High error risk → $$$$$ lost   ║
║  Specialist:     High tokens → Low error risk → $$$ saved    ║
║                                                               ║
║  Always choose correctness over token savings.                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

**Visual Reference Complete** ✓
**All patterns documented with diagrams** ✓
**Quick visual decision-making support** ✓
