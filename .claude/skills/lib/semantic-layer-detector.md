# dbt Semantic Layer Capability Detection

**Purpose**: Detect if Semantic Layer is available before making MCP calls to avoid unnecessary errors

**Location**: `.claude/skills/lib/semantic-layer-detector.md`
**Version**: 1.0.0
**Status**: Production

---

## Quick Reference

```yaml
# Check BEFORE any semantic layer operations

semantic_status = detect_semantic_layer()

IF semantic_status.available:
  # Safe to use Semantic Layer MCP tools
  metrics = mcp__dbt-mcp__list_metrics()
ELSE:
  # Skip semantic layer features
  # Show reason to user
  Display: "Semantic Layer not available: {semantic_status.reason}"
```

---

## Semantic Layer Requirements

**Required for Availability**:
1. ✅ dbt Cloud (not dbt Core)
2. ✅ Team or Enterprise tier (not Developer/free)
3. ✅ Semantic Layer enabled in environment
4. ✅ At least one metric defined in project

**If ANY requirement not met** → Semantic Layer unavailable

---

## Detection Workflow

```yaml
Function: detect_semantic_layer()

  # Check 1: Platform (must be Cloud)
  platform = detect_dbt_platform()

  IF platform != "dbt_cloud":
    RETURN {
      "available": false,
      "reason": "Semantic Layer requires dbt Cloud (you're on dbt Core)",
      "tier_required": null,
      "metrics_count": 0,
      "suggestion": "Semantic Layer is Cloud-only. Define metrics in YAML locally but no query API available."
    }

  # Check 2: Cloud Tier (must be Team or Enterprise)
  cloud_tier = detect_cloud_tier()

  IF cloud_tier == "developer":
    RETURN {
      "available": false,
      "reason": "Semantic Layer requires Team or Enterprise tier (you're on Developer/free)",
      "tier_required": "team_or_enterprise",
      "metrics_count": 0,
      "suggestion": "Upgrade to Team tier ($100/seat) to enable Semantic Layer"
    }

  # Check 3: Metrics Configured (non-invasive check)
  metrics_status = check_metrics_configured()

  IF metrics_status.error:
    # Semantic Layer not enabled in environment
    RETURN {
      "available": false,
      "reason": "Semantic Layer not enabled in dbt Cloud environment",
      "tier_required": "team_or_enterprise",
      "metrics_count": 0,
      "suggestion": "Enable Semantic Layer in dbt Cloud environment settings"
    }

  IF metrics_status.count == 0:
    # Enabled but no metrics defined
    RETURN {
      "available": false,
      "reason": "No metrics defined in project yet",
      "tier_required": null,
      "metrics_count": 0,
      "suggestion": "Define metrics in MetricFlow YAML to use Semantic Layer",
      "can_create_metrics": true
    }

  # All checks passed - Semantic Layer available!
  RETURN {
    "available": true,
    "reason": "Semantic Layer configured and ready",
    "tier": cloud_tier,
    "metrics_count": metrics_status.count,
    "metrics_sample": metrics_status.sample_names[:5]  # Show first 5
  }
```

---

## Cloud Tier Detection

```yaml
Function: detect_cloud_tier()

  # Method 1: Check MCP API availability (most reliable)
  TRY:
    # Try to access Admin API (Team+ feature)
    test = mcp__dbt-mcp__list_jobs_runs(limit=1)

    IF success:
      # Admin API available = at least Team tier
      RETURN "team_or_enterprise"

  CATCH "API not available" OR "Unauthorized":
    # Admin API not available = Developer tier
    RETURN "developer"

  # Method 2: Check environment variables (Cloud-specific)
  IF env_var_exists("DBT_CLOUD_PLAN_TYPE"):
    plan = get_env("DBT_CLOUD_PLAN_TYPE")

    IF plan in ["team", "enterprise"]:
      RETURN plan
    ELSE:
      RETURN "developer"

  # Method 3: Ask user (last resort)
  Display: "What dbt Cloud tier are you on?
            1. Developer (free tier)
            2. Team ($100/seat)
            3. Enterprise (custom pricing)

            Not sure? Check: https://cloud.getdbt.com/settings"

  user_choice = get_user_input()

  tier_map = {
    "1": "developer",
    "2": "team",
    "3": "enterprise"
  }

  RETURN tier_map[user_choice]
```

---

## Metrics Configuration Check

```yaml
Function: check_metrics_configured()

  # Non-invasive check using MCP list_metrics()
  # This doesn't query data, just lists metadata

  TRY:
    metrics_result = mcp__dbt-mcp__list_metrics()

    IF metrics_result.error:
      # Semantic Layer not enabled
      RETURN {
        "configured": false,
        "count": 0,
        "error": metrics_result.error_message
      }

    IF len(metrics_result.metrics) == 0:
      # Enabled but no metrics defined
      RETURN {
        "configured": false,
        "count": 0,
        "error": null,
        "message": "No metrics defined"
      }

    # Metrics exist!
    RETURN {
      "configured": true,
      "count": len(metrics_result.metrics),
      "sample_names": [m.name for m in metrics_result.metrics[:5]],
      "error": null
    }

  CATCH MCP_ERROR as e:
    # MCP not configured or Semantic Layer not available
    RETURN {
      "configured": false,
      "count": 0,
      "error": str(e)
    }
```

---

## Saved Configuration

```json
{
  "semantic_layer_available": true,
  "platform": "dbt_cloud",
  "cloud_tier": "team",
  "metrics_count": 23,
  "metrics_sample": [
    "revenue",
    "customer_lifetime_value",
    "monthly_active_users",
    "conversion_rate",
    "churn_rate"
  ],
  "last_verified": "2025-10-22T14:45:00Z",
  "safe_sl_operations": [
    "list_metrics",
    "get_dimensions",
    "query_metrics",
    "get_metrics_compiled_sql"
  ]
}
```

