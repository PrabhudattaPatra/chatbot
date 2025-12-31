import logging
import requests
import fitz
import io
import base64
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

def pdf_url_to_images(pdf_url: str, dpi: int = 300) -> list[Image.Image]:
    try:
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()

        doc = fitz.open(stream=response.content, filetype="pdf")
        images = []

        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)

        for page in doc:
            pix = page.get_pixmap(matrix=matrix)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            images.append(img)

        return images

    except Exception:
        logger.exception(f"Failed to convert PDF to images: {pdf_url}")
        raise


def pil_image_to_base64(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
