# dbt Platform Detection Framework

**Purpose**: Detect whether user is on dbt Core or dbt Cloud to ensure skills use correct workflows

**Location**: `.claude/skills/lib/platform-detector.md`
**Version**: 1.0.0
**Status**: Production

---

## Quick Reference

```yaml
# Include this at the start of EVERY dbt skill

platform = detect_dbt_platform()

IF platform == "dbt_core":
  # Use Core-specific workflow
ELIF platform == "dbt_cloud":
  # Use Cloud-specific workflow
ELSE:
  # Ask user and save answer
```

---

## Detection Methods (In Order of Priority)

### Method 1: Check Saved Configuration (Fastest)

```bash
# Check if platform already detected and saved
IF file_exists(".claude/dbt-platform-config.json"):
  config = read_json(".claude/dbt-platform-config.json")

  IF config.last_verified within 7 days:
    platform = config.platform
    RETURN platform
  ELSE:
    # Re-verify (might have changed)
    CONTINUE to Method 2
```

**Config Format**:
```json
{
  "platform": "dbt_core",
  "dbt_version": "1.8.3",
  "last_verified": "2025-10-22T10:30:00Z",
  "project_path": "/Users/dylanmorrish/analytics/dbt_project",
  "verified_by": "dbt --version"
}
```

---

### Method 2: Check dbt Version Output (Most Reliable)

```bash
# Run dbt --version and parse output
output = run_command("dbt --version")

# dbt Cloud output examples:
#   "dbt Cloud CLI - 0.35.1 (dbt-core: 1.8.0)"
#   "dbt Cloud IDE"

# dbt Core output examples:
#   "Core:\n  - installed: 1.8.3"
#   "installed version: 1.8.3"

IF "Cloud" in output OR "cloud" in output:
  platform = "dbt_cloud"
  dbt_version = extract_version(output)  # Get Core version underneath

ELIF "Core" in output OR "installed" in output:
  platform = "dbt_core"
  dbt_version = extract_version(output)

ELSE:
  # Inconclusive, continue to Method 3
  CONTINUE
```

---

### Method 3: Check Environment Variables

```bash
# dbt Cloud sets specific environment variables
cloud_vars = [
  "DBT_CLOUD_PROJECT_ID",
  "DBT_CLOUD_ACCOUNT_ID",
  "DBT_CLOUD_ENVIRONMENT_ID",
  "DBT_CLOUD_RUN_ID"
]

IF any environment variable exists:
  platform = "dbt_cloud"
  RETURN platform

ELSE:
  # Still inconclusive, continue to Method 4
  CONTINUE
```

---

### Method 4: Check for Cloud-Specific Files

```bash
# dbt Cloud IDE creates specific files
cloud_indicators = [
  ".dbt_cloud",
  ".dbt/cloud.yml"
]

IF any file exists:
  platform = "dbt_cloud"
  RETURN platform
```

---

### Method 5: Ask User Directly (Last Resort)

```bash
# If all detection methods fail, ask user
Display: "I need to determine your dbt platform to provide the right workflow.

          Are you using:

          1. dbt Core (running dbt locally on your machine via terminal)
             Examples: dbt run, dbt test from command line

          2. dbt Cloud (using dbt Cloud IDE or Cloud-scheduled jobs)
             Examples: Developing in browser IDE, jobs in dbt Cloud UI

          Enter 1 for Core, 2 for Cloud:"

user_input = get_user_choice()

IF user_input == "1":
  platform = "dbt_core"
ELIF user_input == "2":
  platform = "dbt_cloud"
ELSE:
  ERROR: "Invalid selection. Please choose 1 or 2."
  RETRY

# Save answer for future skills
save_platform_config(platform)
```

---

## Save Platform Configuration

```yaml
# After successful detection, save to avoid re-detection

Function: save_platform_config(platform, dbt_version=null)

  config = {
    "platform": platform,
    "dbt_version": dbt_version,
    "last_verified": current_timestamp(),
    "project_path": current_working_directory(),
    "verified_by": detection_method_used
  }

  write_json(".claude/dbt-platform-config.json", config)

  Display: "✅ Platform detected: {platform}"
  IF dbt_version:
    Display: "   dbt version: {dbt_version}"
```

---

## Platform Validation for Skills

```yaml
# Use this in every skill's Step 0

Function: validate_platform_for_skill(skill_name, required_platform)

  detected_platform = detect_dbt_platform()

  IF detected_platform NOT IN required_platform:
    # Platform mismatch
    display_platform_error(
      skill_name=skill_name,
      detected=detected_platform,
      required=required_platform
    )
    EXIT skill

  ELSE:
    # Platform matches, proceed
    RETURN detected_platform
```

---

## Error Messages

### Core User Tries Cloud Skill

```yaml
Function: display_platform_error_core_to_cloud(skill_name)

Display:
  "❌ Platform Mismatch

  Detected Platform: dbt Core (local CLI)
  This skill requires: dbt Cloud

  '{skill_name}' uses dbt Cloud-specific features:
  - Cloud APIs (jobs, Discovery API, Semantic Layer)
  - Cloud IDE integration
  - Cloud job scheduling

  dbt Core doesn't have these features.

  💡 Alternative for dbt Core:
  {suggest_core_alternative(skill_name)}

  Or upgrade to dbt Cloud: https://www.getdbt.com/pricing"
```

