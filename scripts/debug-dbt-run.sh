#!/bin/bash
# dbt Cloud Run Debugger - Direct API Analysis (No MCP Required)
# Investigates failed/errored dbt Cloud runs using direct API calls
# Useful when MCP tools are unavailable or during troubleshooting

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Self-locate script and navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Source 1Password secrets (redirect output to avoid polluting stdout)
if [ -f "$HOME/dotfiles/load-secrets-from-1password.sh" ]; then
    source "$HOME/dotfiles/load-secrets-from-1password.sh" >/dev/null 2>&1 || true
fi

# Configuration (export for Python subprocesses)
export DBT_HOST="${DBT_HOST:-te240.us1.dbt.com}"  # Multi-tenant host (override if needed)
export DBT_ACCOUNT_ID="${DBT_CLOUD_ACCOUNT_ID:-2672}"
export TOKEN="${DBT_CLOUD_API_TOKEN}"

# Check prerequisites
if [ -z "$TOKEN" ]; then
    echo -e "${RED}ERROR: DBT_CLOUD_API_TOKEN not set${NC}"
    echo "Run: source ~/dotfiles/load-secrets-from-1password.sh"
    exit 1
fi

# Usage
usage() {
    cat << EOF
${CYAN}dbt Cloud Run Debugger${NC}

${YELLOW}USAGE:${NC}
    $0 <run_id> [options]

${YELLOW}OPTIONS:${NC}
    -h, --help              Show this help message
    -v, --verbose           Show full API responses
    -a, --artifacts         Download and show artifacts (logs, manifests)
    --host <host>           Override dbt Cloud host (default: $DBT_HOST)

${YELLOW}EXAMPLES:${NC}
    # Basic run investigation
    $0 436685529

    # Verbose output with artifacts
    $0 436685529 -v -a

    # Use different host
    $0 436685529 --host cloud.getdbt.com

${YELLOW}ENVIRONMENT:${NC}
    DBT_HOST:               ${DBT_HOST}
    DBT_ACCOUNT_ID:         ${DBT_ACCOUNT_ID}
    DBT_CLOUD_API_TOKEN:    ${TOKEN:+Set (${#TOKEN} chars)}

EOF
    exit 0
}

# Parse arguments
RUN_ID=""
VERBOSE=false
SHOW_ARTIFACTS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -a|--artifacts)
            SHOW_ARTIFACTS=true
            shift
            ;;
        --host)
            DBT_HOST="$2"
            shift 2
            ;;
        *)
            if [ -z "$RUN_ID" ]; then
                RUN_ID="$1"
            else
                echo -e "${RED}ERROR: Unknown argument: $1${NC}"
                usage
            fi
            shift
            ;;
    esac
done

# Validate run ID
if [ -z "$RUN_ID" ]; then
    echo -e "${RED}ERROR: Run ID required${NC}"
    usage
fi

# API helper function (uses Python to avoid curl Authorization header issues)
api_call() {
    local endpoint="$1"
    local description="$2"

    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}" >&2
    echo -e "${CYAN}${description}${NC}" >&2
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}" >&2

    # Use Python for reliable API calls (avoids bash curl token escaping issues)
    python3 << EOPY
import urllib.request
import urllib.error
import json
import os
import sys

token = os.environ.get('DBT_CLOUD_API_TOKEN', '') or os.environ.get('TOKEN', '')
host = os.environ.get('DBT_HOST', 'te240.us1.dbt.com')
endpoint = '${endpoint}'

url = f"https://{host}/api/v2/{endpoint}"
req = urllib.request.Request(url)
req.add_header('Authorization', f'Token {token}')
req.add_header('Content-Type', 'application/json')

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(json.dumps(data))
except urllib.error.HTTPError as e:
    error_data = {
        'status': {
            'code': e.code,
            'is_success': False,
            'user_message': f'HTTP {e.code}: {e.reason}',
            'developer_message': e.read().decode() if e.fp else None
        },
        'data': None
    }
    print(json.dumps(error_data))
    sys.exit(1)
except Exception as e:
    error_data = {
        'status': {
            'code': 500,
            'is_success': False,
            'user_message': f'Request failed: {str(e)}',
            'developer_message': None
        },
        'data': None
    }
    print(json.dumps(error_data))
    sys.exit(1)
EOPY

    local exit_code=$?
    return $exit_code
}

