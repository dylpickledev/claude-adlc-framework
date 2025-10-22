# dbt MCP Project Size Detection Framework

**Purpose**: Detect dbt project size to avoid MCP token overflow on large projects (>500 models)

**Location**: `.claude/skills/lib/mcp-project-size-detector.md`
**Version**: 1.0.0
**Status**: Production

---

## Quick Reference

```yaml
# Run BEFORE any MCP inventory operations (get_all_models, etc.)

project_size = detect_project_size()

IF project_size == "LARGE":
  # NEVER use get_all_models() - token overflow
  # Use targeted MCP calls only
  strategy = "TARGETED"

ELIF project_size == "MEDIUM":
  # Use get_all_models() with caution
  # Prefer filtered approaches
  strategy = "SELECTIVE"

ELSE:  # SMALL
  # Safe to use get_all_models()
  strategy = "FULL_ACCESS"
```

---

## Project Size Classification

| Size | Model Count | MCP Strategy | Risk Level |
|------|-------------|--------------|------------|
| **SMALL** | < 100 models | Full MCP access | ✅ Low - safe for all MCP tools |
| **MEDIUM** | 100-500 models | Selective MCP | ⚠️ Medium - use with caution |
| **LARGE** | > 500 models | Targeted MCP only | 🚨 High - avoid inventory tools |

---

## Detection Methods (Ordered by Speed)

### Method 1: Check Saved Configuration (Fastest - 0.1s)

```bash
# Check if project size already detected
IF file_exists(".claude/dbt-mcp-config.json"):
  config = read_json(".claude/dbt-mcp-config.json")

  IF config.last_verified within 24 hours:
    # Recent detection, trust it
    RETURN {
      "size": config.project_size,
      "model_count": config.model_count,
      "strategy": config.mcp_strategy,
      "cached": true
    }
  ELSE:
    # Re-verify (project may have grown)
    CONTINUE to Method 2
```

---

### Method 2: dbt CLI Model Count (Fast - 1-2s)

```bash
# Use dbt list to count models without loading data
# Works on both dbt Core and dbt Cloud

command = "dbt list --resource-type model --output name"
result = run_command(command)

# Count lines in output
model_count = count_lines(result)

# Classify size
IF model_count > 500:
  project_size = "LARGE"
  mcp_strategy = "TARGETED"

ELIF model_count > 100:
  project_size = "MEDIUM"
  mcp_strategy = "SELECTIVE"

ELSE:
  project_size = "SMALL"
  mcp_strategy = "FULL_ACCESS"

# Save config
save_project_size_config(project_size, model_count, mcp_strategy)

RETURN {
  "size": project_size,
  "model_count": model_count,
  "strategy": mcp_strategy,
  "detection_method": "dbt_list"
}
```

---

### Method 3: File System Count (Fallback - 1s)

```bash
# If dbt list fails, count .sql files in models directory
# Less accurate (includes disabled models, analyses)

model_files = glob("models/**/*.sql")
model_count = len(model_files)

# Add 10% buffer for accuracy (file count may differ from dbt list)
estimated_count = model_count * 1.1

# Classify with conservative thresholds
IF estimated_count > 500:
  project_size = "LARGE"
ELIF estimated_count > 100:
  project_size = "MEDIUM"
ELSE:
  project_size = "SMALL"

Display: "⚠️ Estimated project size from file count (less accurate than dbt list)"

RETURN {
  "size": project_size,
  "model_count": int(estimated_count),
  "strategy": get_strategy(project_size),
  "detection_method": "file_system",
  "estimated": true
}
```

---

### Method 4: Manifest Size Check (Optional Verification)

```bash
# Additional verification if manifest.json exists
# Large manifest = large project

IF file_exists("target/manifest.json"):
  manifest_size = get_file_size_mb("target/manifest.json")

  # Heuristic: Large manifests indicate many models
  IF manifest_size > 10:
    project_size_hint = "LARGE"
  ELIF manifest_size > 3:
    project_size_hint = "MEDIUM"
  ELSE:
    project_size_hint = "SMALL"

  # Cross-check with other methods
  IF project_size_hint != detected_size:
    Display: "⚠️ Manifest size suggests {project_size_hint}, but detection shows {detected_size}"
```

---

## MCP Usage Strategies by Project Size

### SMALL Projects (<100 models)

```yaml
Safe MCP Operations:
  ✅ get_all_models()           # Returns all models at once
  ✅ get_mart_models()          # Returns mart layer models
  ✅ Batch operations           # Process multiple models

MCP Approach:
  - Use inventory tools freely
  - Load full project context
  - No special filtering needed

Token Risk: LOW
```

---

### MEDIUM Projects (100-500 models)

```yaml
Selective MCP Operations:
  ⚠️ get_all_models()           # Use with caution, may be slow
  ✅ get_model_details(name)    # Targeted single-model calls
  ✅ get_model_parents(name)    # Safe - limited scope
  ✅ get_model_children(name)   # Safe - limited scope

MCP Approach:
  - Prefer filtered queries
  - Ask user for specific model names
  - Use dbt list with selectors first
  - Paginate if loading many models

Token Risk: MEDIUM

Best Practice:
  "Instead of get_all_models(), ask user:
   'Which model are you working on?'
   Then use targeted get_model_details()"
```

