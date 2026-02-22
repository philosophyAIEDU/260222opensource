"""Utility helpers for image encoding and OCR result processing."""

from __future__ import annotations

import base64
from io import BytesIO

from PIL import Image


SUPPORTED_IMAGE_FORMATS = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
}


def image_file_to_base64(uploaded_file) -> tuple[str, str]:
    image = Image.open(uploaded_file)

    image_format = image.format or "PNG"
    mime_type = SUPPORTED_IMAGE_FORMATS.get(image_format.upper(), "image/png")

    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    buffer = BytesIO()
    save_format = "JPEG" if mime_type == "image/jpeg" else "PNG" if mime_type == "image/png" else "WEBP"
    image.save(buffer, format=save_format)

    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded, mime_type


def normalize_output(text: str) -> str:
    return text.strip()


def ensure_nonempty_message(text: str) -> str:
    if text.strip():
        return text
    return "글자를 찾지 못했어요. 더 선명한 사진을 올려주세요."
