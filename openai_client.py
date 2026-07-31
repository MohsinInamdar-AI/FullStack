"""
openai_client.py - Wrapper around OpenAI's Images API for text-to-image generation.
"""
import base64
import io
import os

from openai import OpenAI
from PIL import Image


class OpenAIImageError(Exception):
    pass


def generate_image(
    prompt: str,
    model_id: str = "gpt-image-1",
    size: str = "1024x1024",
    api_key: str | None = None,
) -> Image.Image:
    """
    Calls the OpenAI Images API to generate an image from a prompt.
    Returns a PIL Image. Raises OpenAIImageError on failure.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise OpenAIImageError(
            "No OpenAI API key found. Set OPENAI_API_KEY env var or pass api_key."
        )

    client = OpenAI(api_key=key)

    try:
        response = client.images.generate(
            model=model_id,
            prompt=prompt,
            size=size,
            n=1,
        )
    except Exception as e:
        raise OpenAIImageError(f"OpenAI API error: {e}")

    try:
        b64_data = response.data[0].b64_json
        image_bytes = base64.b64decode(b64_data)
        image = Image.open(io.BytesIO(image_bytes))
        image.load()
        return image
    except Exception as e:
        raise OpenAIImageError(f"Failed to decode image from response: {e}")