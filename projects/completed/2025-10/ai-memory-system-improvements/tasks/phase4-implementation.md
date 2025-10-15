# Phase 4: Agent-Specific Memory Scopes - Implementation Plan

## Overview

**Goal**: Reduce specialist context noise by 50-70% through agent-specific memory directories
**Timeline**: Weeks 7-8 (estimated 1-2 weeks)
**Status**: Starting

## Problem Statement

**Current State** (Phase 1 & 2 Complete):
- ✅ Token budget system operational (91.7% reduction)
- ✅ Automated consolidation running (daily/weekly/monthly)
- ❌ **ALL agents see ALL patterns** (context noise remains)

**The Issue**:
```
When dbt-expert is invoked:
- Loads: git-workflow patterns, AWS deployment patterns, Tableau optimization patterns
- Relevant: dbt patterns (maybe 20% of loaded content)
- Wasted tokens: 80% of budget on irrelevant patterns
```

**Phase 4 Solution**:
```
dbt-expert loads:
1. FIRST: .claude/memory/specialists/dbt-expert/ (dbt-specific patterns)
2. THEN: .claude/memory/patterns/ (global patterns, if budget allows)
Result: 50-70% more relevant context, same token budget
```

## Success Criteria

### Functional Requirements
- [ ] Agent-specific directories created for all 16 specialists
- [ ] Role-specific directories created for all 11 roles
- [ ] Scope-aware loading implemented in memory budget system
- [ ] Cross-scope promotion workflow operational
- [ ] No specialist knowledge loss during migration

### Performance Requirements
- [ ] 50-70% specialist context reduction measured
- [ ] Relevance score improvement >30% for specialists
- [ ] Budget utilization improved (less waste on irrelevant patterns)
- [ ] No performance degradation in load times

### Quality Requirements
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Backward compatibility maintained
- [ ] Migration path validated

## Implementation Tasks

### Task 1: Create Agent-Specific Directory Structure
**Est. Time**: 1 hour
**Priority**: HIGH

**Directory Layout**:
```
.claude/memory/
├── patterns/                    # Global patterns (cross-agent)
│   ├── git-workflow-patterns.md
│   ├── testing-patterns.md
│   └── project-completion-knowledge-extraction.md
├── specialists/                 # Specialist-specific memory
│   ├── aws-expert/
│   │   ├── recent/             # Tier 1: <30 days
│   │   ├── intermediate/       # Tier 2: 30-90 days
│   │   ├── patterns/           # Tier 3: Permanent
│   │   └── archive/            # Tier 4: Low-value
│   ├── dbt-expert/
│   │   ├── recent/
│   │   ├── intermediate/
│   │   ├── patterns/
│   │   └── archive/
│   ├── snowflake-expert/
│   ├── tableau-expert/
│   ├── dlthub-expert/
│   ├── orchestra-expert/
│   ├── prefect-expert/
│   ├── react-expert/
│   ├── streamlit-expert/
│   ├── documentation-expert/
│   ├── github-sleuth-expert/
│   ├── business-context/
│   ├── data-quality-specialist/
│   ├── cost-optimization-specialist/
│   └── ui-ux-expert/
└── roles/                       # Role-specific memory
    ├── analytics-engineer-role/
    │   ├── recent/
    │   ├── intermediate/
    │   ├── patterns/
    │   └── archive/
    ├── data-engineer-role/
    ├── bi-developer-role/
    ├── ui-ux-developer-role/
    ├── data-architect-role/
    ├── business-analyst-role/
    ├── qa-engineer-role/
    ├── project-manager-role/
    ├── dba-role/
    └── research-role/
```

