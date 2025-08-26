#!/usr/bin/env python3

"""
🔍 Sherlock Holmes Investigation Bureau - GitHub Issue Dispatcher

This Claude command fetches open GitHub issues from graniterock/dbt_cloud
and creates investigation cases for the Sherlock system.

Usage:
    python scripts/sherlock-dispatch-issues.py [--sync] [--limit N]
    
Integration:
    - Uses GitHub MCP to fetch issues
    - Creates Sherlock case files and registry
    - Prioritizes cases based on issue content
    - Tracks case status and GitHub sync
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import re

# Add the parent directory to Python path for MCP access
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_paths():
    """Set up all required paths for the Sherlock system."""
    base_dir = Path(__file__).parent.parent
    sherlock_dir = base_dir / "sherlock"
    
    paths = {
        'base_dir': base_dir,
        'sherlock_dir': sherlock_dir,
        'cases_dir': sherlock_dir / "cases",
        'evidence_dir': sherlock_dir / "evidence", 
        'templates_dir': sherlock_dir / "templates",
        'case_registry': sherlock_dir / "case-registry.json",
        'workspace_dir': base_dir / "workspace"
    }
    
    # Ensure directories exist
    for dir_path in [paths['cases_dir'], paths['evidence_dir'], paths['templates_dir'], paths['workspace_dir']]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return paths

def print_header():
    """Print the Victorian detective header."""
    print("\n🔍 SHERLOCK HOLMES INVESTIGATION BUREAU 🔍")
    print("═══════════════════════════════════════════")
    print("    GitHub Issue Investigation Dispatcher")
    print("═══════════════════════════════════════════\n")

def determine_case_priority(issue):
    """Determine case priority based on issue content."""
    title = issue.get('title', '').lower()
    body = issue.get('body', '').lower()
    labels = [label.get('name', '').lower() for label in issue.get('labels', [])]
    
    # High priority indicators
    high_indicators = [
        'critical', 'urgent', 'blocking', 'high priority',
        'duplicate.*million', '5.*million', 'massive.*duplication'
    ]
    
    for indicator in high_indicators:
        if any(re.search(indicator, text) for text in [title, body] + labels):
            return "HIGH"
    
    # Check for large numbers indicating major issues
    if re.search(r'\d{4,}.*results.*configured to fail', body):
        return "HIGH"
    
    # Medium priority indicators  
    medium_indicators = [
        'bug', 'enhancement', 'medium priority', 'validation.*fail',
        'reconciliation', 'business.*logic', 'test.*fail'
    ]
    
    for indicator in medium_indicators:
        if any(re.search(indicator, text) for text in [title, body] + labels):
            return "MEDIUM"
    
    return "LOW"

def determine_detective_type(issue):
    """Determine which type of detective to assign."""
    title = issue.get('title', '').lower()
    body = issue.get('body', '').lower()
    labels = [label.get('name', '').lower() for label in issue.get('labels', [])]
    
    # PR analysis type
    pr_indicators = ['ready.*merge', 'pr.*review', 'code.*review']
    for indicator in pr_indicators:
        if any(re.search(indicator, text) for text in [title, body] + labels):
            return "pr-analysis"
    
    # Pipeline investigation type
    pipeline_indicators = [
        'pipeline', 'orchestration', 'workflow', 'validation.*fail',
        'business.*logic', 'orchestra'
    ]
    for indicator in pipeline_indicators:
        if any(re.search(indicator, text) for text in [title, body] + labels):
            return "pipeline-investigation"
    
    # Default to data forensics for test failures, duplicates, etc.
    return "data-forensics"

def generate_case_name(issue):
    """Generate a case name from the issue."""
    title = issue.get('title', '')
    number = issue.get('number', 0)
    
    # Clean title for case name
    case_name = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    case_name = case_name.lower().replace(' ', '-')
    case_name = re.sub(r'-+', '-', case_name)
    case_name = case_name.strip('-')
    
    # Limit length and add issue number
    case_name = case_name[:50]
    return f"issue-{number}-{case_name}"

def get_investigation_objective(issue):
    """Generate investigation objective based on issue content."""
    title = issue.get('title', '').lower()
    body = issue.get('body', '').lower()
    
    if re.search(r'duplicate.*record|duplication', title + ' ' + body):
        return "Identify and resolve data duplication issues, implement deduplication strategy"
    elif re.search(r'validation.*fail|test.*fail', title + ' ' + body):
        return "Investigate validation failures, fix test configurations and business logic"  
    elif re.search(r'reconciliation|mismatch', title + ' ' + body):
        return "Resolve data reconciliation issues and fix cross-system data consistency"
    elif re.search(r'performance|slow|timeout', title + ' ' + body):
        return "Investigate performance issues and implement optimization solutions"
    elif re.search(r'null.*value|missing.*data', title + ' ' + body):
        return "Resolve null value issues and implement proper data handling"
    else:
        return "Conduct thorough investigation of GitHub issue and provide actionable technical solution"

def get_expert_contacts(detective_type):
    """Get expert contacts based on detective type."""
    contacts = {
        "data-forensics": [
            "**Snowflake Expert** (snowflake-expert): Database forensics and query analysis",
            "**dbt Expert** (dbt-expert): Model logic and transformation analysis", 
            "**Business Context Agent** (business-context): Domain knowledge and requirements"
        ],
        "pr-analysis": [
            "**dbt Expert** (dbt-expert): Code review and model analysis",
            "**Business Context Agent** (business-context): Business impact assessment"
        ],
        "pipeline-investigation": [
            "**Orchestra Expert** (orchestra-expert): Pipeline orchestration analysis",
            "**dbt Expert** (dbt-expert): Transformation logic review",
            "**Snowflake Expert** (snowflake-expert): Data warehouse impact analysis"
        ]
    }
    
    return contacts.get(detective_type, contacts["data-forensics"])

def create_case_files(issue, case_name, priority, detective_type, paths):
    """Create all case files for a GitHub issue."""
    case_dir = paths['cases_dir'] / case_name
    case_dir.mkdir(exist_ok=True)
    
    issue_number = issue.get('number')
    issue_title = issue.get('title', 'No title')
    issue_body = issue.get('body', 'No description provided')
    issue_url = f"https://github.com/graniterock/dbt_cloud/issues/{issue_number}"
    labels = ', '.join([label.get('name', '') for label in issue.get('labels', [])])
    created_at = issue.get('created_at', '')
    updated_at = issue.get('updated_at', '')
    
    # Case Brief
    case_brief = f"""# {case_name.upper().replace('-', ' ')} 🔍

