"""FastAPI execution layer dependency injection registry mappings."""

from fastapi import Request
from agrivision.models.classifier import CropDiseaseClassifier
from google.adk.runners import Runner


def get_classifier(request: Request) -> CropDiseaseClassifier:
    """Injects the pre-loaded neural classification system layer from application state contexts."""
    return request.app.state.classifier


def get_agent_runner(request: Request) -> Runner:
    """Injects the operational multi-tool Google ADK agent execution orchestration runner."""
    return request.app.state.runner