**Script**:
```python
# scripts/create-agent-scopes.py

from pathlib import Path

def create_agent_scope_structure():
    """Create directory structure for agent-specific memory scopes"""

    base = Path(".claude/memory")

    # Specialist agents (from .claude/agents/specialists/)
    specialists = [
        "aws-expert",
        "dbt-expert",
        "snowflake-expert",
        "tableau-expert",
        "dlthub-expert",
        "orchestra-expert",
        "prefect-expert",
        "react-expert",
        "streamlit-expert",
        "documentation-expert",
        "github-sleuth-expert",
        "business-context",
        "data-quality-specialist",
        "cost-optimization-specialist",
        "ui-ux-expert",
        "project-delivery-expert",
    ]

    # Role agents (from .claude/agents/roles/)
    roles = [
        "analytics-engineer-role",
        "data-engineer-role",
        "bi-developer-role",
        "ui-ux-developer-role",
        "data-architect-role",
        "business-analyst-role",
        "qa-engineer-role",
        "project-manager-role",
        "dba-role",
        "research-role",
    ]

    # Create specialist directories
    for specialist in specialists:
        specialist_dir = base / "specialists" / specialist
        for tier in ["recent", "intermediate", "patterns", "archive"]:
            tier_dir = specialist_dir / tier
            tier_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {tier_dir}")

    # Create role directories
    for role in roles:
        role_dir = base / "roles" / role
        for tier in ["recent", "intermediate", "patterns", "archive"]:
            tier_dir = role_dir / tier
            tier_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {tier_dir}")

    print(f"\n✅ Created {len(specialists)} specialist scopes")
    print(f"✅ Created {len(roles)} role scopes")

if __name__ == "__main__":
    create_agent_scope_structure()
```

**Deliverable**: Agent-specific directory structure created

---

### Task 2: Analyze Current Pattern Distribution
**Est. Time**: 2 hours
**Priority**: HIGH

**Goal**: Understand which patterns belong to which agents

**Analysis Script**:
```python
# scripts/analyze-pattern-distribution.py

from pathlib import Path
import json
from collections import defaultdict

def analyze_pattern_distribution():
    """Analyze which patterns should belong to which agents"""

    patterns_dir = Path(".claude/memory/patterns")
    results = defaultdict(list)

    # Technology/tool keywords for agents
    agent_keywords = {
        "dbt-expert": ["dbt", "sql", "model", "test", "macro", "jinja"],
        "snowflake-expert": ["snowflake", "warehouse", "database", "query", "performance"],
        "aws-expert": ["aws", "ec2", "s3", "lambda", "ecs", "cloudformation", "alb"],
        "tableau-expert": ["tableau", "dashboard", "visualization", "workbook"],
        "github-sleuth-expert": ["github", "repository", "pr", "issue", "commit"],
        "react-expert": ["react", "jsx", "component", "state", "hook"],
        "streamlit-expert": ["streamlit", "st.", "app.py"],
        # ... etc
    }

    for pattern_file in patterns_dir.glob("**/*.md"):
        content = pattern_file.read_text().lower()

        # Check which agents this pattern is relevant to
        for agent, keywords in agent_keywords.items():
            relevance_score = sum(1 for kw in keywords if kw in content)
            if relevance_score > 0:
                results[agent].append({
                    "pattern": pattern_file.name,
                    "relevance_score": relevance_score,
                    "path": str(pattern_file)
                })

    # Save analysis results
    output = Path("projects/active/ai-memory-system-improvements/tasks/pattern-distribution.json")
    output.write_text(json.dumps(results, indent=2))

    print("Pattern Distribution Analysis:")
    for agent, patterns in results.items():
        print(f"  {agent}: {len(patterns)} relevant patterns")

if __name__ == "__main__":
    analyze_pattern_distribution()
```

**Expected Output**:
```json
{
  "dbt-expert": [
    {
      "pattern": "dbt-snowflake-optimization-pattern.md",
      "relevance_score": 8,
      "path": ".claude/memory/patterns/cross-tool-integration/dbt-snowflake-optimization-pattern.md"
    }
  ],
  "aws-expert": [
    {
      "pattern": "aws-docs-deployment-pattern.md",
      "relevance_score": 12,
      "path": ".claude/memory/patterns/cross-tool-integration/aws-docs-deployment-pattern.md"
    }
  ]
}
```

**Deliverable**: `pattern-distribution.json` analysis report

---

### Task 3: Implement Scope-Aware Memory Loading
**Est. Time**: 4 hours
**Priority**: HIGH

**Goal**: Update memory budget system to load agent-specific patterns first

