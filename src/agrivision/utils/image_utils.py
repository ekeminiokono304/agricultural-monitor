"""Helper logic handling image operations safely to avoid resource leaks."""

import io
import logging
from PIL import Image
from fastapi import HTTPException, status

logger = logging.getLogger("agrivision.utils.image_utils")


def validate_and_parse_image(image_bytes: bytes) -> Image.Image:
    """Parses raw stream arrays verifying integrity signatures.

    Raises:
        HTTPException: 400 bad image structure signature flags.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
        
        # Re-open stream because verify() closes structural pointers
        parsed_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return parsed_image
    except Exception as err:
        logger.warning(f"Malformed image structure signature uploaded: {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The provided file payload is not a valid, uncorrupted image asset."
        )