**Case Classification:** {priority} PRIORITY
**Case Number:** {datetime.now().strftime('%Y%m%d-%H%M%S')}
**GitHub Issue:** #{issue_number}
**Detective Type Required:** {detective_type}
**Issue URL:** {issue_url}
**Created:** {created_at}
**Last Updated:** {updated_at}
**Labels:** {labels}

## Case Description
**Issue Title:** {issue_title}

{issue_body}

## GitHub Integration
- **Repository:** graniterock/dbt_cloud
- **Issue Number:** #{issue_number}
- **Direct Link:** {issue_url}
- **Status Tracking:** Case will be marked resolved when GitHub issue is closed

## Investigation Objective
{get_investigation_objective(issue)}

## Expected Evidence
- [ ] Root cause analysis with GitHub issue context
- [ ] Technical findings documentation
- [ ] Recommended action plan
- [ ] GitHub issue updates with progress
- [ ] Cross-case dependencies noted

## Case Resolution Criteria
- [ ] GitHub issue addressed
- [ ] Solution implemented and tested
- [ ] Issue closed in GitHub
- [ ] Evidence compiled for bureau records

---
*"The game is afoot!" - S.H.*
"""
    
    # Detective Instructions
    expert_contacts = '\n'.join([f"- {contact}" for contact in get_expert_contacts(detective_type)])
    
    detective_instructions = f"""# 🕵️ DETECTIVE CLAUDE ASSIGNMENT

