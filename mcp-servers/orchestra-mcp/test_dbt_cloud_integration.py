"""Test Orchestra → dbt Cloud artifact integration."""
import asyncio
import sys
import json
from datetime import datetime, timedelta
sys.path.insert(0, "src")
from orchestra_mcp.client import OrchestraClient, DBTCloudClient, OrchestraAPIError

async def main():
    print("\n" + "=" * 80)
    print("Orchestra → dbt Cloud Artifact Integration Test")
    print("=" * 80)
    
    orchestra_client = OrchestraClient()
    
    try:
        # Step 1: Find a recent dbt task run
        print("\n[Step 1] Finding recent dbt Cloud task run...")
        time_to = datetime.utcnow()
        time_from = time_to - timedelta(days=1)
        
        tasks = await orchestra_client.list_task_runs(
            time_from=time_from.strftime("%Y-%m-%dT%H:%M:%SZ"),
            time_to=time_to.strftime("%Y-%m-%dT%H:%M:%SZ"),
            integration="DBT",
            limit=5
        )
        
        if not tasks.get("results"):
            print("❌ No dbt tasks found in last 24 hours")
            return 1
        
        # Find a task with run_id
        task_run = None
        for candidate in tasks["results"]:
            if candidate.get("runParameters", {}).get("run_id"):
                task_run = candidate
                break
        
        if not task_run:
            print("❌ No dbt tasks with run_id found")
            return 1
        
        task_run_id = task_run["id"]
        dbt_run_id = task_run["runParameters"]["run_id"]
        
        print(f"✅ Found dbt task run:")
        print(f"   Orchestra task_run_id: {task_run_id}")
        print(f"   dbt Cloud run_id: {dbt_run_id}")
        print(f"   Task: {task_run.get('taskName')}")
        print(f"   Status: {task_run.get('status')}")
        
        # Step 2: Get dbt Cloud run_id extraction
        print("\n[Step 2] Testing dbt Cloud run_id extraction...")
        extracted_run_id = await orchestra_client.get_dbt_cloud_run_id(task_run_id)
        
        if extracted_run_id == dbt_run_id:
            print(f"✅ Run ID extraction works: {extracted_run_id}")
        else:
            print(f"❌ Run ID mismatch: {extracted_run_id} != {dbt_run_id}")
            return 1
        
        # Step 3: Fetch artifacts via dbt Cloud API
        print("\n[Step 3] Fetching artifacts from dbt Cloud API...")
        artifacts = await orchestra_client.get_dbt_artifacts_via_cloud(task_run_id)
        
        print(f"✅ Successfully fetched artifacts!")
        print(f"   dbt Cloud run_id: {artifacts.get('run_id')}")
        
        # Check which artifacts we got
        artifact_types = ["manifest", "run_results", "catalog"]
        for artifact_type in artifact_types:
            if artifact_type in artifacts:
                artifact = artifacts[artifact_type]
                keys = list(artifact.keys()) if isinstance(artifact, dict) else []
                print(f"   ✅ {artifact_type}.json - {len(keys)} top-level keys")
            else:
                print(f"   ⚠️  {artifact_type}.json - not available")
        
        # Step 4: Validate run_results if available
        if "run_results" in artifacts:
            print("\n[Step 4] Validating run_results.json...")
            run_results = artifacts["run_results"]
            
            if "results" in run_results:
                total_results = len(run_results["results"])
                error_count = sum(1 for r in run_results["results"] if r.get("status") == "error")
                success_count = sum(1 for r in run_results["results"] if r.get("status") == "success")
                
                print(f"   Total results: {total_results}")
                print(f"   Successful: {success_count}")
                print(f"   Errors: {error_count}")
                
                # Show first error if any
                if error_count > 0:
                    for result in run_results["results"]:
                        if result.get("status") == "error":
                            print(f"\n   Example error:")
                            print(f"   Model: {result.get('unique_id')}")
                            print(f"   Message: {result.get('message', 'No message')[:200]}")
                            break
            else:
                print("   ⚠️  run_results.json missing 'results' key")
        
        # Step 5: Validate manifest if available
        if "manifest" in artifacts:
            print("\n[Step 5] Validating manifest.json...")
            manifest = artifacts["manifest"]
            
            nodes = manifest.get("nodes", {})
            sources = manifest.get("sources", {})
            macros = manifest.get("macros", {})
            
            print(f"   Models/Tests: {len(nodes)}")
            print(f"   Sources: {len(sources)}")
            print(f"   Macros: {len(macros)}")
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED - Orchestra → dbt Cloud integration working!")
        print("=" * 80)
        
        return 0
        
    except OrchestraAPIError as e:
        print(f"\n❌ Orchestra API error: {e}")
        return 1
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
        print("   Make sure DBT_CLOUD_API_TOKEN and DBT_CLOUD_ACCOUNT_ID are set")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await orchestra_client.close()

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
