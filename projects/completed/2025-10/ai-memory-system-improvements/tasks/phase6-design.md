# Phase 6: Memory Budget Profiles - Design Specification

**Created**: 2025-10-14
**Status**: DESIGN
**Goal**: Implement agent-specific memory budgets with dynamic adjustment and monitoring

---

## Executive Summary

**Problem**: All agents currently share the same 200K token budget ceiling. Different agent types have different memory needs:
- **Specialist agents**: Deep, narrow expertise → Lower budgets (20-50K tokens)
- **Role agents**: Broad, cross-domain coordination → Higher budgets (50-100K tokens)
- **Task complexity**: Simple queries vs complex multi-system analysis → Variable needs

**Solution**: Create memory budget profiles per agent type with dynamic adjustment based on task complexity and monitoring/alerting when budgets are exceeded.

**Expected Outcomes**:
- **25-50% reduction** in average context window size per agent invocation
- **Faster agent responses** due to smaller context loading
- **Better resource utilization** by matching budget to actual needs
- **Proactive alerts** when agents approach budget limits

---

## Architecture

### 1. Budget Profile System

#### Profile Definitions (`.claude/memory/budget-profiles.json`)
```json
{
  "profiles": {
    "specialist-narrow": {
      "description": "Single-tool specialists (e.g., snowflake-expert, dbt-expert)",
      "base_budget": 20000,
      "max_budget": 50000,
      "scope_weights": {
        "global": 0.2,
        "agent_recent": 0.3,
        "agent_patterns": 0.5
      }
    },
    "specialist-broad": {
      "description": "Cross-tool specialists (e.g., data-quality-specialist, aws-expert)",
      "base_budget": 35000,
      "max_budget": 75000,
      "scope_weights": {
        "global": 0.25,
        "agent_recent": 0.25,
        "agent_patterns": 0.5
      }
    },
    "role-coordinator": {
      "description": "Role agents coordinating multiple specialists",
      "base_budget": 50000,
      "max_budget": 100000,
      "scope_weights": {
        "global": 0.3,
        "agent_recent": 0.2,
        "agent_patterns": 0.5
      }
    },
    "role-architect": {
      "description": "Strategic architecture roles (data-architect-role, research-role)",
      "base_budget": 75000,
      "max_budget": 150000,
      "scope_weights": {
        "global": 0.35,
        "agent_recent": 0.15,
        "agent_patterns": 0.5
      }
    }
  },
  "agent_assignments": {
    "specialists/snowflake-expert": "specialist-narrow",
    "specialists/dbt-expert": "specialist-narrow",
    "specialists/tableau-expert": "specialist-narrow",
    "specialists/prefect-expert": "specialist-narrow",
    "specialists/orchestra-expert": "specialist-narrow",
    "specialists/dlthub-expert": "specialist-narrow",
    "specialists/streamlit-expert": "specialist-narrow",
    "specialists/react-expert": "specialist-narrow",
    "specialists/github-sleuth-expert": "specialist-narrow",
    "specialists/documentation-expert": "specialist-narrow",
    "specialists/business-context": "specialist-narrow",
    "specialists/ui-ux-expert": "specialist-narrow",
    "specialists/project-delivery-expert": "specialist-narrow",

    "specialists/aws-expert": "specialist-broad",
    "specialists/data-quality-specialist": "specialist-broad",
    "specialists/cost-optimization-specialist": "specialist-broad",

    "roles/analytics-engineer-role": "role-coordinator",
    "roles/data-engineer-role": "role-coordinator",
    "roles/bi-developer-role": "role-coordinator",
    "roles/ui-ux-developer-role": "role-coordinator",
    "roles/qa-engineer-role": "role-coordinator",
    "roles/business-analyst-role": "role-coordinator",
    "roles/project-manager-role": "role-coordinator",

    "roles/data-architect-role": "role-architect",
    "roles/research-role": "role-architect"
  }
}
```

