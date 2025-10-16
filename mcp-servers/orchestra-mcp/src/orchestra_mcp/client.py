"""Orchestra API client for making authenticated requests."""

import os
from typing import Any, Optional
from datetime import datetime
import httpx
from .models import PipelineRun, PipelineRunStatus, TaskRun, ArtifactInfo, TriggerResponse


class DBTCloudClient:
    """Client for fetching dbt Cloud artifacts via Admin API."""

    def __init__(
        self,
        api_token: Optional[str] = None,
        account_id: Optional[str] = None,
        host: Optional[str] = None,
        timeout: int = 30,
    ):
        """Initialize dbt Cloud API client.

        Args:
            api_token: dbt Cloud API token (from Account Settings → API Tokens)
            account_id: dbt Cloud account ID
            host: dbt Cloud host URL (default: cloud.getdbt.com)
            timeout: Request timeout in seconds
        """
        self.api_token = api_token or os.getenv("DBT_CLOUD_API_TOKEN")
        self.account_id = account_id or os.getenv("DBT_CLOUD_ACCOUNT_ID")
        self.host = host or os.getenv("DBT_CLOUD_HOST", "cloud.getdbt.com")

        if not self.api_token:
            raise ValueError(
                "dbt Cloud API token required. Set DBT_CLOUD_API_TOKEN environment variable "
                "or pass api_token parameter."
            )
        if not self.account_id:
            raise ValueError(
                "dbt Cloud account ID required. Set DBT_CLOUD_ACCOUNT_ID environment variable "
                "or pass account_id parameter."
            )

        self.base_url = f"https://{self.host}/api/v2/accounts/{self.account_id}"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Token {self.api_token}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def get_run_artifact(
        self, run_id: int, artifact_path: str, step: Optional[int] = None
    ) -> Any:
        """Download artifact from dbt Cloud run.

        Args:
            run_id: dbt Cloud run ID
            artifact_path: Path to artifact (e.g., 'manifest.json', 'run_results.json')
            step: Optional step index (defaults to last step)

        Returns:
            Parsed JSON artifact content

        Raises:
            httpx.HTTPStatusError: If artifact not found or request fails
        """
        url = f"{self.base_url}/runs/{run_id}/artifacts/{artifact_path}"
        params = {}
        if step is not None:
            params["step"] = step

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def list_run_artifacts(self, run_id: int, step: Optional[int] = None) -> list[str]:
        """List available artifacts for a dbt Cloud run.

        Args:
            run_id: dbt Cloud run ID
            step: Optional step index (defaults to last step)

        Returns:
            List of artifact paths available

        Note:
            dbt Cloud doesn't have a dedicated list endpoint, so this returns
            common artifact paths that typically exist.
        """
        # Common dbt artifacts that typically exist
        common_artifacts = [
            "manifest.json",
            "run_results.json",
            "catalog.json",
        ]

        # Try to fetch each and return those that exist
        available = []
        for artifact_path in common_artifacts:
            try:
                await self.get_run_artifact(run_id, artifact_path, step)
                available.append(artifact_path)
            except httpx.HTTPStatusError:
                continue

        return available


class OrchestraAPIError(Exception):
    """Base exception for Orchestra API errors."""

    pass


