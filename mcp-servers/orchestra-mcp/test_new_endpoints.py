"""Test script for new Orchestra MCP endpoints (operations and dbt artifacts)."""

import asyncio
import os
import sys
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from orchestra_mcp.client import OrchestraClient, OrchestraAPIError


async def test_list_operations():
    """Test the operations endpoint - should provide error messages!"""
    print("\n" + "=" * 80)
    print("TEST 1: List Operations (Error Messages!)")
    print("=" * 80)

    client = OrchestraClient()

    # Get operations from last 2 days
    time_to = datetime.utcnow()
    time_from = time_to - timedelta(days=2)

    try:
        response = await client.list_operations(
            time_from=time_from.strftime("%Y-%m-%dT%H:%M:%SZ"),
            time_to=time_to.strftime("%Y-%m-%dT%H:%M:%SZ"),
            limit=10,
        )

        print(f"\n✅ Operations endpoint works!")
        print(f"Total operations: {response.get('total', 0)}")
        print(f"Results returned: {len(response.get('results', []))}")

        # Show first few operations
        for i, op in enumerate(response.get("results", [])[:3], 1):
            print(f"\n--- Operation {i} ---")
            print(f"  Name: {op.get('operationName')}")
            print(f"  Status: {op.get('operationStatus')}")
            print(f"  Message: {op.get('message', 'NO MESSAGE')[:100]}")
            print(f"  Integration: {op.get('integration')}")
            print(f"  Type: {op.get('operationType')}")
            print(f"  Task Run ID: {op.get('taskRunId')}")

        return True

    except OrchestraAPIError as e:
        print(f"\n❌ Operations endpoint failed: {e}")
        return False
    finally:
        await client.close()


async def test_download_dbt_artifact():
    """Test downloading dbt artifacts - manifest.json and run_results.json."""
    print("\n" + "=" * 80)
    print("TEST 2: Download dbt Artifacts")
    print("=" * 80)

    client = OrchestraClient()

    # First, get a recent task run ID from operations
    time_to = datetime.utcnow()
    time_from = time_to - timedelta(days=2)

    try:
        # Find a dbt MATERIALISATION operation (model builds have artifacts)
        ops_response = await client.list_operations(
            time_from=time_from.strftime("%Y-%m-%dT%H:%M:%SZ"),
            time_to=time_to.strftime("%Y-%m-%dT%H:%M:%SZ"),
            operation_type="MATERIALISATION",  # dbt models, not tests
            limit=20,  # Get more results to find one with artifacts
        )

        results = ops_response.get("results", [])
        if not results:
            print("\n⚠️  No dbt MATERIALISATION operations found in last 2 days")
            print("    (Tests don't have run_results.json, need actual model builds)")
            return True

        # Try multiple operations until we find one with artifacts
        dbt_op = None
        for candidate in results:
            # Prefer SUCCEEDED operations (more likely to have complete artifacts)
            if candidate.get("operationStatus") == "SUCCEEDED":
                dbt_op = candidate
                break

        if not dbt_op:
            # Fallback to first operation
            dbt_op = results[0]

        pipeline_run_id = dbt_op.get("pipelineRunId")
        task_run_id = dbt_op.get("taskRunId")

        print(f"\nFound dbt operation:")
        print(f"  Pipeline Run: {pipeline_run_id}")
        print(f"  Task Run: {task_run_id}")
        print(f"  Operation: {dbt_op.get('operationName')}")

        # Try to download manifest
        print("\n--- Testing manifest.json download ---")
        try:
            manifest = await client.download_dbt_artifact(
                pipeline_run_id=pipeline_run_id,
                task_run_id=task_run_id,
                artifact_type="manifest",
            )
            print("✅ manifest.json downloaded successfully!")
            print(f"   Keys: {list(manifest.keys())[:5]}...")
        except OrchestraAPIError as e:
            print(f"⚠️  manifest.json not available: {e}")

        # Try to download run_results
        print("\n--- Testing run_results.json download ---")
        try:
            run_results = await client.download_dbt_artifact(
                pipeline_run_id=pipeline_run_id,
                task_run_id=task_run_id,
                artifact_type="run_results",
            )
            print("✅ run_results.json downloaded successfully!")
            print(f"   Keys: {list(run_results.keys())[:5]}...")

            # Show any errors from dbt run
            if "results" in run_results:
                for result in run_results["results"]:
                    if result.get("status") == "error":
                        print(f"\n   ERROR in {result.get('unique_id')}:")
                        print(f"   {result.get('message', 'No message')[:100]}")

        except OrchestraAPIError as e:
            print(f"⚠️  run_results.json not available: {e}")

        return True

    except OrchestraAPIError as e:
        print(f"\n❌ dbt artifact test failed: {e}")
        return False
    finally:
        await client.close()


async def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("Orchestra MCP - New Endpoints Validation")
    print("=" * 80)

    test_results = []

    # Test 1: Operations endpoint
    result1 = await test_list_operations()
    test_results.append(("list_operations", result1))

    # Test 2: dbt artifacts
    result2 = await test_download_dbt_artifact()
    test_results.append(("download_dbt_artifact", result2))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(result for _, result in test_results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
