"""Pydantic definition layer matching the target system validation matrix."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Structured response schema monitoring system vitality signatures."""
    status: str = Field(..., examples=["healthy"])
    engine: str = Field(..., examples=["operational"])
    model_loaded: bool = Field(...)
    version: str = Field(..., examples=["1.0.0"])


class ModelInfoResponse(BaseModel):
    """Detailed telemetry describing the encapsulated deep tech components."""
    architecture: str = Field(..., examples=["EfficientNetB0"])
    framework: str = Field(..., examples=["TensorFlow/Keras"])
    version: str = Field(..., examples=["1.0.0"])
    accuracy: float = Field(..., examples=[0.89])
    num_classes: int = Field(..., examples=[5])
    classes: List[str] = Field(...)


class DiseaseCatalogResponse(BaseModel):
    """Static catalog listing all diagnostic target capabilities."""
    supported_count: int = Field(..., examples=[5])
    list: List[str] = Field(...)


class PredictionResponse(BaseModel):
    """Production data model for standard target field classifications."""
    status: str = Field(..., examples=["success"])
    field_id: str = Field(..., examples=["NGA-AKWA-IBOM-ZONE-A"])
    detected_disease: str = Field(..., examples=["Leaf Blight"])
    confidence_score: float = Field(..., examples=[0.9452])
    all_scores: Dict[str, float] = Field(...)
    agent_reasoning_output: str = Field(...)


class BatchPredictionResponse(BaseModel):
    """Aggregated encapsulation response for multi-target batch ingestion processing."""
    results: List[PredictionResponse] = Field(...)
    total: int = Field(..., examples=[2])


class FeedbackRequest(BaseModel):
    """Secure inbound target verification structure for system model drift tuning."""
    scan_id: str = Field(..., min_length=3)
    flagged_error: bool = Field(...)
    user_provided_label: str = Field(...)
    additional_context: Optional[str] = Field(None, max_length=500)


class FeedbackResponse(BaseModel):
    """Outbound tracking payload generated post-in-memory ingestion processing."""
    feedback_id: str = Field(...)
    status: str = Field(..., examples=["received"])
    message: str = Field(...)