#### Budget Calculation Logic
```python
def calculate_agent_budget(agent_name: str, task_complexity: str = "medium") -> int:
    """
    Calculate memory budget for agent based on profile and task complexity

    Args:
        agent_name: Agent identifier (e.g., "specialists/dbt-expert")
        task_complexity: "simple" | "medium" | "complex" | "multi-system"

    Returns:
        Token budget for this agent invocation
    """
    profile = get_agent_profile(agent_name)
    base_budget = profile["base_budget"]
    max_budget = profile["max_budget"]

    # Complexity multipliers
    complexity_multipliers = {
        "simple": 0.5,      # 50% of base budget (e.g., single query)
        "medium": 1.0,      # 100% of base budget (standard task)
        "complex": 1.5,     # 150% of base budget (multi-step analysis)
        "multi-system": 2.0 # 200% of base budget (cross-system coordination)
    }

    multiplier = complexity_multipliers.get(task_complexity, 1.0)
    calculated_budget = int(base_budget * multiplier)

    # Cap at max budget
    return min(calculated_budget, max_budget)
```

---

### 2. Dynamic Budget Adjustment

#### Task Complexity Detection

**Automatic detection** based on task characteristics:

```python
def detect_task_complexity(task_description: str, context: Dict) -> str:
    """
    Automatically detect task complexity from description and context

    Detection heuristics:
    - simple: Single query, single tool, specific question
    - medium: Multiple steps, single system, standard analysis
    - complex: Multi-step workflow, multiple tools, deep analysis
    - multi-system: Cross-system coordination, multiple agents, architectural decisions
    """
    complexity_signals = {
        "multi-system": [
            "cross-system", "integration", "multiple tools",
            "orchestrat", "coordinate", "architecture"
        ],
        "complex": [
            "analyze", "investigate", "troubleshoot", "optimize",
            "multi-step", "comprehensive", "deep dive"
        ],
        "simple": [
            "list", "show", "get", "fetch", "find",
            "what is", "how many", "check status"
        ]
    }

    # Count signal matches
    desc_lower = task_description.lower()

    for complexity, signals in complexity_signals.items():
        if any(signal in desc_lower for signal in signals):
            return complexity

    # Default to medium if no clear signals
    return "medium"
```

#### Budget Adjustment Protocol

1. **Pre-task**: Detect complexity → Calculate budget → Load memory within budget
2. **Mid-task**: If agent requests more context → Bump to next complexity tier
3. **Post-task**: Log actual token usage → Update profile recommendations

---

### 3. Budget Monitoring & Alerts

#### Real-Time Budget Tracking

```python
class BudgetMonitor:
    """Monitor agent memory budget usage in real-time"""

    def __init__(self, agent_name: str, budget: int):
        self.agent_name = agent_name
        self.budget = budget
        self.loaded_tokens = 0
        self.warnings = []

    def track_load(self, scope: str, tokens: int):
        """Track tokens loaded from a scope"""
        self.loaded_tokens += tokens

        # Warning thresholds
        if self.loaded_tokens > self.budget * 0.75:
            self.warnings.append({
                "threshold": "75%",
                "message": f"Budget 75% consumed ({self.loaded_tokens}/{self.budget} tokens)"
            })

        if self.loaded_tokens > self.budget * 0.90:
            self.warnings.append({
                "threshold": "90%",
                "message": f"⚠️ Budget 90% consumed ({self.loaded_tokens}/{self.budget} tokens)"
            })

        if self.loaded_tokens > self.budget:
            self.warnings.append({
                "threshold": "exceeded",
                "message": f"❌ Budget EXCEEDED ({self.loaded_tokens}/{self.budget} tokens)"
            })

    def get_status(self) -> Dict:
        """Get current budget status"""
        return {
            "agent": self.agent_name,
            "budget": self.budget,
            "loaded": self.loaded_tokens,
            "usage_pct": (self.loaded_tokens / self.budget) * 100,
            "remaining": self.budget - self.loaded_tokens,
            "warnings": self.warnings
        }
```

#### Budget Alert System

