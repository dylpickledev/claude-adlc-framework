#!/usr/bin/env python3
"""Find specific Orchestra pipeline run by ID or name.

This script works around FastMCP parameter exposure limitations by:
1. Querying the Orchestra API directly with full parameter support
2. Client-side filtering for specific runs

Usage:
    python3 find_run.py --run-id <run_id>
    python3 find_run.py --pipeline-name "Sales Journal"
    python3 find_run.py --status FAILED --limit 10
"""

import asyncio
import sys
import os
import json
import argparse
from pathlib import Path

# Add src to path so we can import orchestra_mcp
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from orchestra_mcp.client import OrchestraClient, OrchestraAPIError


async def find_run(
    run_id: str = None,
    pipeline_name: str = None,
    status: str = None,
    time_from: str = None,
    time_to: str = None,
    limit: int = 100,
):
    """Find pipeline runs matching criteria.

    Args:
        run_id: Specific pipeline run ID to find
        pipeline_name: Pipeline name to search for (partial match)
        status: Filter by run status (FAILED, SUCCEEDED, etc.)
        time_from: ISO 8601 start time
        time_to: ISO 8601 end time
        limit: Max results to return
    """
    client = OrchestraClient()

    try:
        # Call API with full parameter support (not limited by FastMCP)
        results = await client.list_pipeline_runs(
            status=status,
            time_from=time_from,
            time_to=time_to,
            limit=limit,
        )

        # Client-side filtering
        runs = results.get("results", [])

        # Filter by run ID if specified
        if run_id:
            runs = [r for r in runs if r.get("id") == run_id]

        # Filter by pipeline name if specified (case-insensitive partial match)
        if pipeline_name:
            pipeline_name_lower = pipeline_name.lower()
            runs = [
                r for r in runs
                if pipeline_name_lower in r.get("pipelineName", "").lower()
            ]

        # Output results
        print(json.dumps({
            "total_fetched": len(results.get("results", [])),
            "matched": len(runs),
            "runs": runs
        }, indent=2))

        return runs

    except OrchestraAPIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.close()


def main():
    parser = argparse.ArgumentParser(
        description="Find Orchestra pipeline runs with flexible filtering"
    )
    parser.add_argument("--run-id", help="Specific pipeline run ID")
    parser.add_argument("--pipeline-name", help="Pipeline name (partial match)")
    parser.add_argument("--status", help="Run status (FAILED, SUCCEEDED, etc.)")
    parser.add_argument("--time-from", help="Start time (ISO 8601)")
    parser.add_argument("--time-to", help="End time (ISO 8601)")
    parser.add_argument("--limit", type=int, default=100, help="Max results")

    args = parser.parse_args()

    if not any([args.run_id, args.pipeline_name, args.status]):
        parser.error("Must specify at least one filter: --run-id, --pipeline-name, or --status")

    asyncio.run(find_run(
        run_id=args.run_id,
        pipeline_name=args.pipeline_name,
        status=args.status,
        time_from=args.time_from,
        time_to=args.time_to,
        limit=args.limit,
    ))


if __name__ == "__main__":
    main()
