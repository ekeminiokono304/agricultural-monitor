"""Domain-specific functional tools exposed to the Google ADK runner engine."""

import logging

logger = logging.getLogger("agrivision.agent.tools")


def get_disease_info(disease_name: str) -> str:
    """Retrieves diagnostic documentation and contextual metadata for a specific crop disease anomaly.

    Args:
        disease_name: Exact string matching structural class labels.
    """
    logger.info(f"ADK executable tool 'get_disease_info' invoked for target label: {disease_name}")
    info_db = {
        "Leaf Blight": "Fungal/Bacterial infection causing rapid, localized tissue death and leaf wilting.",
        "Powdery Mildew": "Fungus appearing as distinct white powder spots on foliage surface vectors.",
        "Rust": "Fungal pathogen causing orange, brown, or yellow pustules compromising leaf vascular networks.",
        "Leaf Spot": "Bacterial or fungal circles on foliage limiting overall chlorophyll processing activity.",
        "Healthy": "Crop exhibits standard structural metabolic characteristics and vibrant foliage metrics."
    }
    return info_db.get(disease_name, "Unknown crop abnormality discovered outside localized indexing frameworks.")


def get_treatment_advice(disease_name: str, severity: str) -> str:
    """Generates immediate response protocols and regional action blueprints for treating infected crop metrics.

    Args:
        disease_name: The diagnosed anomaly label.
        severity: Evaluated risk band based on tracking variables.
    """
    logger.info(f"ADK executable tool 'get_treatment_advice' triggered under severity framework: {severity}")
    if disease_name == "Healthy":
        return "Maintain regular irrigation cycles. No chemical or emergency action required."
    return f"Immediate Interventions for {disease_name} [{severity}]: Apply copper-based targeted fungicide."


def estimate_yield_impact(disease_name: str, confidence: float) -> str:
    """Calculates overall economic risk indices based on statistical engine tracking signals.

    Args:
        disease_name: Target diagnostic metric.
        confidence: Normalized model confidence value.
    """
    logger.info(f"ADK evaluation calculation matrix invoked for tracking index metric: {confidence}")
    if disease_name == "Healthy":
        return "0% Expected Loss. Yield trends map normally against established local baselines."
    projected_loss = int(confidence * 45)
    return f"Estimated yield degradation profile: Approximately {projected_loss}% overall impact if untreated."