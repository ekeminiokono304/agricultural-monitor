"""Main entry point configuration engine."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agrivision.config import settings
from agrivision.models.classifier import CropDiseaseClassifier
from agrivision.agent.agrivision_agent import build_adk_runner
from agrivision.api.routes import info, predict, feedback

logger = logging.getLogger("agrivision.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager handling system startup tasks and resource teardowns smoothly."""
    logger.info("Initializing AgriVision deep learning and semantic agent components...")
    
    # Instance initialization block mapping logic patterns
    classifier_instance = CropDiseaseClassifier()
    classifier_instance.load_model_weights()
    
    adk_runner_instance = build_adk_runner()
    
    # Store instances in application state context pointers
    app.state.classifier = classifier_instance
    app.state.runner = adk_runner_instance
    
    logger.info("AgriVision application core engines are fully loaded and operational.")
    yield
    logger.info("Beginning system teardown... Releasing active thread resources safely.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs"
)

# Configure resource cross-origin mapping definitions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints to app router instance
app.include_router(info.router)
app.include_router(predict.router)
app.include_router(feedback.router)