## Your Mission Briefing
You are Detective Claude, assigned to investigate **GitHub Issue #{issue_number}**.

### GitHub Issue Details
- **Title:** {issue_title}
- **Repository:** graniterock/dbt_cloud
- **Issue URL:** {issue_url}
- **Priority Level:** {priority}
- **Labels:** {labels}

### Case Context
**Read your case brief:** ./case-brief.md

**GitHub Issue Description:**
{issue_body}

### Expert Contacts (Sub-Agents) Available
{expert_contacts}

### Investigation Protocol
1. **GitHub Analysis**: Review the issue details, comments, and related PRs
2. **Technical Investigation**: Use sub-agents to analyze the problem
3. **Cross-Reference**: Check for related issues or existing solutions
4. **Solution Development**: Create actionable recommendations
5. **GitHub Updates**: Update the GitHub issue with findings
6. **Evidence Documentation**: Record everything in evidence-report.md

### GitHub Integration Commands
```bash
# View full issue details
gh issue view {issue_number} --repo graniterock/dbt_cloud

# Add comments to the issue  
gh issue comment {issue_number} --repo graniterock/dbt_cloud --body "Investigation update..."

# Check related PRs
gh pr list --repo graniterock/dbt_cloud --search "fixes #{issue_number} OR closes #{issue_number}"

# View issue timeline
gh issue view {issue_number} --repo graniterock/dbt_cloud --comments
```

### MCP Integration Commands
```python
# Get issue details with comments
mcp__github__get_issue(owner="graniterock", repo="dbt_cloud", issue_number={issue_number})

# Add comment to issue
mcp__github__add_issue_comment(owner="graniterock", repo="dbt_cloud", issue_number={issue_number}, body="Investigation findings...")

# Get related PRs
mcp__github__search_pull_requests(query="repo:graniterock/dbt_cloud #{issue_number}")
```

### Evidence Documentation
Document all findings in: `./evidence-report.md`

Include:
- GitHub issue analysis
- Technical investigation results
- Recommended solution
- Implementation plan
- GitHub issue updates made

### Success Criteria
- [ ] Issue root cause identified
- [ ] Solution developed and documented
- [ ] GitHub issue updated with progress
- [ ] Ready for implementation or closure

---
*"You see, but you do not observe. Now observe the GitHub issue!" - S.H.*
"""
    
    # Evidence Report Template
    evidence_report = f"""# 📄 EVIDENCE REPORT: {case_name.upper().replace('-', ' ')}

**Detective:** Claude
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Case Priority:** {priority}
**GitHub Issue:** #{issue_number}
**Repository:** graniterock/dbt_cloud
**Issue URL:** {issue_url}

## GitHub Issue Analysis

### Original Issue Details
**Title:** {issue_title}
**Created:** {created_at}
**Last Updated:** {updated_at}
**Labels:** {labels}

**Description:**
{issue_body}

### Issue Comments and Updates
*[Document key comments and updates from GitHub]*

### Related PRs and References
*[List any related pull requests or referenced issues]*

## Investigation Summary
*[Provide overview of investigation conducted]*

## Technical Evidence Gathered
*[Detail technical findings from sub-agent analysis]*

## Root Cause Analysis
*[Identify underlying causes with GitHub context]*

## Solution Recommendations
*[Provide specific, actionable recommendations]*

### Implementation Plan
*[Step-by-step plan for resolving the GitHub issue]*

### Testing Strategy
*[How to validate the solution works]*

## GitHub Issue Updates
*[Record any comments or updates made to the GitHub issue]*

## Cross-Case Dependencies
*[Note any connections to other GitHub issues or investigations]*

