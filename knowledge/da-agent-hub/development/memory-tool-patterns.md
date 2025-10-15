# Memory Tool Implementation Patterns

**Created**: 2025-10-15
**Based On**: Anthropic Claude Cookbook and official guidance
**Project**: Enhanced /switch command implementation

---

## Overview

The memory tool pattern enables cross-session learning where Claude can persist knowledge between conversations through client-side file storage. This guide documents implementation patterns following Anthropic's official Memory Tool Cookbook.

---

## Anthropic Official Guidance

> "Memory files are read back into Claude's context, making them a potential vector for prompt injection."

**Key Requirements**:
- Client-side file storage with security validation
- Path traversal prevention
- Prompt injection sanitization
- Comprehensive audit logging
- Memory scope isolation per user/project

---

## Memory Architecture

### Directory Structure

```
.claude/memory/
├── switch-contexts/      # Switch operation history for learning
├── project-contexts/     # Project-specific memories
├── patterns/             # Learned patterns (cross-session)
├── preferences/          # User preferences
└── agent-knowledge/      # Cross-session agent learnings
```

**Design Principles**:
- Separate memory scopes prevent cross-contamination
- Hierarchical organization enables efficient querying
- JSON format for structured data, Markdown for documentation

---

## Security Implementation

### Path Traversal Prevention

```python
class SecurityValidator:
    """Security validation for memory operations per Anthropic guidance"""

    @staticmethod
    def validate_path(path: str, base_dir: str) -> str:
        """Prevent directory traversal attacks"""
        base_dir_abs = os.path.abspath(base_dir)
        requested_abs = os.path.abspath(os.path.join(base_dir_abs, path))

        if not requested_abs.startswith(base_dir_abs):
            raise SecurityError(f"Path traversal attempt detected: {path}")

        return requested_abs
```

**Attack Prevention**:
- `../../etc/passwd` → Blocked (traversal outside base_dir)
- `switch-contexts/../../../secrets` → Blocked (normalized path escapes base)
- `switch-contexts/2025-10.json` → Allowed (stays within base_dir)

### Prompt Injection Sanitization

```python
@staticmethod
def sanitize_content(content: str) -> str:
    """Prevent prompt injection via memory content"""
    dangerous_patterns = [
        (r"<claude>.*?</claude>", "[REDACTED: POTENTIAL INJECTION]"),
        (r"IGNORE\s+PREVIOUS\s+INSTRUCTIONS", "[REDACTED: COMMAND INJECTION]"),
        (r"\[SYSTEM\]", "[REDACTED: SYSTEM TAG]"),
        (r"<\|im_start\|>", "[REDACTED: CONTROL SEQUENCE]"),
        (r"Act\s+as\s+if\s+you\s+are", "[REDACTED: ROLE MANIPULATION]"),
    ]

    sanitized = content
    for pattern, replacement in dangerous_patterns:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    return sanitized
```

**Threat Model**:
- **Claude control tags**: `<claude>`, `<|im_start|>` → Redacted
- **Command injection**: `IGNORE PREVIOUS INSTRUCTIONS` → Redacted
- **System impersonation**: `[SYSTEM]` tags → Redacted
- **Role manipulation**: `Act as if you are...` → Redacted

### Audit Logging

```python
@staticmethod
def audit_log(operation: str, path: str, success: bool, error: Optional[str] = None):
    """Log all memory operations for security audit"""
    audit_dir = Path.home() / ".claude" / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)

    log_file = audit_dir / f"memory-audit-{datetime.now().strftime('%Y-%m')}.jsonl"

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "path": path,
        "success": success,
        "error": error,
        "pid": os.getpid()
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

**Audit Trail**:
- Every memory operation logged
- Monthly rotation for manageable file sizes
- JSONL format for easy parsing and analysis
- Includes PID for process tracking

---

## MemoryManager Implementation

### Core Class Structure

```python
class MemoryManager:
    """Manages persistent memory across Claude sessions"""

    def __init__(self, memory_root: str = ".claude/memory"):
        self.memory_root = Path(memory_root)
        self.validator = SecurityValidator()
        self._ensure_structure()

    def _ensure_structure(self):
        """Create memory directory structure if it doesn't exist"""
        for subdir in ["switch-contexts", "project-contexts", "patterns",
                       "preferences", "agent-knowledge"]:
            (self.memory_root / subdir).mkdir(parents=True, exist_ok=True)
