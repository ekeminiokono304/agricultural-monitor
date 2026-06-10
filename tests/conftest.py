"""Unified validation tracking fixture configurations for pytest execution structures."""

import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from agrivision.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Yields a test communication channel mapped directly against core FastAPI logic instances."""
    with TestClient(app) as test_channel:
        yield test_channel


@pytest.fixture
def sample_image_bytes() -> bytes:
    """Generates synthetic green placeholder image mock arrays directly inside execution frames."""
    image_canvas = Image.new('RGB', (224, 224), color=(34, 139, 34))
    buffer_memory_stream = io.BytesIO()
    image_canvas.save(buffer_memory_stream, format='JPEG')
    return buffer_memory_stream.getvalue()