**Enhanced Memory Budget System**:
```python
# scripts/memory-budget-scoped.py

from pathlib import Path
from typing import List, Optional
import json

class ScopedMemoryBudget:
    """Memory budget with agent-specific scope awareness"""

    def __init__(self, max_tokens: int = 20000, agent_name: Optional[str] = None, agent_type: Optional[str] = None):
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.loaded_patterns = []
        self.skipped_patterns = []
        self.agent_name = agent_name
        self.agent_type = agent_type  # "specialist" or "role"

    def get_scope_directories(self) -> List[Path]:
        """Get directories to load patterns from, in priority order"""
        base = Path(".claude/memory")
        directories = []

        # Priority 1: Agent-specific patterns (if agent specified)
        if self.agent_name and self.agent_type:
            agent_dir = base / self.agent_type / self.agent_name
            if agent_dir.exists():
                directories.append(agent_dir / "recent")
                directories.append(agent_dir / "patterns")
                directories.append(agent_dir / "intermediate")

        # Priority 2: Global patterns (always loaded)
        directories.append(base / "patterns")
        directories.append(base / "recent")

        return [d for d in directories if d.exists()]

    def load_patterns_with_scope(self, context: dict) -> List[Pattern]:
        """Load patterns with scope awareness"""
        all_patterns = []

        # Get scope directories in priority order
        scope_dirs = self.get_scope_directories()

        # Load patterns from each scope
        for scope_dir in scope_dirs:
            for pattern_file in scope_dir.glob("*.md"):
                pattern = load_pattern(pattern_file, context)
                all_patterns.append(pattern)

        # Sort by relevance (scope-aware patterns get bonus)
        sorted_patterns = sorted(
            all_patterns,
            key=lambda p: self._calculate_scope_relevance(p),
            reverse=True
        )

        # Load patterns until budget exhausted
        for pattern in sorted_patterns:
            if not self.add_pattern(pattern):
                break  # Budget exhausted

        return self.loaded_patterns

    def _calculate_scope_relevance(self, pattern: Pattern) -> float:
        """Calculate relevance with scope bonus"""
        base_relevance = pattern.relevance_score

        # Bonus for agent-specific patterns
        if self.agent_name and self.agent_type:
            agent_path = f".claude/memory/{self.agent_type}/{self.agent_name}/"
            if agent_path in str(pattern.path):
                return base_relevance + 0.3  # 30% bonus for scoped patterns

        return base_relevance

    def get_scope_stats(self) -> dict:
        """Get statistics about scope usage"""
        agent_patterns = []
        global_patterns = []

        for pattern in self.loaded_patterns:
            if self.agent_name and self.agent_type:
                agent_path = f".claude/memory/{self.agent_type}/{self.agent_name}/"
                if agent_path in str(pattern.path):
                    agent_patterns.append(pattern)
                else:
                    global_patterns.append(pattern)
            else:
                global_patterns.append(pattern)

        return {
            "agent_patterns_loaded": len(agent_patterns),
            "global_patterns_loaded": len(global_patterns),
            "agent_tokens": sum(p.token_count for p in agent_patterns),
            "global_tokens": sum(p.token_count for p in global_patterns),
            "scope_utilization_pct": (len(agent_patterns) / len(self.loaded_patterns) * 100) if self.loaded_patterns else 0
        }
```

**Deliverable**: `scripts/memory-budget-scoped.py` with scope awareness

---

### Task 4: Create Pattern Migration Tool
**Est. Time**: 3 hours
**Priority**: MEDIUM

**Goal**: Migrate existing patterns to appropriate agent scopes

**Migration Strategy**:
1. Use pattern distribution analysis (Task 2)
2. Copy high-relevance patterns to agent-specific directories
3. Keep originals in global patterns (backward compatibility)
4. Add metadata tracking origin