## Case Resolution Status
- [ ] Investigation Complete
- [ ] Solution Ready for Implementation
- [ ] GitHub Issue Updated with Findings
- [ ] Ready for Issue Closure
- [ ] Requires Additional Investigation
- [ ] Blocked by Dependencies

## Next Actions
*[Specific next steps, including GitHub issue actions]*

---
**Detective Signature:** Claude
**Bureau File:** {case_dir}
**GitHub Integration:** Active
"""
    
    # Write files
    (case_dir / "case-brief.md").write_text(case_brief)
    (case_dir / "detective-instructions.md").write_text(detective_instructions)
    (case_dir / "evidence-report.md").write_text(evidence_report)
    
    return case_dir

def load_case_registry(paths):
    """Load existing case registry or create new one."""
    registry_path = paths['case_registry']
    
    if registry_path.exists():
        with open(registry_path, 'r') as f:
            return json.load(f)
    
    return {
        "cases": {},
        "last_sync": None,
        "github_repo": "graniterock/dbt_cloud"
    }

def save_case_registry(registry, paths):
    """Save case registry to file."""
    with open(paths['case_registry'], 'w') as f:
        json.dump(registry, f, indent=2)

def update_case_registry(registry, case_name, issue, priority, detective_type):
    """Update case registry with new case."""
    registry["cases"][case_name] = {
        "issue_number": issue.get('number'),
        "issue_title": issue.get('title', ''),
        "issue_url": f"https://github.com/graniterock/dbt_cloud/issues/{issue.get('number')}",
        "priority": priority,
        "detective_type": detective_type,
        "github_created_at": issue.get('created_at', ''),
        "github_updated_at": issue.get('updated_at', ''),
        "last_synced": datetime.now().isoformat(),
        "status": "active",
        "github_state": issue.get('state', 'OPEN')
    }
    registry["last_sync"] = datetime.now().isoformat()

def create_coordination_hub(registry, paths):
    """Create the coordination hub file."""
    cases = registry.get("cases", {})
    total_cases = len(cases)
    
    priority_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for case in cases.values():
        priority = case.get("priority", "LOW")
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    coordination_content = f"""# 🔍 SHERLOCK HOLMES INVESTIGATION BUREAU - COORDINATION HUB

**Bureau Chief:** Inspector Dylan
**Investigation Start Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**GitHub Repository:** graniterock/dbt_cloud
**Total Active Cases:** {total_cases}

## Case Priority Distribution
- 🔴 **High Priority:** {priority_counts['HIGH']} cases
- 🟡 **Medium Priority:** {priority_counts['MEDIUM']} cases
- 🟢 **Low Priority:** {priority_counts['LOW']} cases

## GitHub Integration Status
- **Repository:** graniterock/dbt_cloud
- **Last Sync:** {registry.get('last_sync', 'Never')}
- **Case Registry:** {paths['case_registry']}
- **Auto-sync:** Cases track GitHub issue status changes

## Bureau Commands

### Case Management
```bash
# Refresh cases from GitHub
python scripts/sherlock-dispatch-issues.py --sync

# List all tracked cases  
python scripts/sherlock-dispatch-issues.py --list

# Deploy detective squad
./sherlock/bureau/deploy-detectives.sh

# Monitor investigations
./sherlock/bureau/check-investigations.sh

# Compile evidence
./sherlock/bureau/compile-evidence.sh
```

### GitHub Integration (MCP)
```python
# List open issues
mcp__github__list_issues(owner="graniterock", repo="dbt_cloud", state="OPEN")

# Get specific issue details
mcp__github__get_issue(owner="graniterock", repo="dbt_cloud", issue_number=<number>)

# Add investigation comment
mcp__github__add_issue_comment(owner="graniterock", repo="dbt_cloud", issue_number=<number>, body="Investigation progress...")
```

## Active Cases Summary