# Pretty print JSON with highlighting
pretty_json() {
    python3 << 'EOPY'
import sys
import json

data = json.load(sys.stdin)

def colorize(obj, indent=0):
    """Recursively print JSON with colors"""
    spaces = "  " * indent

    if isinstance(obj, dict):
        if not obj:
            print("{}")
            return
        print("{")
        for i, (key, value) in enumerate(obj.items()):
            comma = "," if i < len(obj) - 1 else ""
            print(f'{spaces}  \033[1;33m"{key}"\033[0m: ', end='')
            if isinstance(value, (dict, list)):
                colorize(value, indent + 1)
                print(comma)
            else:
                colorize(value, 0)
                print(comma)
        print(f"{spaces}}}")
    elif isinstance(obj, list):
        if not obj:
            print("[]")
            return
        print("[")
        for i, item in enumerate(obj):
            comma = "," if i < len(obj) - 1 else ""
            print(f"{spaces}  ", end='')
            colorize(item, indent + 1)
            print(comma)
        print(f"{spaces}]")
    elif isinstance(obj, str):
        # Color-code status values
        if obj in ["success", "Success"]:
            print(f'\033[0;32m"{obj}"\033[0m', end='')
        elif obj in ["error", "Error", "failed", "Failed"]:
            print(f'\033[0;31m"{obj}"\033[0m', end='')
        elif obj in ["running", "Running", "queued", "Queued"]:
            print(f'\033[1;33m"{obj}"\033[0m', end='')
        else:
            print(f'"{obj}"', end='')
    elif isinstance(obj, bool):
        print(f'\033[0;36m{str(obj).lower()}\033[0m', end='')
    elif obj is None:
        print('\033[0;90mnull\033[0m', end='')
    else:
        print(f'\033[0;35m{obj}\033[0m', end='')

colorize(data)
EOPY
}