### Cloud User Tries Core Skill

```yaml
Function: display_platform_error_cloud_to_core(skill_name)

Display:
  "❌ Platform Mismatch

  Detected Platform: dbt Cloud
  This skill requires: dbt Core (local CLI access)

  '{skill_name}' uses local dbt CLI commands:
  - Direct file system access
  - Local dbt run/test/compile
  - Local docs generation

  dbt Cloud uses IDE and jobs instead of local CLI.

  💡 Alternative for dbt Cloud:
  {suggest_cloud_alternative(skill_name)}

  Or use dbt Cloud IDE features instead of CLI"
```

---

## Platform-Specific Alternative Suggestions

```yaml
# Map skills to their platform alternatives

skill_alternatives = {
  # Cloud skill → Core alternative
  "dbt-cloud-job-monitor": {
    "core_alternative": "dbt-core-local-runner",
    "explanation": "Run models directly with: dbt run --select {model}"
  },

  "dbt-cloud-semantic-layer-explorer": {
    "core_alternative": null,
    "explanation": "Semantic Layer is Cloud-only. Define metrics locally in YAML but no query API."
  },

  "dbt-cloud-discovery-navigator": {
    "core_alternative": "dbt-core-model-analyzer",
    "explanation": "Analyze models via file reads instead of Discovery API"
  },

  # Core skill → Cloud alternative
  "dbt-core-local-runner": {
    "cloud_alternative": "Use dbt Cloud IDE 'Preview' button",
    "explanation": "Click 'Preview' in IDE to run models interactively"
  },

  "dbt-core-docs-generator": {
    "cloud_alternative": "Use dbt Cloud built-in documentation",
    "explanation": "View docs in Cloud UI under Documentation tab"
  }
}
```

---

## Complete Detection Example

```yaml
# Example: dbt-test-suite-generator (universal skill)

## Step 0: Platform Detection (ALWAYS FIRST)

platform = detect_dbt_platform()

# This skill works on both platforms (file generation)
# No platform validation needed

Display: "Detected platform: {platform}"

## Step 1: Version Detection (platform-aware)

IF platform == "dbt_core":
  # Get version from dbt --version
  version_output = run_command("dbt --version")
  dbt_version = parse_version(version_output)

ELIF platform == "dbt_cloud":
  # Cloud might have different version than Core underneath
  # Cloud CLI version may differ from dbt-core version
  version_output = run_command("dbt --version")
  dbt_version = parse_core_version(version_output)

  Display: "Note: Using dbt Cloud (underlying dbt-core: {dbt_version})"

## Step 2: Proceed with skill (same workflow for both)
# ... skill continues ...
```

---

## Version Detection (Platform-Aware)

```yaml
# dbt version parsing differs by platform

Function: detect_dbt_version(platform)

  version_output = run_command("dbt --version")

  IF platform == "dbt_core":
    # Parse Core version
    # Example: "Core:\n  - installed: 1.8.3"
    version = extract_version_core(version_output)

  ELIF platform == "dbt_cloud":
    # Parse underlying dbt-core version
    # Example: "dbt Cloud CLI - 0.35.1 (dbt-core: 1.8.0)"
    version = extract_core_version_from_cloud(version_output)

  RETURN version

# Parse into major.minor.patch
Function: parse_version(version_string)
  # "1.8.3" → {major: 1, minor: 8, patch: 3}
  parts = version_string.split(".")

  RETURN {
    "major": int(parts[0]),
    "minor": int(parts[1]),
    "patch": int(parts[2]) if len(parts) > 2 else 0,
    "full": version_string
  }
```

---

## Usage in Skills

### Universal Skill Example
```yaml
---
name: dbt-test-suite-generator
platform: ["dbt_core", "dbt_cloud"]  # Works on both
---

# Step 0: Platform detection (informational only)
platform = detect_dbt_platform()
version = detect_dbt_version(platform)

# No platform validation needed (works everywhere)

# Step 1: Version validation (feature-specific)
IF version.minor >= 8:
  unit_tests_available = true
ELSE:
  unit_tests_available = false

# Proceed with skill...
```

### Platform-Specific Skill Example
```yaml
---
name: dbt-cloud-job-monitor
platform: ["dbt_cloud"]  # Cloud ONLY
---

# Step 0: Platform validation (REQUIRED)
platform = validate_platform_for_skill(
  skill_name="dbt-cloud-job-monitor",
  required_platform=["dbt_cloud"]
)

# If we reach here, platform is validated
# Proceed with Cloud-specific MCP calls...
```

---

## Testing Platform Detection

```bash
# Test detection on dbt Core
$ cd /path/to/core/project
$ dbt --version
# Should detect: "dbt_core"

# Test detection on dbt Cloud
$ cd /path/to/cloud/project
$ dbt --version
# Should detect: "dbt_cloud"

# Test saved config
$ cat .claude/dbt-platform-config.json
# Should show detected platform with timestamp
```

---

## Maintenance

**Re-detection Triggers**:
- Config older than 7 days → Re-verify
- User explicitly runs platform detection skill
- Skill fails due to platform mismatch → Re-verify
- User switches projects → New detection

**Config Location**: `.claude/dbt-platform-config.json` (gitignored)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-22
**Maintainer**: ADLC Platform Team