| Issue # | Priority | Title | Status |
|---------|----------|--------|--------|"""

    for case_name, case_data in cases.items():
        priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(case_data.get("priority", "LOW"), "⚪")
        coordination_content += f"""
| #{case_data.get('issue_number', 'N/A')} | {priority_emoji} {case_data.get('priority', 'LOW')} | {case_data.get('issue_title', 'No title')[:60]}... | 📋 Active |"""

    coordination_content += f"""

## Investigation Notes
*Bureau coordination notes will be updated here as cases progress*

## Cross-Case Dependencies
*Dependencies between GitHub issues and investigation cases will be noted here*

---
**Next Action:** Deploy detective squad via `./sherlock/bureau/deploy-detectives.sh`

*"When you eliminate the impossible, whatever remains, however improbable, must be the truth." - S.H.*
"""
    
    (paths['cases_dir'] / "case-coordination.md").write_text(coordination_content)

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Sherlock GitHub Issue Dispatcher")
    parser.add_argument('--sync', action='store_true', help='Sync with existing cases')
    parser.add_argument('--limit', type=int, default=50, help='Limit number of issues to process')
    parser.add_argument('--list', action='store_true', help='List current cases')
    parser.add_argument('--status', action='store_true', help='Show case status summary')
    
    args = parser.parse_args()
    
    paths = setup_paths()
    print_header()
    
    if args.list:
        registry = load_case_registry(paths)
        cases = registry.get("cases", {})
        
        if not cases:
            print("📋 No cases found. Run without --list to dispatch new cases.\n")
            return
        
        print(f"📋 Case Registry Status")
        print(f"Last GitHub Sync: {registry.get('last_sync', 'Never')}\n")
        
        for case_name, case_data in cases.items():
            priority_color = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(case_data.get("priority"), "⚪")
            print(f"{priority_color} #{case_data.get('issue_number')} - {case_data.get('priority')} - {case_data.get('issue_title')}")
        
        print(f"\n📊 Total Cases: {len(cases)}")
        return
    
    if args.status:
        registry = load_case_registry(paths)
        cases = registry.get("cases", {})
        
        active_cases = sum(1 for case in cases.values() if case.get('status') == 'active')
        resolved_cases = sum(1 for case in cases.values() if case.get('status') == 'resolved')
        
        print(f"📊 Case Registry Status")
        print(f"Total Cases: {len(cases)}")
        print(f"Active Cases: {active_cases}")
        print(f"Resolved Cases: {resolved_cases}")
        print(f"Last Sync: {registry.get('last_sync', 'Never')}")
        return
    
    # This would normally import and use MCP functionality
    # For now, we'll use a placeholder that shows the structure
    print("🔗 Connecting to GitHub MCP...")
    print("📡 Fetching open issues from graniterock/dbt_cloud...")
    
    # Placeholder for MCP integration - you would call the MCP functions here
    print("⚠️  MCP integration placeholder - implement with actual MCP calls")
    print("💡 Use: mcp__github__list_issues(owner='graniterock', repo='dbt_cloud')")
    
    # For demonstration, create a sample structure
    registry = load_case_registry(paths)
    
    if not registry.get("cases"):
        print("\n📝 No existing cases found.")
        print("🎯 Ready for MCP integration to fetch GitHub issues and create cases.")
        print("\n🚀 Next steps:")
        print("   1. Integrate MCP GitHub calls in this script")
        print("   2. Run this script to populate cases from live GitHub issues")  
        print("   3. Deploy detectives: ./sherlock/bureau/deploy-detectives.sh")
    else:
        print(f"📋 Found {len(registry['cases'])} existing cases")
        
    create_coordination_hub(registry, paths)
    save_case_registry(registry, paths)
    
    print("\n✅ Sherlock dispatch system ready!")
    print(f"📂 Cases directory: {paths['cases_dir']}")
    print(f"📋 Registry file: {paths['case_registry']}")

if __name__ == "__main__":
    main()