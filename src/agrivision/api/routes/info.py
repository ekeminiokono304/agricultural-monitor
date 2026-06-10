"""FastAPI route logic exposing system status and model architecture info."""

from fastapi import APIRouter, Depends, Request
from agrivision.config import settings
from agrivision.api.dependencies import get_classifier
from agrivision.models.schemas import HealthResponse, ModelInfoResponse, DiseaseCatalogResponse

router = APIRouter(tags=["System Metrics & Info Monitoring"])


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    """Verifies operational state metrics and verifies the presence of backend dependencies."""
    model_attached = request.app.state.classifier.model is not None
    return HealthResponse(
        status="healthy",
        engine="operational",
        model_loaded=model_attached,
        version=settings.APP_VERSION
    )


@router.get("/model/info", response_model=ModelInfoResponse)
async def model_info(classifier=Depends(get_classifier)):
    """Exposes underlying computer vision frameworks, architecture settings, and classification metrics."""
    return ModelInfoResponse(
        architecture="EfficientNetB0",
        framework="TensorFlow/Keras",
        version=settings.MODEL_VERSION,
        accuracy=settings.MODEL_ACCURACY,
        num_classes=len(classifier.classes),
        classes=classifier.classes
    )


@router.get("/diseases", response_model=DiseaseCatalogResponse)
async def get_diseases(classifier=Depends(get_classifier)):
    """Lists all valid agricultural crop disease labels indexed by the classification engine."""
    return DiseaseCatalogResponse(
        supported_count=len(classifier.classes),
        list=classifier.classes
    )