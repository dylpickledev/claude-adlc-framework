"""Orchestra MCP Server - FastMCP implementation for Orchestra platform."""

import sys
from typing import Any, Optional
from fastmcp import FastMCP
from .client import OrchestraClient, OrchestraAPIError

# Initialize FastMCP server
mcp = FastMCP("orchestra-mcp")

# Global client instance (initialized on startup)
_client: Optional[OrchestraClient] = None


def get_client() -> OrchestraClient:
    """Get or create Orchestra API client instance."""
    global _client
    if _client is None:
        _client = OrchestraClient()
    return _client


@mcp.tool()
async def list_pipeline_runs(
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    status: Optional[str] = None,
    pipeline_run_ids: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """List pipeline runs with optional time filtering.

    Query Orchestra pipeline runs with time-based filtering and pagination.
    Without date filters, only last 7 days of data is available.

    Args:
        time_from: Start time filter in ISO 8601 format (e.g., '2025-04-01T00:00:00Z')
        time_to: End time filter in ISO 8601 format
        status: Filter by status (CREATED, RUNNING, SUCCEEDED, WARNING, FAILED, CANCELLING, CANCELLED)
        pipeline_run_ids: Comma-separated list of pipeline run IDs
        limit: Maximum number of results to return (default: 100, max: 1000)
        offset: Pagination offset for result sets (default: 0)

    Returns:
        Paginated response containing:
        {
            "page": 1,
            "pageSize": 50,
            "total": 2367,
            "results": [list of pipeline run dictionaries]
        }

    Example:
        # Get last 50 runs
        list_pipeline_runs(limit=50)

        # Get runs from specific date range
        list_pipeline_runs(
            time_from="2025-04-01T00:00:00Z",
            time_to="2025-04-30T23:59:59Z"
        )

        # Get specific pipeline run by ID
        list_pipeline_runs(pipeline_run_ids="8e808ad7-1234-5678-abcd-ef1234567890")
    """
    client = get_client()
    try:
        return await client.list_pipeline_runs(
            time_from=time_from,
            time_to=time_to,
            status=status,
            pipeline_run_ids=pipeline_run_ids,
            limit=limit,
            offset=offset,
        )
    except OrchestraAPIError as e:
        return {"error": str(e)}


@mcp.tool()
async def get_pipeline_run_status(pipeline_run_id: str) -> dict[str, Any]:
    """Get status for a specific pipeline run.

    Retrieve the current status of a pipeline run including execution state,
    timing information, and duration.

    Args:
        pipeline_run_id: Unique identifier for the pipeline run

    Returns:
        Pipeline run status dictionary with current state and timing data

    Example:
        get_pipeline_run_status(pipeline_run_id="8e808ad7-1234-5678-abcd-ef1234567890")
    """
    client = get_client()
    try:
        return await client.get_pipeline_run_status(pipeline_run_id)
    except OrchestraAPIError as e:
        return {"error": str(e)}


@mcp.tool()
async def get_pipeline_run_details(pipeline_run_id: str) -> dict[str, Any]:
    """Get comprehensive details for a specific pipeline run.

    Retrieve complete information about a pipeline run including configuration,
    execution results, metadata, and full run context.

    Args:
        pipeline_run_id: Unique identifier for the pipeline run

    Returns:
        Complete pipeline run information including all metadata and results

    Example:
        get_pipeline_run_details(pipeline_run_id="8e808ad7-1234-5678-abcd-ef1234567890")
    """
    client = get_client()
    try:
        return await client.get_pipeline_run_details(pipeline_run_id)
    except OrchestraAPIError as e:
        return {"error": str(e)}


@mcp.tool()
async def list_task_runs(
    pipeline_run_id: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    status: Optional[str] = None,
    pipeline_ids: Optional[str] = None,
    integration: Optional[str] = None,
    task_run_ids: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """List all task runs within a pipeline run.

    Retrieve the list of individual task executions that are part of a
    pipeline run, including their status and timing information.

    Args:
        pipeline_run_id: Unique identifier for the pipeline run
        time_from: Start time filter in ISO 8601 format
        time_to: End time filter in ISO 8601 format
        status: Filter by status (CREATED, SKIPPED, QUEUED, RUNNING, SUCCEEDED, WARNING, FAILED, CANCELLING, CANCELLED)
        pipeline_ids: Comma-separated pipeline IDs
        integration: Comma-separated integration names
        task_run_ids: Comma-separated task run IDs
        limit: Maximum number of results (default: 100, max: 1000)
        offset: Pagination offset (default: 0)

    Returns:
        Paginated response containing:
        {
            "page": 1,
            "pageSize": 50,
            "total": 1234,
            "results": [list of task run dictionaries]
        }

    Example:
        list_task_runs(pipeline_run_id="8e808ad7-1234-5678-abcd-ef1234567890")
    """
    client = get_client()
    try:
        return await client.list_task_runs(
            pipeline_run_id=pipeline_run_id,
            time_from=time_from,
            time_to=time_to,
            status=status,
            pipeline_ids=pipeline_ids,
            integration=integration,
            task_run_ids=task_run_ids,
            limit=limit,
            offset=offset,
        )
    except OrchestraAPIError as e:
        return {"error": str(e)}


@mcp.tool()
async def get_task_run_artifacts(
    pipeline_run_id: str, task_run_id: str
) -> list[dict[str, Any]]:
    """List available artifacts for a specific task run.

    Retrieve metadata about artifacts (logs, outputs, data files) generated
    by a task run. Use this before downloading artifacts to see what's available.

    Args:
        pipeline_run_id: Unique identifier for the pipeline run
        task_run_id: Unique identifier for the task run

    Returns:
        List of artifact info dictionaries with filenames, sizes, and types

    Example:
        get_task_run_artifacts(
            pipeline_run_id="8e808ad7-1234-5678-abcd-ef1234567890",
            task_run_id="task-abc123"
        )
    """
    client = get_client()
    try:
        return await client.get_task_run_artifacts(pipeline_run_id, task_run_id)
    except OrchestraAPIError as e:
        return {"error": str(e)}


@mcp.tool()
async def download_task_artifact(
    pipeline_run_id: str, task_run_id: str, filename: str
) -> str:
    """Download a specific artifact from a task run.

    Retrieve the content of a specific artifact file generated by a task run.
    Use get_task_run_artifacts first to see available artifact filenames.

    Args:
        pipeline_run_id: Unique identifier for the pipeline run
        task_run_id: Unique identifier for the task run
        filename: Name of the artifact file to download

    Returns:
        Artifact content as string (text files, logs, JSON, etc.)

    Example:
        download_task_artifact(
            pipeline_run_id="8e808ad7-1234-5678-abcd-ef1234567890",
            task_run_id="task-abc123",
            filename="error.log"
        )
    """
    client = get_client()
    try:
        return await client.download_task_artifact(
            pipeline_run_id, task_run_id, filename
        )
    except OrchestraAPIError as e:
        return str(e)


@mcp.tool()
async def list_operations(
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    operation_type: Optional[str] = None,
    external_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """List operations (detailed task-level execution info) with filtering.

    Operations provide granular details about task executions, including:
    - Error messages (the "message" field contains actual error text)
    - Integration-specific metadata (e.g., dbt model results, SQL query details)
    - Execution metrics (duration, rows affected)
    - Operation-level status (operationStatus, externalStatus)

    This is THE KEY ENDPOINT for debugging pipeline failures - it provides the
    error messages that were missing from task_runs endpoint!

    Args:
        time_from: Start time filter in ISO 8601 format (e.g., '2025-10-15T00:00:00Z')
        time_to: End time filter in ISO 8601 format
        operation_type: Filter by operation type (QUERY, AGGREGATION, DEPLOY,
                       MATERIALISATION, TEST, SNAPSHOT, SOURCE, SEED, etc.)
        external_id: Filter by external identifier (e.g., dbt model name)
        limit: Maximum number of results to return (default: 100, max: 1000)
        offset: Pagination offset for result sets (default: 0)

    Returns:
        Paginated response containing:
        {
            "page": 1,
            "pageSize": 50,
            "total": 567,
            "results": [
                {
                    "id": "operation-uuid",
                    "pipelineRunId": "pipeline-run-uuid",
                    "taskRunId": "task-run-uuid",
                    "operationName": "model.my_project.my_model",
                    "operationStatus": "SUCCEEDED" | "FAILED",
                    "message": "Actual error message or success message",
                    "externalStatus": "SUCCESS" | "ERROR",
                    "externalDetail": "Additional integration details",
                    "integration": "DBT" | "SNOWFLAKE" | etc.,
                    "integrationJob": "DBT_RUN_MODEL",
                    "operationType": "MATERIALISATION",
                    "startedAt": "2025-10-16T00:00:00Z",
                    "completedAt": "2025-10-16T00:05:00Z",
                    "operationDuration": 300.5,
                    "rowsAffected": 1000
                }
            ]
        }

    Example:
        # Find failed dbt operations in last 24 hours
        list_operations(
            time_from="2025-10-15T00:00:00Z",
            time_to="2025-10-16T00:00:00Z",
            operation_type="MATERIALISATION"
        )

        # Find operations for specific task run
        # (Note: Use time filters + cross-reference taskRunId from results)
        list_operations(
            time_from="2025-10-15T00:00:00Z",
            time_to="2025-10-16T00:00:00Z"
        )
    """
    client = get_client()
    try:
        return await client.list_operations(
            time_from=time_from,
            time_to=time_to,
            operation_type=operation_type,
            external_id=external_id,
            limit=limit,
            offset=offset,
        )
    except OrchestraAPIError as e:
        return {"error": str(e)}


@mcp.tool()
async def download_dbt_artifact(
    pipeline_run_id: str,
    task_run_id: str,
    artifact_type: str = "manifest",
) -> dict[str, Any]:
    """Download dbt artifacts (manifest.json or run_results.json) from task run.

    Retrieve dbt-specific artifacts generated during pipeline execution.
    These artifacts contain detailed information about dbt model compilation,
    execution results, test outcomes, and metadata.

    Args:
        pipeline_run_id: Unique identifier for the pipeline run
        task_run_id: Unique identifier for the task run (from list_task_runs)
        artifact_type: Type of artifact to download:
                      - "manifest" → manifest.json (dbt project structure, models, tests)
                      - "run_results" → run_results.json (execution results, timing, errors)
                      - "run_results_1" → run_results_1.json (if multiple result files)

    Returns:
        Parsed JSON content of the dbt artifact

    Example:
        # Get dbt manifest to understand project structure
        manifest = download_dbt_artifact(
            pipeline_run_id="8e808ad7-1234-5678-abcd-ef1234567890",
            task_run_id="task-abc123",
            artifact_type="manifest"
        )

        # Get run results to see execution details and errors
        results = download_dbt_artifact(
            pipeline_run_id="8e808ad7-1234-5678-abcd-ef1234567890",
            task_run_id="task-abc123",
            artifact_type="run_results"
        )
    """
    client = get_client()
    try:
        return await client.download_dbt_artifact(
            pipeline_run_id, task_run_id, artifact_type
        )
    except OrchestraAPIError as e:
        return {"error": str(e)}


@mcp.tool()
async def get_dbt_artifacts_from_cloud(
    task_run_id: str,
) -> dict[str, Any]:
    """Fetch dbt Cloud artifacts for an Orchestra task run.

    This is the RECOMMENDED way to get dbt artifacts - it fetches them directly
    from dbt Cloud API instead of relying on Orchestra's artifact storage.

    How it works:
    1. Gets the Orchestra task run to extract dbt Cloud run_id from runParameters
    2. Fetches artifacts directly from dbt Cloud API using that run_id
    3. Returns manifest.json, run_results.json, catalog.json if available

    This method provides more reliable artifact access than download_dbt_artifact,
    since Orchestra doesn't always persist artifacts from dbt Cloud.

    Args:
        task_run_id: Orchestra task run ID (from list_task_runs)

    Returns:
        Dictionary with available artifacts:
        {
            "run_id": 123456,
            "manifest": {...},          # dbt project structure, models, tests
            "run_results": {...},       # execution results, timing, errors
            "catalog": {...}            # table/column metadata, statistics
        }

    Requirements:
        - DBT_CLOUD_API_TOKEN environment variable (dbt Cloud API token)
        - DBT_CLOUD_ACCOUNT_ID environment variable (dbt Cloud account ID)
        - Task must be a dbt Cloud job (integration=DBT with runParameters.run_id)

    Example:
        # Get all dbt artifacts for a task run
        artifacts = get_dbt_artifacts_from_cloud(
            task_run_id="b069b1da-7e4c-4d32-b3b8-5a3c7322d857"
        )

        # Access specific artifact
        if "run_results" in artifacts:
            for result in artifacts["run_results"]["results"]:
                if result["status"] == "error":
                    print(f"Error in {result['unique_id']}: {result['message']}")

    Note:
        This replaces the need for download_dbt_artifact in most cases.
        Use this when you need reliable access to dbt artifacts for debugging,
        lineage analysis, or understanding execution details.
    """
    client = get_client()
    try:
        return await client.get_dbt_artifacts_via_cloud(task_run_id)
    except OrchestraAPIError as e:
        return {"error": str(e)}
    except ValueError as e:
        return {"error": f"dbt Cloud configuration error: {str(e)}"}


@mcp.tool()
async def trigger_pipeline(
    pipeline_id: str, cause: str = "Triggered by Orchestra MCP"
) -> dict[str, Any]:
    """Trigger a pipeline run via webhook.

    Start a new pipeline run for the specified pipeline. This initiates
    execution asynchronously and returns the new run information.

    Args:
        pipeline_id: Unique identifier for the pipeline to trigger
        cause: Optional description of why the pipeline was triggered
               (default: "Triggered by Orchestra MCP")

    Returns:
        Trigger response with new pipeline run ID and initial status

    Example:
        trigger_pipeline(
            pipeline_id="pipeline-xyz789",
            cause="Manual trigger for testing new configuration"
        )
    """
    client = get_client()
    try:
        return await client.trigger_pipeline(pipeline_id, cause)
    except OrchestraAPIError as e:
        return {"error": str(e)}


def main():
    """Entry point for Orchestra MCP server."""
    try:
        # Initialize client on startup to validate credentials
        global _client
        _client = OrchestraClient()

        # Run FastMCP server
        mcp.run()
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Failed to start Orchestra MCP server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