```

### Switch Pattern Learning

```python
def remember_switch(self, from_project: str, to_project: str,
                   preservation_method: str, duration_seconds: float):
    """Remember a switch operation for learning"""
    memory = {
        "from_project": from_project,
        "to_project": to_project,
        "preservation_method": preservation_method,  # "commit" or "stash"
        "duration_seconds": duration_seconds,
        "timestamp": datetime.now().isoformat(),
        "success": True
    }

    # Sanitize project names
    memory["from_project"] = self.validator.sanitize_content(from_project)
    memory["to_project"] = self.validator.sanitize_content(to_project)

    # Validate storage path
    filename = f"switch-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    filepath = self.validator.validate_path(
        f"switch-contexts/{filename}",
        str(self.memory_root)
    )

    # Save and audit
    with open(filepath, "w") as f:
        json.dump(memory, f, indent=2)

    self.validator.audit_log("remember_switch", str(filepath), True)
```

**Learning Pattern**:
- Every switch operation recorded
- Timestamps enable temporal pattern analysis
- Method tracking (commit vs stash) for optimization
- Duration tracking for performance insights

### Historical Query

```python
def query_switches(self, from_project: Optional[str] = None,
                  to_project: Optional[str] = None) -> List[Dict[str, Any]]:
    """Query switch history with optional filters"""
    switches = []

    switch_dir = self.memory_root / "switch-contexts"
    if not switch_dir.exists():
        return switches

    for switch_file in sorted(switch_dir.glob("switch-*.json")):
        try:
            with open(switch_file, "r") as f:
                switch = json.load(f)

            # Apply filters
            if from_project and switch.get("from_project") != from_project:
                continue
            if to_project and switch.get("to_project") != to_project:
                continue

            switches.append(switch)
        except Exception as e:
            self.validator.audit_log("query_switches", str(switch_file), False, str(e))

    return switches
```

**Query Capabilities**:
- Filter by source project
- Filter by destination project
- Filter by both (specific transition)
- Returns chronologically sorted results

### Intelligent Suggestions

```python
def suggest_switch_approach(self, from_project: str, to_project: str) -> Dict[str, Any]:
    """Suggest optimal switch approach based on learned patterns"""
    similar_switches = self.query_switches(from_project, to_project)

    if not similar_switches:
        return {
            "suggestion": "commit",  # Default to commit
            "confidence": 0.50,
            "reason": "No historical data - using safe default",
            "avg_duration": None,
            "sample_size": 0
        }

    # Analyze patterns
    commit_count = sum(1 for s in similar_switches if s["preservation_method"] == "commit")
    stash_count = len(similar_switches) - commit_count
    total = len(similar_switches)

    avg_duration = sum(s["duration_seconds"] for s in similar_switches) / total

    if commit_count > stash_count:
        return {
            "suggestion": "commit",
            "confidence": commit_count / total,
            "reason": f"You usually commit when switching between these projects ({commit_count}/{total} times)",
            "avg_duration": avg_duration,
            "sample_size": total
        }
    else:
        return {
            "suggestion": "stash",
            "confidence": stash_count / total,
            "reason": f"You usually stash when switching between these projects ({stash_count}/{total} times)",
            "avg_duration": avg_duration,
            "sample_size": total
        }
```

**Confidence Scoring**:
- Higher sample size → Higher reliability
- Pattern consistency → Higher confidence
- Default fallback when no data available
- Explainable recommendations with reasoning

---

## Performance Benefits

Based on Anthropic official measurements:

| Feature | Performance Improvement | Source |
|---------|------------------------|--------|
| Context editing + memory | **39% improvement** | Anthropic News |
| Context editing alone | **29% improvement** | Anthropic News |
| Memory tool learning | **+10% boost** | Derived (39% - 29%) |

**Key Benefit**: Memory tool enables personalized workflows that adapt to user patterns over time.

---

## Usage Patterns

### Recording Switch Operations

```python
from context_manager import MemoryManager
import time

memory = MemoryManager()

# Before switch
start_time = time.time()

