# 🔍 Sherlock Holmes Investigation Bureau

A Victorian-themed orchestration system for deploying multiple Claude instances to investigate dbt Cloud issues in parallel.

## Quick Start

```bash
# 1. Dispatch investigation cases
./sherlock/bureau/dispatch-cases.sh

# 2. Deploy detective squad  
./sherlock/bureau/deploy-detectives.sh

# 3. Monitor progress
./sherlock/bureau/check-investigations.sh

# 4. Compile evidence
./sherlock/bureau/compile-evidence.sh
```

## How It Works

### The Investigation Process

1. **Case Dispatch** 📋
   - Analyzes dbt issue analysis to create investigation cases
   - Each case gets assigned priority, issues, and detective type
   - Creates case briefs with investigation protocols

2. **Detective Deployment** 🕵️
   - Launches multiple Claude instances as specialized detectives
   - Each detective opens in a new terminal with case-specific context
   - Pre-loaded with sub-agent deployment instructions

3. **Investigation Monitoring** 📊  
   - Watson-style progress tracking across all active cases
   - Shows case status, evidence compilation, and blockers
   - Continuous monitoring mode available

4. **Evidence Compilation** 📄
   - Aggregates findings from all detective investigations
   - Generates actionable reports for implementation
   - Creates PR readiness assessments and next action lists

## Directory Structure

```
sherlock/
├── bureau/                 # Core orchestration scripts
│   ├── dispatch-cases.sh      # Generate investigation cases
│   ├── deploy-detectives.sh   # Launch detective squad
│   ├── check-investigations.sh # Monitor progress 
│   └── compile-evidence.sh    # Aggregate findings
├── cases/                  # Investigation case files
│   ├── the-camera-mystery/        # High priority cases
│   ├── inventory-ledger-affair/   # Cross-system issues
│   ├── pr-review-critical/        # Ready-to-merge analysis
│   └── case-coordination.md       # Central coordination hub
├── evidence/               # Compiled investigation results
└── templates/              # Standardized case templates
```

## Case Types

### 🔴 High Priority Cases
- **The Camera Mystery** - 5.3M duplicate camera records
- **Inventory Ledger Affair** - JDE F4111 vs data mart reconciliation

### 🟡 Medium Priority Cases  
- **PR Review Critical** - Analysis of ready-to-merge PRs
- **FuelCloud Duplicates** - Consolidated deduplication issues
- **Business Logic Validation** - Freight/safety/ticket validation

### 🟢 Low Priority Cases
- **Minor Incidents** - Routine null values and small duplications

## Detective Types

Each case is assigned a detective type that determines sub-agent deployment:

- **data-forensics** - Uses snowflake-expert, dbt-expert, business-context
- **pr-analysis** - Uses dbt-expert, business-context, github-expert  
- **pipeline-investigation** - Uses orchestra-expert, dbt-expert, snowflake-expert

## Commands Reference

### Bureau Operations
```bash
# Dispatch all cases from analysis
./sherlock/bureau/dispatch-cases.sh

# Deploy detective squad (opens multiple terminals)
./sherlock/bureau/deploy-detectives.sh

# Preview deployment without launching
./sherlock/bureau/deploy-detectives.sh --dry-run
```

### Investigation Monitoring
```bash
# Quick status overview
./sherlock/bureau/check-investigations.sh

# Detailed case information  
./sherlock/bureau/check-investigations.sh --detailed

# Continuous monitoring (refreshes every 30s)
./sherlock/bureau/check-investigations.sh --watch
```

### Evidence Compilation
```bash
# Compile all evidence reports
./sherlock/bureau/compile-evidence.sh

# Compile specific report types
./sherlock/bureau/compile-evidence.sh --summary-only
./sherlock/bureau/compile-evidence.sh --pr-only
./sherlock/bureau/compile-evidence.sh --actions-only
```

## Evidence Reports Generated

1. **Investigation Summary** (`sherlock/evidence/investigation-summary.md`)
   - Comprehensive overview of all investigations
   - Case status, priorities, and findings
   - Bureau statistics and progress metrics

2. **PR Readiness Report** (`workspace/pr-readiness-report.md`)  
   - Cases ready for immediate implementation
   - Deployment priority recommendations
   - Integration with existing PR analysis

3. **Next Actions List** (`workspace/next-actions.md`)
   - Prioritized action items by HIGH/MEDIUM/LOW
   - Specific implementation steps
   - Blocked cases and dependencies

## Integration with Existing Workflow

The Sherlock system integrates with your existing da-agent-hub architecture:

- **Leverages sub-agents** as "expert contacts" for specialized analysis
- **Uses .claude/tasks/** pattern for coordination between instances  
- **Builds on dbt-cloud-pr-issue-analysis.md** as the central evidence source
- **Generates reports in workspace/** for easy access and sharing

## Troubleshooting

### Cases Not Deploying
- Ensure analysis file exists: `workspace/dbt-cloud-pr-issue-analysis.md`
- Run dispatch first: `./sherlock/bureau/dispatch-cases.sh`

### Terminal Launch Issues
- macOS: Requires Terminal.app (automatically detected)
- Linux: Requires gnome-terminal or xterm
- Fallback: Manual deployment instructions provided

### Missing Evidence
- Detectives must create evidence-report.md in their case directory
- Use monitoring to check investigation progress
- Evidence compilation requires completed investigations

---

*"The game is afoot!" - Sherlock Holmes*

🔍 **Investigation Bureau Status:** Ready for deployment  
📋 **Case Management:** Fully automated  
🕵️ **Detective Coordination:** Multi-instance parallel processing  
📊 **Evidence Compilation:** Comprehensive reporting system