"""Google ADK agent orchestration engine configuration pipeline."""

import logging
from google.adk.agents import llm_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agrivision.config import settings
from agrivision.agent.tools import get_disease_info, get_treatment_advice, estimate_yield_impact

logger = logging.getLogger("agrivision.agent.agrivision_agent")


def build_adk_runner() -> Runner:
    """Constructs a clean instance of the Google ADK processing graph runtime wrapper."""
    logger.info("Configuring localized Google ADK LlmAgent structural definition profiles...")
    
    agrivision_agent = llm_agent.LlmAgent(
        name="AgriVision",
        model="gemini-2.0-flash",
        instruction=(
            "You are AgriVision, a distinguished production-grade autonomous agricultural engine. "
            "Your main task is diagnosing Nigerian crop anomalies and returning structured advice profiles. "
            "Use your tools to extract exact disease details, recommend specific treatments, and calculate "
            "potential yield impact before giving your final analysis."
        ),
        tools=[get_disease_info, get_treatment_advice, estimate_yield_impact]
    )

    session_service = InMemorySessionService()
    
    runner = Runner(
        session_service=session_service,
        agent=agrivision_agent,
        app_name=settings.APP_NAME
    )
    return runner


async def run_agent(runner: Runner, disease_label: str, confidence: float, field_id: str) -> str:
    """Streams data arrays cleanly from the async engine to resolve the event collection bug."""
    session_id = f"session_{field_id}"
    input_prompt = (
        f"A crop image from field token ID '{field_id}' was processed and classified as '{disease_label}' "
        f"with a statistical confidence score of {confidence:.2f}. Execute complete analytical matrix profiles."
    )
    
    full_response = ""
    try:
        # Fixed async chunk aggregation pattern mapping loop
        async for event in runner.run_async(
            user_id="farmer_terminal",
            session_id=session_id,
            new_message=types.Content(role="user", parts=[types.Part.from_text(text=input_prompt)])
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        full_response += part.text
                        
        return full_response.strip() if full_response else "Expert system reasoning module is buffering data."
    except Exception as err:
        logger.error(f"ADK runner pipeline exception trace encountered: {str(err)}")
        return f"Autonomous agent reasoning stream failed due to system exception: {str(err)}"