---

### LARGE Projects (>500 models)

```yaml
Targeted MCP Operations ONLY:
  ❌ get_all_models()           # NEVER - token overflow risk
  ❌ get_mart_models()          # AVOID - still too many models
  ✅ get_model_details(name)    # Safe - single model only
  ✅ get_model_parents(name)    # Safe - limited scope
  ✅ get_model_children(name)   # Safe - limited scope

MCP Approach:
  - ALWAYS ask for specific model name first
  - Use dbt CLI selectors for discovery
  - Never attempt inventory operations
  - Process one model at a time

Token Risk: HIGH

Error Prevention:
  "STOP - Large project detected (>500 models)

   MCP get_all_models() will fail (token overflow).

   Please specify which model to analyze:
   (Or use: dbt list --select tag:your_tag)"
```

---

## Saved Configuration Format

```json
{
  "project_size": "LARGE",
  "model_count": 847,
  "mcp_strategy": "TARGETED",
  "detection_method": "dbt_list",
  "last_verified": "2025-10-22T14:30:00Z",
  "project_path": "/Users/dylanmorrish/analytics/dbt_project",
  "safe_mcp_operations": [
    "get_model_details",
    "get_model_parents",
    "get_model_children"
  ],
  "unsafe_mcp_operations": [
    "get_all_models",
    "get_mart_models"
  ],
  "recommendations": [
    "Always ask user for specific model name before MCP calls",
    "Use dbt list with selectors for model discovery",
    "Never attempt inventory operations"
  ]
}
```

**Config Location**: `.claude/dbt-mcp-config.json` (gitignored)

---

## Integration with Skills

### Example: dbt-model-impact-analyzer

```yaml
## Step 0: Project Size Detection

project_info = detect_project_size()

Display: "📊 Project: {project_info.size} ({project_info.model_count} models)"
Display: "   MCP Strategy: {project_info.strategy}"

## Step 1: Get Model Name (approach depends on size)

IF project_info.size == "SMALL":
  # Can offer model list
  all_models = mcp__dbt-mcp__get_all_models()
  Display: "Available models: {all_models}"
  Ask: "Which model to analyze?"
  model_name = user_selection

ELIF project_info.size in ["MEDIUM", "LARGE"]:
  # Must ask for specific name
  Display: "Specify model name to analyze:"
  Display: "(Tip: Use 'dbt list --select tag:your_tag' to find models)"
  model_name = user_input

## Step 2: Targeted MCP Calls (safe for all sizes)

model_details = mcp__dbt-mcp__get_model_details(model_name)
parents = mcp__dbt-mcp__get_model_parents(model_name)
children = mcp__dbt-mcp__get_model_children(model_name)

# Proceed with analysis...
```

---

## Detection Workflow

```yaml
Function: detect_project_size()

  # Try saved config first
  IF cached_config_valid():
    RETURN load_cached_config()

  # Try dbt list (most accurate)
  TRY:
    result = run_dbt_list()
    size_info = classify_by_model_count(result.model_count)
    save_config(size_info)
    RETURN size_info

  CATCH dbt_error:
    # Fallback to file count
    result = count_sql_files()
    size_info = classify_by_file_count(result.file_count)
    size_info.estimated = true
    save_config(size_info)
    RETURN size_info
```

---

## User-Facing Messages

### Small Project Detected
```
✅ Project Size: SMALL (67 models)

MCP Strategy: Full access
- Safe to use get_all_models()
- No token overflow risk
- Full project context available
```

### Medium Project Detected
```
⚠️ Project Size: MEDIUM (347 models)

MCP Strategy: Selective use
- get_all_models() may be slow
- Prefer targeted model queries
- Specify model names when possible

Tip: Use dbt list --select <selector> for discovery
```

### Large Project Detected
```
🚨 Project Size: LARGE (847 models)

MCP Strategy: Targeted only
- get_all_models() DISABLED (token overflow risk)
- Always specify model name
- Use dbt CLI selectors for discovery

Required: Provide specific model names for MCP operations
```

---

## Testing

```bash
# Test detection on small project
$ cd /path/to/small/project  # <100 models
$ dbt list --resource-type model | wc -l
67
# Expected: SMALL classification

# Test detection on medium project
$ cd /path/to/medium/project  # 100-500 models
$ dbt list --resource-type model | wc -l
347
# Expected: MEDIUM classification

# Test detection on large project
$ cd /path/to/large/project  # >500 models
$ dbt list --resource-type model | wc -l
847
# Expected: LARGE classification

# Verify saved config
$ cat .claude/dbt-mcp-config.json
# Should show correct size and strategy
```

---

## Maintenance

**Re-detection Triggers**:
- Config older than 24 hours → Re-verify
- User adds many new models → Re-verify
- MCP operations start failing → Re-verify
- User explicitly requests detection

**Update Frequency**: Daily automatic re-check

---

**Version**: 1.0.0
**Last Updated**: 2025-10-22
**Maintainer**: ADLC Platform Team