**Alerting triggers**:
- **75% threshold**: Log info message (normal, not concerning)
- **90% threshold**: Warning message (consider bumping complexity tier)
- **100% exceeded**: Error message + automatic complexity tier bump
- **Repeated exceedances**: Flag profile for adjustment

**Alert destinations**:
- Real-time console output during agent execution
- Budget usage logs (`.claude/cache/budget-usage.jsonl`)
- Weekly budget report (via Phase 5 automation)

---

### 4. Budget Profile Tuning

#### Usage Analytics

Track actual budget usage over time:

```json
{
  "timestamp": "2025-10-14T20:00:00Z",
  "agent": "specialists/dbt-expert",
  "profile": "specialist-narrow",
  "task_complexity": "medium",
  "budget_allocated": 20000,
  "tokens_loaded": 15432,
  "usage_pct": 77.16,
  "scopes_loaded": {
    "global": 3200,
    "agent_recent": 4100,
    "agent_patterns": 8132
  },
  "exceeded_budget": false,
  "warnings_triggered": ["75%"]
}
```

#### Profile Recommendations

**Monthly analysis** (via Phase 5 automation):
- Identify agents consistently exceeding budgets → Recommend profile upgrade
- Identify agents under-utilizing budgets → Recommend profile downgrade
- Detect scope weight imbalances → Recommend weight adjustments

**Output**: `.claude/cache/budget-profile-recommendations.json`

```json
{
  "date": "2025-11-01",
  "recommendations": [
    {
      "agent": "specialists/dbt-expert",
      "current_profile": "specialist-narrow",
      "recommended_profile": "specialist-broad",
      "reason": "Budget exceeded in 8/30 days (26.7% exceedance rate)",
      "avg_usage_pct": 94.3,
      "confidence": 0.85
    },
    {
      "agent": "specialists/tableau-expert",
      "current_profile": "specialist-narrow",
      "recommended_action": "adjust_weights",
      "current_weights": {"global": 0.2, "agent_recent": 0.3, "agent_patterns": 0.5},
      "recommended_weights": {"global": 0.15, "agent_recent": 0.25, "agent_patterns": 0.6},
      "reason": "Pattern usage higher than expected (60% vs 50% allocated)",
      "confidence": 0.72
    }
  ]
}
```

---

## Implementation Plan

### Phase 6.1: Core Budget System (Week 1)
**Deliverables**:
- [ ] `budget-profiles.json` schema and initial profiles
- [ ] `calculate-agent-budget.py` script
- [ ] Integration with `memory-budget-scoped.py`
- [ ] Basic budget enforcement in memory loading

**Tests**:
- Budget calculation for all agent types
- Profile assignment correctness
- Budget enforcement (hard limit)

### Phase 6.2: Dynamic Complexity Detection (Week 1)
**Deliverables**:
- [ ] `detect-task-complexity.py` script
- [ ] Complexity signal dictionary
- [ ] Integration with agent task invocation
- [ ] Manual complexity override capability

**Tests**:
- Complexity detection accuracy (sample tasks)
- Budget scaling by complexity tier
- Override functionality

### Phase 6.3: Budget Monitoring (Week 2)
**Deliverables**:
- [ ] `BudgetMonitor` class implementation
- [ ] Real-time budget tracking during agent execution
- [ ] Warning/alert system
- [ ] Budget usage logging (`.claude/cache/budget-usage.jsonl`)

**Tests**:
- Warning triggers at 75%, 90%, 100%
- Log formatting and persistence
- Multi-agent concurrent tracking

### Phase 6.4: Analytics & Tuning (Week 2)
**Deliverables**:
- [ ] `analyze-budget-usage.py` script
- [ ] Profile recommendation engine
- [ ] Weekly budget usage report (integrate with Phase 5)
- [ ] Profile adjustment workflow

**Tests**:
- Recommendation accuracy (historical data)
- Profile upgrade/downgrade logic
- Scope weight optimization

---

## Success Metrics

