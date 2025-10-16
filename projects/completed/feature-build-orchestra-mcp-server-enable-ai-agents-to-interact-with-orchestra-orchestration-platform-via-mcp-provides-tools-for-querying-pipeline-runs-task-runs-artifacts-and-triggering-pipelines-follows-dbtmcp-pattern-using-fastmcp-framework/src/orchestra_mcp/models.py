"""Pydantic models for Orchestra API responses."""

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class PipelineRun(BaseModel):
    """Orchestra pipeline run model."""

    id: str = Field(description="Unique pipeline run ID")
    pipeline_id: str = Field(description="Pipeline ID that was executed")
    status: str = Field(description="Run status (e.g., 'running', 'success', 'failed')")
    created_at: datetime = Field(description="When the run was created")
    started_at: Optional[datetime] = Field(None, description="When execution started")
    finished_at: Optional[datetime] = Field(None, description="When execution finished")
    duration_seconds: Optional[int] = Field(None, description="Total runtime in seconds")
    trigger_type: Optional[str] = Field(None, description="How the run was triggered")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional run metadata")


class PipelineRunStatus(BaseModel):
    """Simplified pipeline run status."""

    id: str = Field(description="Pipeline run ID")
    status: str = Field(description="Current status")
    duration_seconds: Optional[int] = Field(None, description="Runtime in seconds")
    started_at: Optional[datetime] = Field(None, description="Start time")
    finished_at: Optional[datetime] = Field(None, description="Finish time")


class TaskRun(BaseModel):
    """Orchestra task run model."""

    id: str = Field(description="Unique task run ID")
    pipeline_run_id: str = Field(description="Parent pipeline run ID")
    task_name: str = Field(description="Name of the task")
    status: str = Field(description="Task status")
    started_at: Optional[datetime] = Field(None, description="Task start time")
    finished_at: Optional[datetime] = Field(None, description="Task finish time")
    duration_seconds: Optional[int] = Field(None, description="Task runtime in seconds")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Task metadata")


class ArtifactInfo(BaseModel):
    """Information about available artifacts."""

    filename: str = Field(description="Artifact filename")
    size_bytes: Optional[int] = Field(None, description="File size in bytes")
    content_type: Optional[str] = Field(None, description="MIME type")
    created_at: Optional[datetime] = Field(None, description="When artifact was created")


class TriggerResponse(BaseModel):
    """Response from triggering a pipeline."""

    pipeline_run_id: str = Field(description="ID of the triggered run")
    pipeline_id: str = Field(description="ID of the pipeline")
    status: str = Field(description="Initial status")
    message: str = Field(description="Success/error message")