class OrchestraClient:
    """Client for interacting with Orchestra Metadata API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
    ):
        """Initialize Orchestra API client.

        Args:
            api_key: Orchestra API key (from Settings → API Key).
                    If not provided, reads from ORCHESTRA_API_KEY env var.
            base_url: Base URL for Orchestra API.
                     If not provided, reads from ORCHESTRA_API_BASE_URL env var.
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key or os.getenv("ORCHESTRA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Orchestra API key required. Set ORCHESTRA_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.base_url = (
            base_url
            or os.getenv("ORCHESTRA_API_BASE_URL")
            or "https://app.getorchestra.io/api/engine/public/"
        )
        self.timeout = timeout

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def _request(
        self, method: str, path: str, **kwargs
    ) -> dict[str, Any]:
        """Make an authenticated request to Orchestra API.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (relative to base_url)
            **kwargs: Additional arguments for httpx request

        Returns:
            Response JSON data

        Raises:
            OrchestraAPIError: If request fails
        """
        try:
            response = await self.client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = f"Orchestra API error ({e.response.status_code}): {e.response.text}"
            raise OrchestraAPIError(error_msg) from e
        except httpx.RequestError as e:
            error_msg = f"Orchestra API request failed: {str(e)}"
            raise OrchestraAPIError(error_msg) from e

    async def list_pipeline_runs(
        self,
        time_from: Optional[str] = None,
        time_to: Optional[str] = None,
        status: Optional[str] = None,
        pipeline_run_ids: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List pipeline runs with optional filtering.

        Args:
            time_from: Start time filter (ISO 8601 format, e.g., '2025-04-01T00:00:00Z')
            time_to: End time filter (ISO 8601 format)
            status: Filter by status (CREATED, RUNNING, SUCCEEDED, WARNING, FAILED, CANCELLING, CANCELLED)
            pipeline_run_ids: Comma-separated list of pipeline run IDs to filter
            limit: Maximum number of results (default: 100, max: 1000)
            offset: Pagination offset (default: 0)

        Returns:
            Paginated response with structure:
            {
                "page": 1,
                "pageSize": 50,
                "total": 2367,
                "results": [...]
            }

        Note:
            Without date filters, only last 7 days of data available.
            Time filters must be used together or not at all (max 7 day range).
        """
        params = {"limit": min(limit, 1000), "offset": offset}
        if time_from:
            params["time_from"] = time_from
        if time_to:
            params["time_to"] = time_to
        if status:
            params["status"] = status
        if pipeline_run_ids:
            params["pipeline_run_ids"] = pipeline_run_ids

        # Orchestra returns paginated response, return as-is
        return await self._request("GET", "pipeline_runs", params=params)

    async def get_pipeline_run_status(
        self, pipeline_run_id: str
    ) -> dict[str, Any]:
        """Get status for specific pipeline run.

        Note: Orchestra doesn't have individual detail endpoints.
        This uses the list endpoint with pipeline_run_ids filter.

        Args:
            pipeline_run_id: Pipeline run ID

        Returns:
            Pipeline run dictionary from results[0]
        """
        data = await self.list_pipeline_runs(pipeline_run_ids=pipeline_run_id, limit=1)
        results = data.get("results", [])
        if not results:
            raise OrchestraAPIError(f"Pipeline run {pipeline_run_id} not found")
        return results[0]

    async def get_pipeline_run_details(
        self, pipeline_run_id: str
    ) -> dict[str, Any]:
        """Get comprehensive details for specific pipeline run.

        Note: Orchestra doesn't have individual detail endpoints.
        This uses the list endpoint with pipeline_run_ids filter.

        Args:
            pipeline_run_id: Pipeline run ID

        Returns:
            Complete pipeline run information
        """
        # Same as get_pipeline_run_status - Orchestra list endpoint returns full details
        return await self.get_pipeline_run_status(pipeline_run_id)

    async def list_task_runs(
        self,
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
        """List task runs with optional filtering.

        Args:
            pipeline_run_id: Filter by specific pipeline run ID
            time_from: Start time filter (ISO 8601 format)
            time_to: End time filter (ISO 8601 format)
            status: Filter by status (CREATED, SKIPPED, QUEUED, RUNNING, SUCCEEDED, WARNING, FAILED, CANCELLING, CANCELLED)
            pipeline_ids: Comma-separated pipeline IDs
            integration: Comma-separated integration names
            task_run_ids: Comma-separated task run IDs
            limit: Maximum number of results (default: 100, max: 1000)
            offset: Pagination offset (default: 0)

        Returns:
            Paginated response with structure:
            {
                "page": 1,
                "pageSize": 50,
                "total": 1234,
                "results": [...]
            }

        Note:
            Time filters must be used together or not at all (max 7 day range).
        """
        params = {"limit": min(limit, 1000), "offset": offset}
        if pipeline_run_id:
            params["pipeline_run_id"] = pipeline_run_id
        if time_from:
            params["time_from"] = time_from
        if time_to:
            params["time_to"] = time_to
        if status:
            params["status"] = status
        if pipeline_ids:
            params["pipeline_ids"] = pipeline_ids
        if integration:
            params["integration"] = integration
        if task_run_ids:
            params["task_run_ids"] = task_run_ids

        return await self._request("GET", "task_runs", params=params)

    async def get_task_run_artifacts(
        self, pipeline_run_id: str, task_run_id: str
    ) -> list[dict[str, Any]]:
        """List available artifacts for a task run.

        Args:
            pipeline_run_id: Pipeline run ID
            task_run_id: Task run ID

        Returns:
            List of artifact info dictionaries
        """
        data = await self._request(
            "GET", f"pipeline_runs/{pipeline_run_id}/task_runs/{task_run_id}/artifacts"
        )
        return data.get("data", data) if isinstance(data, dict) else data

    async def download_task_artifact(
        self, pipeline_run_id: str, task_run_id: str, filename: str
    ) -> str:
        """Download specific task run artifact.

        Args:
            pipeline_run_id: Pipeline run ID
            task_run_id: Task run ID
            filename: Artifact filename to download

        Returns:
            Artifact content as string
        """
        response = await self.client.get(
            f"pipeline_runs/{pipeline_run_id}/task_runs/{task_run_id}/artifacts/download",
            params={"filename": filename},
        )
        response.raise_for_status()
        return response.text

    async def list_operations(
        self,
        time_from: Optional[str] = None,
        time_to: Optional[str] = None,
        operation_type: Optional[str] = None,
        external_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List operations (detailed task-level execution info) with optional filtering.

        Operations provide granular details about task executions, including error messages,
        integration-specific metadata (e.g., dbt model results), and execution metrics.

        Args:
            time_from: Start time filter (ISO 8601 format, e.g., '2025-04-01T00:00:00Z')
            time_to: End time filter (ISO 8601 format)
            operation_type: Filter by operation type (QUERY, AGGREGATION, DEPLOY, MATERIALISATION,
                          TEST, SNAPSHOT, SOURCE, SEED, etc.)
            external_id: Filter by external identifier (e.g., dbt model name)
            limit: Maximum number of results (default: 100, max: 1000)
            offset: Pagination offset (default: 0)

        Returns:
            Paginated response with structure:
            {
                "page": 1,
                "pageSize": 50,
                "total": 567,
                "results": [
                    {
                        "id": "...",
                        "pipelineRunId": "...",
                        "taskRunId": "...",
                        "operationName": "model.my_project.my_model",
                        "operationStatus": "SUCCEEDED" | "FAILED",
                        "message": "Error message or success message",
                        "externalStatus": "SUCCESS" | "ERROR",
                        "externalDetail": "Additional integration-specific details",
                        "integration": "DBT" | "SNOWFLAKE" | etc.,
                        "integrationJob": "DBT_RUN_MODEL",
                        "operationType": "MATERIALISATION",
                        "startedAt": "2025-10-16T...",
                        "completedAt": "2025-10-16T...",
                        "operationDuration": 12.5,
                        "rowsAffected": 1000
                    }
                ]
            }

        Note:
            Without date filters, only last 7 days of data available.
            Time filters must be used together or not at all (max 7 day range).

            This endpoint provides the ERROR MESSAGES that were missing from task_runs!
        """
        params = {"limit": min(limit, 1000), "offset": offset}
        if time_from:
            params["time_from"] = time_from
        if time_to:
            params["time_to"] = time_to
        if operation_type:
            params["operation_type"] = operation_type
        if external_id:
            params["external_id"] = external_id

        return await self._request("GET", "operations", params=params)

    async def download_dbt_artifact(
        self, pipeline_run_id: str, task_run_id: str, artifact_type: str = "manifest"
    ) -> dict[str, Any]:
        """Download dbt artifacts (manifest.json or run_results.json) from task run.

        Args:
            pipeline_run_id: Pipeline run ID
            task_run_id: Task run ID
            artifact_type: Type of artifact to download:
                         - "manifest" → manifest.json
                         - "run_results" → run_results.json
                         - "run_results_1" → run_results_1.json (if multiple exist)

        Returns:
            Parsed JSON content of the artifact

        Example:
            # Get dbt manifest
            manifest = await client.download_dbt_artifact(
                pipeline_run_id="...",
                task_run_id="...",
                artifact_type="manifest"
            )

            # Get run results
            results = await client.download_dbt_artifact(
                pipeline_run_id="...",
                task_run_id="...",
                artifact_type="run_results"
            )
        """
        filename_map = {
            "manifest": "manifest.json",
            "run_results": "run_results.json",
            "run_results_1": "run_results_1.json",
            "run_results_2": "run_results_2.json",
        }

        filename = filename_map.get(artifact_type, f"{artifact_type}.json")

        try:
            response = await self.client.get(
                f"pipeline_runs/{pipeline_run_id}/task_runs/{task_run_id}/artifacts/download",
                params={"filename": filename},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = f"dbt artifact '{filename}' not found (status {e.response.status_code})"
            raise OrchestraAPIError(error_msg) from e
        except httpx.RequestError as e:
            error_msg = f"Failed to download dbt artifact '{filename}': {str(e)}"
            raise OrchestraAPIError(error_msg) from e

    async def get_dbt_cloud_run_id(self, task_run_id: str) -> Optional[int]:
        """Extract dbt Cloud run_id from Orchestra task run.

        Args:
            task_run_id: Orchestra task run ID

        Returns:
            dbt Cloud run ID if task is a dbt job, None otherwise

        Raises:
            OrchestraAPIError: If task run not found
        """
        # Get task run details
        task_runs = await self.list_task_runs(task_run_ids=task_run_id, limit=1)
        results = task_runs.get("results", [])

        if not results:
            raise OrchestraAPIError(f"Task run {task_run_id} not found")

        task_run = results[0]

        # Check if this is a dbt task with run_id in runParameters
        if task_run.get("integration") == "DBT":
            run_params = task_run.get("runParameters", {})
            return run_params.get("run_id")

        return None

    async def get_dbt_artifacts_via_cloud(
        self,
        task_run_id: str,
        dbt_cloud_client: Optional[DBTCloudClient] = None,
    ) -> dict[str, Any]:
        """Fetch dbt artifacts from dbt Cloud API for an Orchestra task run.

        This method:
        1. Gets the Orchestra task run
        2. Extracts the dbt Cloud run_id from runParameters
        3. Fetches artifacts from dbt Cloud API
        4. Returns manifest.json, run_results.json, catalog.json if available

        Args:
            task_run_id: Orchestra task run ID
            dbt_cloud_client: Optional DBTCloudClient instance
                            (will create one if not provided)

        Returns:
            Dictionary with available artifacts:
            {
                "run_id": 123456,
                "manifest": {...},
                "run_results": {...},
                "catalog": {...}
            }

        Raises:
            OrchestraAPIError: If task not found or not a dbt task
            ValueError: If dbt Cloud credentials not configured

        Example:
            # Automatic client creation (uses env vars)
            artifacts = await orchestra_client.get_dbt_artifacts_via_cloud(
                task_run_id="abc-123"
            )

            # Or bring your own client
            dbt_client = DBTCloudClient(api_token="...", account_id="...")
            artifacts = await orchestra_client.get_dbt_artifacts_via_cloud(
                task_run_id="abc-123",
                dbt_cloud_client=dbt_client
            )
        """
        # Get dbt Cloud run_id
        dbt_run_id = await self.get_dbt_cloud_run_id(task_run_id)
        if not dbt_run_id:
            raise OrchestraAPIError(
                f"Task run {task_run_id} is not a dbt Cloud job or missing run_id"
            )

        # Create dbt Cloud client if not provided
        should_close_client = False
        if dbt_cloud_client is None:
            dbt_cloud_client = DBTCloudClient()
            should_close_client = True

        try:
            # Fetch artifacts from dbt Cloud
            artifacts = {"run_id": dbt_run_id}

            # Try to get each artifact type
            artifact_types = ["manifest.json", "run_results.json", "catalog.json"]
            for artifact_path in artifact_types:
                try:
                    artifact_key = artifact_path.replace(".json", "")
                    artifacts[artifact_key] = await dbt_cloud_client.get_run_artifact(
                        run_id=dbt_run_id, artifact_path=artifact_path
                    )
                except httpx.HTTPStatusError:
                    # Artifact not available, skip it
                    continue

            return artifacts

        finally:
            if should_close_client:
                await dbt_cloud_client.close()

    async def trigger_pipeline(
        self, pipeline_id: str, cause: str = "Triggered by Orchestra MCP"
    ) -> dict[str, Any]:
        """Trigger a pipeline run via webhook.

        Args:
            pipeline_id: Pipeline ID to trigger
            cause: Optional description of why pipeline was triggered

        Returns:
            Trigger response with new run information
        """
        # Note: The webhook endpoint is slightly different from metadata API
        webhook_url = f"https://app.getorchestra.io/engine/public/pipelines/{pipeline_id}/start"

        response = await self.client.post(
            webhook_url,
            json={"cause": cause},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", data) if isinstance(data, dict) else data