# Main execution
main() {
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         dbt Cloud Run Debugger - Run $RUN_ID         ${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"

    # 1. Get run details
    echo -e "\n${YELLOW}[1/5] Fetching Run Details...${NC}"
    RUN_RESPONSE=$(api_call "accounts/${DBT_ACCOUNT_ID}/runs/${RUN_ID}/" "Run Overview")

    if [ "$VERBOSE" = true ]; then
        echo "$RUN_RESPONSE" | pretty_json
    else
        echo "$RUN_RESPONSE" | python3 << 'EOPY'
import sys
import json
data = json.load(sys.stdin)
run = data.get('data', {})

print(f"\n{'Job Name:':<20} {run.get('job', {}).get('name', 'N/A')}")
print(f"{'Job ID:':<20} {run.get('job_id', 'N/A')}")
print(f"{'Environment:':<20} {run.get('environment', {}).get('name', 'N/A')} (ID: {run.get('environment_id', 'N/A')})")
print(f"{'Status:':<20} {run.get('status_humanized', 'N/A')} ({run.get('status', 'N/A')})")
print(f"{'Trigger:':<20} {run.get('trigger', {}).get('cause', 'N/A')}")
print(f"{'Started:':<20} {run.get('created_at', 'N/A')}")
print(f"{'Finished:':<20} {run.get('finished_at', 'N/A')}")
print(f"{'Duration:':<20} {run.get('duration_humanized', 'N/A')}")
print(f"{'dbt Version:':<20} {run.get('dbt_version', 'N/A')}")
print(f"{'Git Branch:':<20} {run.get('git_branch', 'N/A')}")
print(f"{'Git SHA:':<20} {run.get('git_sha', 'N/A')[:8] if run.get('git_sha') else 'N/A'}")
EOPY
    fi

    # 2. Get run steps
    echo -e "\n${YELLOW}[2/5] Analyzing Run Steps...${NC}"
    STEPS=$(echo "$RUN_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(data.get('data', {}).get('run_steps', [])))")

    echo "$STEPS" | python3 << 'EOPY'
import sys
import json

steps = json.load(sys.stdin)
print(f"\n{'Step':<5} {'Name':<30} {'Status':<15} {'Duration':<12} {'Models':<8}")
print("─" * 80)

for i, step in enumerate(steps, 1):
    name = step.get('name', 'Unknown')[:29]
    status = step.get('status_humanized', 'Unknown')
    duration = step.get('duration_humanized', 'N/A')

    # Color code status
    if status == 'Success':
        status_color = '\033[0;32m'
    elif status in ['Error', 'Failed']:
        status_color = '\033[0;31m'
    elif status in ['Running', 'Queued']:
        status_color = '\033[1;33m'
    else:
        status_color = '\033[0m'

    # Count models
    num_models = len(step.get('run_step_models', []))
    models_str = f"{num_models} model{'s' if num_models != 1 else ''}" if num_models > 0 else '-'

    print(f"{i:<5} {name:<30} {status_color}{status:<15}\033[0m {duration:<12} {models_str:<8}")
EOPY

    # 3. Check for errors in steps
    echo -e "\n${YELLOW}[3/5] Checking for Errors...${NC}"
    ERRORS=$(echo "$STEPS" | python3 << 'EOPY'
import sys
import json

steps = json.load(sys.stdin)
errors = []

for step in steps:
    if step.get('status_humanized') in ['Error', 'Failed']:
        errors.append({
            'step': step.get('name'),
            'status': step.get('status_humanized'),
            'logs': step.get('logs', 'No logs available')
        })

    # Check individual models
    for model in step.get('run_step_models', []):
        if model.get('status') in ['error', 'failed']:
            errors.append({
                'step': step.get('name'),
                'model': model.get('name'),
                'status': model.get('status'),
                'error': model.get('error', 'No error message')
            })

print(json.dumps(errors, indent=2))
EOPY
)

    ERROR_COUNT=$(echo "$ERRORS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")

    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo -e "${RED}Found $ERROR_COUNT error(s):${NC}\n"
        echo "$ERRORS" | pretty_json
    else
        echo -e "${GREEN}✓ No errors detected${NC}"
    fi

    # 4. Get job information
    echo -e "\n${YELLOW}[4/5] Job Configuration...${NC}"
    JOB_ID=$(echo "$RUN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('data', {}).get('job_id', ''))")

    if [ -n "$JOB_ID" ]; then
        JOB_RESPONSE=$(api_call "accounts/${DBT_ACCOUNT_ID}/jobs/${JOB_ID}/" "Job Details")

        echo "$JOB_RESPONSE" | python3 << 'EOPY'
import sys
import json
data = json.load(sys.stdin)
job = data.get('data', {})

print(f"\n{'Execute Steps:':<20} {', '.join(job.get('execute_steps', []))}")
print(f"{'Generate Docs:':<20} {job.get('generate_docs', False)}")
print(f"{'Schedule:':<20} {job.get('schedule', {}).get('cron', 'Manual trigger only')}")
print(f"{'Threads:':<20} {job.get('settings', {}).get('threads', 'Default')}")
print(f"{'Target Name:':<20} {job.get('settings', {}).get('target_name', 'N/A')}")
EOPY
    fi

    # 5. Artifacts (if requested)
    if [ "$SHOW_ARTIFACTS" = true ]; then
        echo -e "\n${YELLOW}[5/5] Downloading Artifacts...${NC}"

        # List available artifacts
        ARTIFACTS_RESPONSE=$(api_call "accounts/${DBT_ACCOUNT_ID}/runs/${RUN_ID}/artifacts/" "Available Artifacts")

        echo "$ARTIFACTS_RESPONSE" | python3 << 'EOPY'
import sys
import json
data = json.load(sys.stdin)
artifacts = data.get('data', [])

if artifacts:
    print("\nAvailable artifacts:")
    for artifact in artifacts:
        print(f"  - {artifact}")
else:
    print("\nNo artifacts available for this run")
EOPY

        # Download run_results.json if available
        echo -e "\n${CYAN}Fetching run_results.json...${NC}"
        RUN_RESULTS=$(python3 << EOPY
import urllib.request
import json
import os

token = os.environ.get('DBT_CLOUD_API_TOKEN', '')
host = os.environ.get('DBT_HOST', 'te240.us1.dbt.com')
account_id = os.environ.get('DBT_ACCOUNT_ID', '2672')
run_id = '${RUN_ID}'

url = f"https://{host}/api/v2/accounts/{account_id}/runs/{run_id}/artifacts/run_results.json"
req = urllib.request.Request(url)
req.add_header('Authorization', f'Token {token}')

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except:
    print("{}")
EOPY
)

        if echo "$RUN_RESULTS" | python3 -c "import sys, json; json.load(sys.stdin); exit(0)" 2>/dev/null; then
            echo "$RUN_RESULTS" | python3 << 'EOPY'
import sys
import json

results = json.load(sys.stdin)
metadata = results.get('metadata', {})
elapsed_time = results.get('elapsed_time', 0)

print(f"\n{'Generated At:':<20} {metadata.get('generated_at', 'N/A')}")
print(f"{'Invocation ID:':<20} {metadata.get('invocation_id', 'N/A')}")
print(f"{'Elapsed Time:':<20} {elapsed_time:.2f}s")

# Summary of results
result_summary = {}
for result in results.get('results', []):
    status = result.get('status', 'unknown')
    result_summary[status] = result_summary.get(status, 0) + 1

if result_summary:
    print("\nModel Results:")
    for status, count in sorted(result_summary.items()):
        status_color = '\033[0;32m' if status == 'success' else '\033[0;31m' if status in ['error', 'fail'] else '\033[0m'
        print(f"  {status_color}{status}:\033[0m {count}")
EOPY
        else
            echo -e "${RED}run_results.json not available or invalid${NC}"
        fi
    else
        echo -e "\n${YELLOW}[5/5] Skipping artifacts (use -a to download)${NC}"
    fi

    # Summary
    echo -e "\n${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    Investigation Complete                 ${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"

    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo -e "\n${RED}⚠ Run failed with $ERROR_COUNT error(s)${NC}"
        echo -e "${YELLOW}Review error details above for troubleshooting${NC}"
    else
        echo -e "\n${GREEN}✓ Run completed successfully${NC}"
    fi

    echo -e "\n${CYAN}Next steps:${NC}"
    echo "  - View full details: https://${DBT_HOST}/#/accounts/${DBT_ACCOUNT_ID}/runs/${RUN_ID}/"
    if [ "$SHOW_ARTIFACTS" = false ]; then
        echo "  - Download artifacts: $0 $RUN_ID -a"
    fi
    if [ "$VERBOSE" = false ]; then
        echo "  - Verbose output: $0 $RUN_ID -v"
    fi
}

# Run main function
main
