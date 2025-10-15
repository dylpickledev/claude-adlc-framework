#!/usr/bin/env bash
#
# Memory Health Check Wrapper
#
# This script runs the memory health check using uvx with tiktoken dependency.
# uvx creates an ephemeral environment with all required packages automatically.
#
# Usage:
#   ./scripts/check-memory-health-uvx.sh                 # Standard check
#   ./scripts/check-memory-health-uvx.sh --history       # Show growth trend
#   ./scripts/check-memory-health-uvx.sh --detailed      # Detailed breakdown
#

set -e

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to repo root (scripts expect to be run from there)
cd "$REPO_ROOT"

# Run with uvx - automatically installs tiktoken in ephemeral environment
# Much simpler than managing venvs or global Python packages
uvx --with tiktoken python3 scripts/check-memory-health.py "$@"
