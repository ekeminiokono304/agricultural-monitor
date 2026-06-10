"""AgriVision root package execution namespace initialization mapping."""

from agrivision.config import settings

__all__ = ["settings"]
__version__ = settings.APP_VERSION