# ... perform switch operation ...

# After switch
duration = time.time() - start_time

memory.remember_switch(
    from_project="feature-dashboard",
    to_project="fix-pipeline-error",
    preservation_method="commit",
    duration_seconds=duration
)
```

### Querying Historical Patterns

```python
# Query all switches from a project
switches = memory.query_switches(from_project="feature-dashboard")
print(f"Found {len(switches)} historical switches from dashboard project")

# Query specific transition
transitions = memory.query_switches(
    from_project="feature-dashboard",
    to_project="fix-pipeline-error"
)
```

### Getting Suggestions

```python
# Get AI-powered suggestion
suggestion = memory.suggest_switch_approach(
    from_project="feature-dashboard",
    to_project="fix-pipeline-error"
)

print(f"Suggested approach: {suggestion['suggestion']}")
print(f"Confidence: {suggestion['confidence']:.0%}")
print(f"Reason: {suggestion['reason']}")
print(f"Avg duration: {suggestion['avg_duration']:.1f}s")
```

---

## Integration with Enhanced /switch

### Automatic Learning

The enhanced `/switch` command automatically learns from every operation:

```bash
./scripts/switch.sh feature-new-work

# Internally:
# 1. START_TIME = record start
# 2. Execute switch workflow
# 3. END_TIME = record end
# 4. memory.remember_switch(from, to, method, duration)
# 5. Pattern recorded for future optimization
```

### Suggestion Integration (Future)

```bash
./scripts/switch.sh feature-previous-work

# Future capability:
# 🧠 Analyzing switch patterns...
# Based on 17 similar switches:
#   Suggested: commit (85% confidence)
#   Reason: You usually commit between these projects
#   Avg time: 12.3 seconds
```

---

## Security Best Practices

### Do's ✅

1. **Always validate paths** before file operations
2. **Always sanitize content** before storage
3. **Always audit log** operations for security review
4. **Use memory scopes** to isolate different types of data
5. **Implement error handling** for corrupted memory files

### Don'ts ❌

1. **Don't trust user input** - always sanitize
2. **Don't skip validation** even for "trusted" paths
3. **Don't store sensitive data** in memory (API keys, passwords)
4. **Don't ignore audit logs** - review monthly for anomalies
5. **Don't allow unbounded growth** - implement retention policies

---

## Limitations and Future Work

### Current Limitations

1. **Linear scan for queries**: O(n) performance (acceptable for <10K records)
2. **No indexing**: Simple file-based storage
3. **Manual pattern interpretation**: No ML-based pattern recognition

### Future Enhancements

1. **SQLite Backend**: Efficient querying and indexing
2. **LRU Cache**: Frequent memory access optimization
3. **Compression**: Older memory records compressed for space
4. **ML Pattern Recognition**: Advanced pattern detection and prediction
5. **Distributed Memory**: Cross-team memory sharing (with permission)

---

## References

### Anthropic Official Documentation
- **Memory Tool Cookbook**: https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/memory_cookbook.ipynb
- **Claude Code Best Practices**: https://www.anthropic.com/engineering/claude-code-best-practices
- **Security Guidance**: Anthropic documentation on prompt injection prevention

### Implementation Files
- **Core Library**: `scripts/lib/context_manager.py` (MemoryManager, SecurityValidator)
- **Enhanced Switch**: `scripts/switch.sh` (automatic memory learning)
- **Library Docs**: `scripts/lib/README.md` (complete API reference)

---

## Success Criteria

✅ **Successful implementation includes**:
- Path traversal prevention with base directory validation
- Prompt injection sanitization with pattern matching
- Comprehensive audit logging to JSONL format
- Memory scope isolation (switch-contexts, project-contexts, etc.)
- Cross-session persistence with JSON storage
- Intelligent suggestions with confidence scoring

❌ **Common mistakes to avoid**:
- Skipping path validation (security vulnerability)
- Not sanitizing content (prompt injection risk)
- Missing audit logs (no security visibility)
- Mixing memory scopes (data contamination)
- Unbounded storage growth (disk space issues)

---

*Memory tool implementation patterns - Following Anthropic Claude Cookbook*
*Production-ready pattern with security-first design from enhanced /switch command project*