**Migration Script**:
```python
# scripts/migrate-patterns-to-scopes.py

from pathlib import Path
import json
import shutil

def migrate_patterns_to_scopes():
    """Migrate patterns to agent-specific scopes based on analysis"""

    # Load distribution analysis
    analysis_file = Path("projects/active/ai-memory-system-improvements/tasks/pattern-distribution.json")
    if not analysis_file.exists():
        print("❌ Run analyze-pattern-distribution.py first!")
        return

    distribution = json.loads(analysis_file.read_text())

    base = Path(".claude/memory")
    migrated_count = 0

    for agent, patterns in distribution.items():
        # Determine agent type (specialist vs role)
        agent_type = "specialists" if "expert" in agent or "specialist" in agent else "roles"

        for pattern_info in patterns:
            # Only migrate high-relevance patterns (score > 3)
            if pattern_info["relevance_score"] < 3:
                continue

            source_path = Path(pattern_info["path"])
            if not source_path.exists():
                continue

            # Copy to agent-specific patterns directory
            dest_dir = base / agent_type / agent / "patterns"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / source_path.name

            # Copy pattern
            shutil.copy2(source_path, dest_path)

            # Copy metadata if exists
            metadata_source = source_path.with_suffix(".metadata.json")
            if metadata_source.exists():
                metadata_dest = dest_path.with_suffix(".metadata.json")
                shutil.copy2(metadata_source, metadata_dest)

            migrated_count += 1
            print(f"✅ Migrated: {source_path.name} → {agent} ({pattern_info['relevance_score']} relevance)")

    print(f"\n✅ Migrated {migrated_count} patterns to agent-specific scopes")
    print(f"📦 Original patterns preserved in global directory")

if __name__ == "__main__":
    migrate_patterns_to_scopes()
```

**Deliverable**: Patterns migrated to agent-specific scopes

---

### Task 5: Create Cross-Scope Promotion Workflow
**Est. Time**: 2 hours
**Priority**: MEDIUM

**Goal**: Allow high-value agent-specific patterns to be promoted to global

**Promotion Criteria**:
- Used by 3+ different agents
- Confidence score ≥ 0.85
- Marked for promotion by user/agent

**Promotion Script**:
```python
# scripts/promote-to-global.py

from pathlib import Path
import json
import shutil

def promote_pattern_to_global(agent_type: str, agent_name: str, pattern_name: str):
    """Promote agent-specific pattern to global scope"""

    base = Path(".claude/memory")
    source_dir = base / agent_type / agent_name / "patterns"
    source_pattern = source_dir / pattern_name

    if not source_pattern.exists():
        print(f"❌ Pattern not found: {source_pattern}")
        return False

    # Check promotion criteria
    metadata_file = source_pattern.with_suffix(".metadata.json")
    if metadata_file.exists():
        metadata = json.loads(metadata_file.read_text())

        # Criteria checks
        use_count = metadata.get("use_count", 0)
        confidence = metadata.get("confidence", 0.0)

        if use_count < 3:
            print(f"⚠️  Pattern needs more usage (current: {use_count}, required: 3)")
            return False

        if confidence and confidence < 0.85:
            print(f"⚠️  Pattern needs higher confidence (current: {confidence}, required: 0.85)")
            return False

    # Promote to global
    dest_dir = base / "patterns"
    dest_pattern = dest_dir / pattern_name

    shutil.copy2(source_pattern, dest_pattern)
    if metadata_file.exists():
        shutil.copy2(metadata_file, dest_pattern.with_suffix(".metadata.json"))

    print(f"✅ Promoted: {pattern_name} to global scope")
    print(f"📍 Source: {source_pattern}")
    print(f"📍 Destination: {dest_pattern}")

    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Promote agent pattern to global")
    parser.add_argument("agent_type", choices=["specialists", "roles"])
    parser.add_argument("agent_name")
    parser.add_argument("pattern_name")
    args = parser.parse_args()

    promote_pattern_to_global(args.agent_type, args.agent_name, args.pattern_name)
```

**Usage**:
```bash
python scripts/promote-to-global.py specialists dbt-expert dbt-optimization-pattern.md
```

**Deliverable**: Cross-scope promotion workflow operational

---

### Task 6: Update Memory Health Check
**Est. Time**: 1 hour
**Priority**: LOW

**Goal**: Add scope statistics to health check

