"""Primary inference endpoint pipelines processing target field assets."""

from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from agrivision.api.dependencies import get_classifier, get_agent_runner
from agrivision.models.schemas import PredictionResponse, BatchPredictionResponse
from agrivision.agent.agrivision_agent import run_agent

router = APIRouter(prefix="/predict", tags=["Analytical Classification Matrix Core"])


@router.post("/disease", response_model=PredictionResponse)
async def predict_disease_endpoint(
    file: UploadFile = File(...),
    field_id: str = Form(...),
    classifier=Depends(get_classifier),
    runner=Depends(get_agent_runner)
):
    """Processes crop asset data, runs CNN evaluations, and maps output through Google ADK reasoning tools."""
    try:
        image_payload_bytes = await file.read()
        
        # Core integration logic loop fix: call CNN execution stack directly
        cnn_analysis = classifier.predict(image_payload_bytes)
        
        # Feed the generated metrics directly into the Google ADK streaming engine
        agent_reasoning = await run_agent(
            runner=runner,
            disease_label=cnn_analysis["label"],
            confidence=cnn_analysis["confidence"],
            field_id=field_id
        )
        
        return PredictionResponse(
            status="success",
            field_id=field_id,
            detected_disease=cnn_analysis["label"],
            confidence_score=cnn_analysis["confidence"],
            all_scores=cnn_analysis["all_scores"],
            agent_reasoning_output=agent_reasoning
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline inference routing failure processing crop sample: {str(err)}"
        )


@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch_endpoint(
    files: List[UploadFile] = File(...),
    field_id: str = Form(...),
    classifier=Depends(get_classifier),
    runner=Depends(get_agent_runner)
):
    """Handles continuous array files sequentially for handling multiple target zones simultaneously."""
    aggregated_results = []
    for asset in files:
        try:
            bytes_data = await asset.read()
            cnn_eval = classifier.predict(bytes_data)
            reasoning = await run_agent(
                runner=runner,
                disease_label=cnn_eval["label"],
                confidence=cnn_eval["confidence"],
                field_id=field_id
            )
            aggregated_results.append(
                PredictionResponse(
                    status="success",
                    field_id=field_id,
                    detected_disease=cnn_eval["label"],
                    confidence_score=cnn_eval["confidence"],
                    all_scores=cnn_eval["all_scores"],
                    agent_reasoning_output=reasoning
                )
            )
        except Exception:
            continue
            
    if not aggregated_results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch asset formatting was invalid or could not be processed by the classification engine."
        )
        
    return BatchPredictionResponse(results=aggregated_results, total=len(aggregated_results))