"""In-memory telemetry tracking for monitoring target logging entries."""

import uuid
import logging
from fastapi import APIRouter, HTTPException, status
from agrivision.models.schemas import FeedbackRequest, FeedbackResponse

logger = logging.getLogger("agrivision.api.routes.feedback")
router = APIRouter(tags=["Telemetry Data Registry Loops"])

# Thread-safe local storage for monitoring user corrections
IN_MEMORY_FEEDBACK_DB = {}


@router.post("/feedback", response_model=FeedbackResponse)
async def process_feedback_endpoint(payload: FeedbackRequest):
    """Saves user tracking logs into localized buffers to track model drift anomalies."""
    try:
        tracking_token_id = str(uuid.uuid4())
        IN_MEMORY_FEEDBACK_DB[tracking_token_id] = payload.model_dump()
        
        logger.info(f"Successfully cached system calibration telemetry tracking point token: {tracking_token_id}")
        return FeedbackResponse(
            feedback_id=tracking_token_id,
            status="received",
            message="Telemetry feedback successfully registered."
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Telemetry synchronization error: {str(err)}"
        )