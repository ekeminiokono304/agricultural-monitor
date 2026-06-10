"""Configuration module for the AgriVision application layer."""

import logging
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

# Setup localized structural logging metrics
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("agrivision.config")


class Settings(BaseSettings):
    """Production settings architecture using Pydantic Settings v2."""

    # Core Credentials
    GOOGLE_API_KEY: str

    # Model Parameters
    MODEL_PATH: str = "models/agrivision_model.h5"
    MODEL_NAME: str = "AgriVision EfficientNetB0 Engine"
    MODEL_VERSION: str = "1.0.0"
    MODEL_ACCURACY: float = 0.89

    # Application Configuration
    APP_NAME: str = "AgriVision API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    MAX_IMAGE_SIZE_MB: int = 10

    # Categorization Ground Truth
    CLASS_NAMES: List[str] = ["Healthy", "Leaf Blight", "Powdery Mildew", "Rust", "Leaf Spot"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


try:
    settings = Settings()
    logger.info("Successfully bound environment definitions to Settings entity schema.")
except Exception as err:
    logger.error(f"Initialization failure during settings binding: {str(err)}")
    raise err