**Config Location**: Embedded in `.claude/dbt-mcp-config.json`

---

## User-Facing Messages

### Semantic Layer Available

```
✅ Semantic Layer: AVAILABLE

Platform: dbt Cloud (Team tier)
Metrics Defined: 23 metrics

Available metrics:
  • revenue
  • customer_lifetime_value
  • monthly_active_users
  • conversion_rate
  • churn_rate
  ... and 18 more

You can query these metrics with governed business logic.
```

### Semantic Layer Not Available - Core User

```
❌ Semantic Layer: NOT AVAILABLE

Reason: Semantic Layer requires dbt Cloud (you're using dbt Core)

Alternative for dbt Core:
  • Define metrics in MetricFlow YAML files locally
  • No Semantic Layer query API available
  • Metrics available for documentation only

To use Semantic Layer: Upgrade to dbt Cloud Team tier
```

### Semantic Layer Not Available - Developer Tier

```
❌ Semantic Layer: NOT AVAILABLE

Platform: dbt Cloud (Developer tier)
Reason: Semantic Layer requires Team or Enterprise tier

Current Tier: Developer (free)
Required Tier: Team ($100/seat) or Enterprise

Upgrade: https://cloud.getdbt.com/settings/billing
```

### Semantic Layer Not Available - Not Enabled

```
⚠️ Semantic Layer: NOT ENABLED

Platform: dbt Cloud (Team tier) ✅
Tier: Supports Semantic Layer ✅
Configuration: Semantic Layer not enabled in environment ❌

Enable Semantic Layer:
  1. Go to dbt Cloud Environment Settings
  2. Enable "Semantic Layer" feature
  3. Configure connection credentials

Documentation: https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl
```

### Semantic Layer Enabled But No Metrics

```
⚠️ Semantic Layer: NO METRICS DEFINED

Platform: dbt Cloud (Team tier) ✅
Semantic Layer: Enabled ✅
Metrics Defined: 0 ❌

Next Steps:
  1. Define metrics in MetricFlow YAML
  2. Example:
     ```yaml
     metrics:
       - name: revenue
         type: simple
         type_params:
           measure: revenue_amount
     ```
  3. Deploy to Cloud
  4. Metrics will appear in Semantic Layer

Documentation: https://docs.getdbt.com/docs/build/metrics-overview
```

---

## Integration with Skills

### Example: Skill with Optional Semantic Layer Features

```yaml
name: dbt-model-scaffolder
# Works on both platforms, Semantic Layer optional

## Step 0: Detect Semantic Layer (optional feature check)

semantic_status = detect_semantic_layer()

IF semantic_status.available:
  # Offer metric integration option
  Display: "Semantic Layer available ({semantic_status.metrics_count} metrics)"
  Ask: "Is this model related to any metrics? (y/n)"

  IF user says yes:
    metrics = mcp__dbt-mcp__list_metrics()
    Display: "Available metrics: {metrics}"
    Ask: "Select metrics to reference (comma-separated):"
    selected_metrics = user_input

    # Add metric references to model YAML
    # ... generate with metric metadata ...

ELSE:
  # Skip metric features silently
  # Don't confuse user with unavailable features
  # Just focus on standard model creation
```

### Example: Skill that Requires Semantic Layer

```yaml
name: dbt-cloud-semantic-layer-explorer
# Requires Semantic Layer - platform-specific

## Step 0: Validate Semantic Layer (REQUIRED)

semantic_status = detect_semantic_layer()

IF NOT semantic_status.available:
  # Show detailed error with guidance
  display_semantic_layer_error(semantic_status)
  EXIT skill

# If we reach here, Semantic Layer is available
Display: "Semantic Layer available - {semantic_status.metrics_count} metrics ready"

# Proceed with Semantic Layer operations...
```

---

## Avoid Unnecessary MCP Calls

```yaml
# ❌ BAD: Try MCP call and handle error
TRY:
  metrics = mcp__dbt-mcp__list_metrics()
CATCH error:
  Display: "Semantic Layer not available"

# Problem: Makes unnecessary MCP call, slow error handling


# ✅ GOOD: Detect first, then call
semantic_status = detect_semantic_layer()

IF semantic_status.available:
  metrics = mcp__dbt-mcp__list_metrics()
ELSE:
  # Skip entirely, show helpful message
  Display: "Semantic Layer not available: {semantic_status.reason}"
  Display: "Suggestion: {semantic_status.suggestion}"

# Benefit: Fast detection, no failed MCP calls, better UX
```

---

## Testing

```bash
# Test on dbt Core (should fail platform check)
$ cd /path/to/core/project
# Run detection
# Expected: "Semantic Layer requires dbt Cloud (you're on dbt Core)"

# Test on dbt Cloud Developer tier
$ cd /path/to/cloud/dev/project
# Run detection
# Expected: "Semantic Layer requires Team or Enterprise tier"

# Test on dbt Cloud Team tier with no metrics
$ cd /path/to/cloud/team/project
# Run detection
# Expected: "No metrics defined in project yet"

# Test on dbt Cloud Team tier with metrics
$ cd /path/to/cloud/team/project-with-metrics
# Run detection
# Expected: "Semantic Layer available - 23 metrics"
```

---

## Maintenance

**Re-detection Triggers**:
- First time using Semantic Layer in a session
- After metrics are added to project
- After upgrading Cloud tier
- Config older than 24 hours

**Update Frequency**: Check once per session, cache result

---

**Version**: 1.0.0
**Last Updated**: 2025-10-22
**Maintainer**: ADLC Platform Team