### Performance Metrics
- **Average context reduction**: Target 25-50% per agent invocation
- **Budget exceedance rate**: Target <5% of agent invocations
- **Response time improvement**: Target 10-20% faster agent responses

### Operational Metrics
- **Profile accuracy**: Target >90% of agents assigned to correct profile
- **Alert noise**: Target <2% false positive alerts
- **Tuning frequency**: Target <1 profile adjustment per agent per quarter

### Quality Metrics
- **Agent effectiveness**: No degradation in task completion quality
- **Context sufficiency**: Agents have enough memory to complete tasks
- **Budget efficiency**: Minimal wasted token allocation

---

## Risk Mitigation

### Risk 1: Budget Too Restrictive
**Impact**: Agent can't complete tasks due to insufficient context
**Mitigation**:
- Automatic complexity tier bump on budget exceedance
- Manual override capability
- Conservative initial budgets (err on higher side)
- Weekly monitoring for exceedance patterns

### Risk 2: Complexity Detection Inaccurate
**Impact**: Wrong budget allocation → wasted resources or insufficient context
**Mitigation**:
- Hybrid approach: Automatic detection + manual override
- Logging actual complexity vs detected for tuning
- Conservative default (medium complexity)
- User feedback mechanism

### Risk 3: Profile Assignment Errors
**Impact**: Agents assigned to wrong profile → suboptimal budgets
**Mitigation**:
- Monthly profile recommendation analysis
- Easy profile reassignment process
- Agent-specific overrides in config
- Detailed logging for manual review

---

## Integration Points

### With Phase 4 (Agent Scopes)
- Scope weights defined in profiles
- Budget enforcement respects scope boundaries
- Per-scope budget allocation

### With Phase 5 (Automation)
- Weekly budget usage analysis
- Monthly profile recommendations
- Budget alert aggregation in reports

### With Claude Code Session Initialization
- Budget profile loaded at agent invocation
- Task complexity detected from user request
- Budget monitor initialized before memory loading

---

## Open Questions

1. **Should budgets be enforced hard (error) or soft (warning)?**
   - **Recommendation**: Soft enforcement with automatic tier bump
   - **Rationale**: Better UX, prevents task failures, collects usage data

2. **How to handle multi-agent tasks (role → specialist delegation)?**
   - **Recommendation**: Each agent gets independent budget
   - **Rationale**: Cleaner separation, easier accounting

3. **Should we expose budget to agents in their prompts?**
   - **Recommendation**: No, keep transparent to agents
   - **Rationale**: Avoid agents self-limiting, let system manage

4. **Complexity detection: automatic only or manual override UI?**
   - **Recommendation**: Both - automatic default, manual override in task invocation
   - **Rationale**: Flexibility for power users, automation for standard use

---

## Timeline

**Total Duration**: 2 weeks

**Week 1** (Phase 6.1 + 6.2):
- Days 1-3: Core budget system + profiles
- Days 4-5: Complexity detection + integration

**Week 2** (Phase 6.3 + 6.4):
- Days 1-3: Monitoring + alerting
- Days 4-5: Analytics + tuning

**Deployment**: End of Week 2, start collecting data for 30 days before tuning

---

## Future Enhancements (Post-Phase 6)

1. **Machine Learning Budget Prediction**
   - Use historical usage to predict optimal budgets
   - Adaptive budgets based on agent performance

2. **User-Specific Budget Profiles**
   - Different users may have different usage patterns
   - Personalized budget optimization

3. **Budget Sharing/Pooling**
   - Multi-agent tasks share budget pool
   - Transfer unused budget between agents

4. **Budget Cost Accounting**
   - Track $ cost of token usage (API pricing)
   - Cost optimization recommendations

---

## References

- **Phase 4 Implementation**: `tasks/phase4-implementation.md`
- **Phase 5 Implementation**: `tasks/phase5-implementation.md`
- **Memory Health Check**: `scripts/check-memory-health.py`
- **Scoped Budget Tool**: `scripts/memory-budget-scoped.py`