**Enhanced Health Check**:
```python
# Update scripts/check-memory-health.py

def get_scope_breakdown(self) -> Dict:
    """Get breakdown by agent scopes"""
    base = Path(".claude/memory")

    scope_stats = {
        "global": self.count_directory_tokens(base / "patterns"),
        "specialists": {},
        "roles": {}
    }

    # Count specialist scopes
    specialists_dir = base / "specialists"
    if specialists_dir.exists():
        for agent_dir in specialists_dir.iterdir():
            if agent_dir.is_dir():
                scope_stats["specialists"][agent_dir.name] = self.count_directory_tokens(agent_dir / "patterns")

    # Count role scopes
    roles_dir = base / "roles"
    if roles_dir.exists():
        for role_dir in roles_dir.iterdir():
            if role_dir.is_dir():
                scope_stats["roles"][role_dir.name] = self.count_directory_tokens(role_dir / "patterns")

    return scope_stats
```

**Deliverable**: Health check includes scope breakdown

---

### Task 7: Testing & Validation
**Est. Time**: 3 hours
**Priority**: HIGH

**Test Scenarios**:

1. **Specialist Invocation Test**:
   ```python
   # Test: dbt-expert loads dbt-specific patterns first
   budget = ScopedMemoryBudget(max_tokens=20000, agent_name="dbt-expert", agent_type="specialists")
   loaded = budget.load_patterns_with_scope(context={"task": "optimize dbt model"})

   # Validate:
   # - dbt-expert patterns loaded first
   # - Global patterns loaded if budget allows
   # - Total within budget
   # - Relevance improved vs. global-only loading
   ```

2. **Role Invocation Test**:
   ```python
   # Test: analytics-engineer-role loads role-specific patterns
   budget = ScopedMemoryBudget(max_tokens=20000, agent_name="analytics-engineer-role", agent_type="roles")
   loaded = budget.load_patterns_with_scope(context={"task": "build data model"})
   ```

3. **Promotion Workflow Test**:
   ```python
   # Test: High-value pattern promotes to global
   promote_pattern_to_global("specialists", "aws-expert", "alb-oidc-pattern.md")
   # Validate pattern exists in both scopes
   ```

4. **Backward Compatibility Test**:
   ```python
   # Test: Loading without agent scope still works
   budget = ScopedMemoryBudget(max_tokens=20000)  # No agent specified
   loaded = budget.load_patterns_with_scope(context={})
   # Validate: Global patterns loaded as before
   ```

**Success Metrics**:
- [ ] Specialist context reduction: 50-70%
- [ ] Relevance score improvement: >30%
- [ ] No knowledge loss: All patterns accessible
- [ ] Performance: No degradation in load times

**Deliverable**: All tests passing, metrics validated

---

## Timeline

**Week 1** (Days 1-5):
- [ ] Task 1: Create directory structure (Day 1)
- [ ] Task 2: Analyze pattern distribution (Day 1-2)
- [ ] Task 3: Implement scope-aware loading (Day 2-3)
- [ ] Task 4: Pattern migration tool (Day 3-4)

**Week 2** (Days 6-10):
- [ ] Task 5: Cross-scope promotion workflow (Day 6-7)
- [ ] Task 6: Update health check (Day 7)
- [ ] Task 7: Testing & validation (Day 8-10)

## Dependencies

- Phase 1 & 2 complete ✅
- Token budget system operational ✅
- Memory consolidation running ✅
- All 16 specialist agents identified ✅
- All 11 role agents identified ✅

## Risk Mitigation

**Risk**: Pattern migration causes duplication
**Mitigation**: Copy (not move), preserve originals in global

**Risk**: Scope logic is complex
**Mitigation**: Extensive testing, fallback to global patterns

**Risk**: Performance overhead
**Mitigation**: Cache scope directories, lazy loading

## Success Validation

**Phase 4 Complete When**:
- [ ] Agent-specific directories created (26 agents)
- [ ] Scope-aware loading implemented
- [ ] Pattern migration completed
- [ ] Cross-scope promotion working
- [ ] 50-70% specialist context reduction measured
- [ ] All tests passing
- [ ] Documentation updated

---

*This implementation plan delivers agent-specific memory scopes with measurable context reduction while maintaining backward compatibility and zero knowledge loss.*
